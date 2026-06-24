#!/usr/bin/env python3
"""
generate_static_tiles.py
Generates static PNG tiles for all MTELGON COGs.

Usage:
    python3 generate_static_tiles.py [--dry-run] [--layer ndvi] [--field MTELGON-B2] [--date 2026-05-04]

Output layout:
    ~/remote/Timeseries/tiles/{date}/{field}/{layer}/{z}/{x}/{y}.png

Zoom levels: 14–19  (~1.2 GB expected)
Concurrency: controlled by --workers (default 4)
"""

import os
import sys
import shutil
import subprocess
import tempfile
import argparse
import logging
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────
# CHANGED: Using Path.home() so it writes to /home/lima-hpenvy/ instead of /home/remote/
COG_BASE   = Path.home() / "remote" / "Timeseries" / "COGoutputs"
TILES_BASE = Path.home() / "remote" / "Timeseries" / "tiles"
TMP_BASE   = Path("/tmp/mtelgon_tiles")

# ─── Field / date constants ────────────────────────────────────────────────────
ALL_FIELDS = [
    "MTELGON-B2","MTELGON-C1","MTELGON-M1A","MTELGON-M1B","MTELGON-M2",
    "MTELGON-M3","MTELGON-M4","MTELGON-M5",
    "MTELGON-T1","MTELGON-T2","MTELGON-T3","MTELGON-T4","MTELGON-T5",
    "MTELGON-T6","MTELGON-T7","MTELGON-T8","MTELGON-T9","MTELGON-T10","MTELGON-T11",
]

ALL_DATES = [
    "2024-06-27","2024-07-10","2024-10-18","2024-11-14","2024-12-23",
    "2025-03-19","2025-05-02","2025-06-25","2025-07-04","2025-07-23",
    "2025-08-06","2025-09-03","2025-10-01","2025-10-02","2025-11-08",
    "2025-12-08","2026-01-05","2026-03-06","2026-04-05","2026-05-04","2026-05-14",
]

LAYERS = ["ndvi", "ndre", "rgb"]

ZOOM_MIN = 14
ZOOM_MAX = 19

# ─── Colourmaps ───────────────────────────────────────────────────────────────
def make_rdylgn_colormap_file(path: Path):
    """256-entry RdYlGn table for NDVI [-1, 1] → uint8 0-255."""
    keypoints = [
        (0,   165,  0,  38),
        (32,  215, 48,  39),
        (64,  244,109,  67),
        (96,  253,174, 97),
        (128, 255,255, 191),
        (160, 217,239, 139),
        (192, 166,217, 106),
        (224, 102,189,  99),
        (255,   0, 104,  55),
    ]
    lines = ["nv 0 0 0 0\n"]  # nodata → transparent
    for i in range(256):
        r, g, b = _interp_colormap(i, keypoints)
        lines.append(f"{i} {r} {g} {b} 255\n")
    path.write_text("".join(lines))


def make_rdpu_colormap_file(path: Path):
    """256-entry RdPu table for NDRE [-1, 1] → uint8 0-255."""
    keypoints = [
        (0,   255, 247, 243),
        (64,  253, 224, 221),
        (128, 252, 146, 114),
        (192, 221,  52, 151),
        (255, 122,   1,  19),
    ]
    lines = ["nv 0 0 0 0\n"]
    for i in range(256):
        r, g, b = _interp_colormap(i, keypoints)
        lines.append(f"{i} {r} {g} {b} 255\n")
    path.write_text("".join(lines))


def _interp_colormap(v, keypoints):
    """Linear interpolation between keypoint colours."""
    if v <= keypoints[0][0]:
        return keypoints[0][1], keypoints[0][2], keypoints[0][3]
    if v >= keypoints[-1][0]:
        return keypoints[-1][1], keypoints[-1][2], keypoints[-1][3]
    for i in range(len(keypoints) - 1):
        v0, r0, g0, b0 = keypoints[i]
        v1, r1, g1, b1 = keypoints[i + 1]
        if v0 <= v <= v1:
            t = (v - v0) / (v1 - v0)
            return (
                int(r0 + t * (r1 - r0)),
                int(g0 + t * (g1 - g0)),
                int(b0 + t * (b1 - b0)),
            )
    return 128, 128, 128


# ─── Core tile job ────────────────────────────────────────────────────────────

def tile_dir(date: str, field: str, layer: str) -> Path:
    return TILES_BASE / date / field / layer


def run(cmd, check=True, capture=False):
    kw = dict(check=check)
    if capture:
        kw.update(capture_output=True, text=True)
    return subprocess.run(cmd, **kw)


def convert_float32_to_uint8(src: Path, dst: Path, layer: str, colormap_file: Path) -> bool:
    """
    Convert a Float32 COG (NDVI/NDRE, range -1..1) to RGBA uint8 PNG via:
      1. gdal_translate: scale -1..1 → 0..255 (uint8, one band)
      2. gdaldem color-relief: apply colormap → RGBA GeoTIFF
    Returns True on success.
    """
    tmp_uint8 = dst.parent / (src.stem + "_uint8.tif")
    try:
        # Step 1: rescale to uint8
        run([
            "gdal_translate",
            "-ot", "Byte",
            "-scale", "-1", "1", "0", "255",
            "-a_nodata", "none",          # clear nodata so NaN→0 transparently
            "-co", "COMPRESS=LZW",
            "-co", "TILED=YES",
            str(src), str(tmp_uint8),
        ])
        # Step 2: colour relief → RGBA GeoTIFF (4 bands, alpha on nodata)
        run([
            "gdaldem", "color-relief",
            str(tmp_uint8),
            str(colormap_file),
            str(dst),
            "-alpha",
            "-co", "COMPRESS=LZW",
            "-co", "TILED=YES",
        ])
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Conversion failed for {src}: {e}")
        return False
    finally:
        if tmp_uint8.exists():
            tmp_uint8.unlink()


def prepare_source(date: str, field: str, layer: str,
                   tmp_dir: Path,
                   ndvi_cmap: Path, ndre_cmap: Path) -> Path | None:
    """Return a ready-to-tile GeoTIFF path (converted if needed)."""
    
    # CHANGED: Instead of a hardcoded exact directory path lookup, we use rglob
    # to search for the specific filename dynamically anywhere inside the COG_BASE directory.
    fname = f"{date}_{field}_{layer.upper()}_COG.tif"
    matches = list(COG_BASE.rglob(fname))
    
    if not matches:
        logging.warning(f"COG missing: {fname} (Searched recursively inside {COG_BASE})")
        return None
    
    src = matches[0]  # Take the found path

    if layer == "rgb":
        # RGB COGs are already uint8 — use directly
        return src

    # Float32 NDVI/NDRE → uint8 + colormap
    cmap = ndvi_cmap if layer == "ndvi" else ndre_cmap
    dst = tmp_dir / f"{date}_{field}_{layer}_rgba.tif"
    if not convert_float32_to_uint8(src, dst, layer, cmap):
        return None
    return dst


def run_gdal2tiles(src: Path, out_dir: Path, zoom_min: int, zoom_max: int) -> bool:
    """Run gdal2tiles.py to produce XYZ PNGs."""
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        run([
            "gdal2tiles.py",
            "--profile=mercator",
            f"--zoom={zoom_min}-{zoom_max}",
            "--processes=1",       # we parallelise at job level
            "--tilesize=256",
            "--resampling=average",
            "--webviewer=none",    # skip HTML/JS output
            "--xyz",               # Google/Leaflet XYZ convention
            str(src),
            str(out_dir),
        ])
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"gdal2tiles failed for {src} → {out_dir}: {e}")
        return False


def process_job(job: dict) -> dict:
    """
    Worker function for a single (date, field, layer) combination.
    Returns a result dict.
    """
    date  = job["date"]
    field = job["field"]
    layer = job["layer"]
    dry   = job["dry_run"]

    out_dir = tile_dir(date, field, layer)
    # Skip if already done (sentinel: zoom dir exists and has tiles)
    sentinel = out_dir / str(ZOOM_MAX)
    if sentinel.exists() and any(sentinel.rglob("*.png")):
        return {"status": "skipped", "date": date, "field": field, "layer": layer}

    if dry:
        return {"status": "dry_run", "date": date, "field": field, "layer": layer}

    tmp_dir = TMP_BASE / f"{date}_{field}_{layer}_{os.getpid()}"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Write colourmaps into tmp dir (each worker writes its own copy)
    ndvi_cmap = tmp_dir / "ndvi_colormap.txt"
    ndre_cmap = tmp_dir / "ndre_colormap.txt"
    make_rdylgn_colormap_file(ndvi_cmap)
    make_rdpu_colormap_file(ndre_cmap)

    try:
        src = prepare_source(date, field, layer, tmp_dir, ndvi_cmap, ndre_cmap)
        if src is None:
            return {"status": "missing", "date": date, "field": field, "layer": layer}

        ok = run_gdal2tiles(src, out_dir, ZOOM_MIN, ZOOM_MAX)
        status = "done" if ok else "error"
        return {"status": status, "date": date, "field": field, "layer": layer}
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ─── Manifest ─────────────────────────────────────────────────────────────────

def write_manifest(results: list):
    """Write a JSON manifest of generated tiles for the dashboard."""
    manifest = {"generated_at": datetime.utcnow().isoformat() + "Z", "tiles": {}}
    for r in results:
        if r["status"] in ("done", "skipped"):
            key = f"{r['date']}/{r['field']}/{r['layer']}"
            manifest["tiles"][key] = True
    out = TILES_BASE / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2))
    logging.info(f"Manifest written → {out}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def build_jobs(filter_layer=None, filter_field=None, filter_date=None,
               dry_run=False) -> list:
    jobs = []
    
    # Scan the directory recursively for all .tif files
    # Filename format expected: {date}_{field}_{LAYER}_COG.tif
    all_tifs = COG_BASE.rglob("*.tif")
    
    for file_path in all_tifs:
        # Skip temporary files created by the script itself
        if "_rgba" in file_path.name or "_uint8" in file_path.name:
            continue
            
        stem = file_path.stem  # e.g., "2026-05-04_MTELGON-B2_NDVI_COG"
        parts = stem.split("_")
        
        # Ensure it matches our expected pattern before trying to parse
        if len(parts) < 4 or not parts[-1].count("COG"):
            continue
            
        date = parts[0]
        field = parts[1]
        layer = parts[2].lower() # Convert NDVI/NDRE/RGB to lowercase

        # Apply CLI filters if the user provided them
        if filter_date and date != filter_date:
            continue
        if filter_field and field != filter_field:
            continue
        if filter_layer and layer != filter_layer:
            continue

        jobs.append({
            "date": date, 
            "field": field, 
            "layer": layer,
            "dry_run": dry_run,
        })
        
    return jobs


def main():
    global ZOOM_MIN, ZOOM_MAX

    parser = argparse.ArgumentParser(description="Generate static map tiles from MTELGON COGs")
    parser.add_argument("--dry-run",   action="store_true", help="List jobs without executing")
    parser.add_argument("--layer",     help="Process only this layer (ndvi/ndre/rgb)")
    parser.add_argument("--field",     help="Process only this field (e.g. MTELGON-T4)")
    parser.add_argument("--date",      help="Process only this date (e.g. 2026-05-14)")
    parser.add_argument("--workers",   type=int, default=4,
                        help="Parallel worker processes (default 4)")
    parser.add_argument("--zoom-min",  type=int, default=ZOOM_MIN)
    parser.add_argument("--zoom-max",  type=int, default=ZOOM_MAX)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("/tmp/tile_generation.log"),
        ]
    )

    ZOOM_MIN = args.zoom_min
    ZOOM_MAX = args.zoom_max

    # This will now successfully evaluate without permission errors!
    TMP_BASE.mkdir(parents=True, exist_ok=True)
    TILES_BASE.mkdir(parents=True, exist_ok=True)

    jobs = build_jobs(
        filter_layer=args.layer,
        filter_field=args.field,
        filter_date=args.date,
        dry_run=args.dry_run,
    )

    total = len(jobs)
    logging.info(f"Jobs to process: {total}  (workers={args.workers}, zoom={ZOOM_MIN}-{ZOOM_MAX})")

    if args.dry_run:
        for j in jobs:
            print(f"  DRY  {j['date']}  {j['field']}  {j['layer']}")
        print(f"\nTotal: {total} jobs")
        return

    results = []
    done = skipped = errors = missing = 0

    with ProcessPoolExecutor(max_workers=args.workers) as exe:
        futures = {exe.submit(process_job, j): j for j in jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            try:
                r = fut.result()
            except Exception as e:
                j = futures[fut]
                r = {"status": "error", **j}
                logging.error(f"Job exception {j}: {e}")
            results.append(r)
            s = r["status"]
            if s == "done":    done    += 1
            elif s == "skipped": skipped += 1
            elif s == "missing": missing += 1
            else:              errors  += 1
            logging.info(f"[{i}/{total}] {s:8s}  {r['date']}  {r['field']}  {r['layer']}")

    write_manifest(results)

    print("\n─── Summary ───────────────────────────────")
    print(f"  Done:    {done}")
    print(f"  Skipped: {skipped}  (already existed)")
    print(f"  Missing: {missing}  (COG not found)")
    print(f"  Errors:  {errors}")
    print(f"  Total:   {total}")
    print(f"\nTiles directory: {TILES_BASE}")
    print(f"Log: /tmp/tile_generation.log")


if __name__ == "__main__":
    main()