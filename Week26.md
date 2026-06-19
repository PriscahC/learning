
# What I Learned This Week

## Multi-Node Infrastructure (Tailscale, RustDesk, WSL2)
- Set up a Tailscale mesh network across multiple Windows and Linux machines to enable secure remote access without exposing ports publicly.
- Configured RustDesk as a remote desktop fallback alongside TeamViewer for cross-machine control.
- Worked through WSL2 quirks when bridging Windows-native tools with Linux-based processing workflows.
- Diagnosed GPU compatibility issues on a node lacking an NVIDIA GPU — confirmed which workflows require CUDA acceleration vs. which can fall back to CPU-only processing, and how that affects task distribution across nodes.

## Drone Photogrammetry Pipeline
- Continued refining automation for DJI Terra processing using scripted UI automation (PyAutoGUI/pywinauto) to reduce manual steps in flight data processing.
- Tested running photogrammetry workflows across multiple machines, learning how to route jobs to nodes based on available hardware (GPU vs. non-GPU).

## eTIMS (KRA) API Integration
- Began integrating Kenya's eTIMS API into an Elixir-based project — learned the authentication and request structure required for tax compliance integrations in Elixir, and how to structure HTTP client modules for third-party government APIs.

## General Takeaways
- Distributing compute-heavy geospatial workflows across heterogeneous hardware (GPU/non-GPU nodes) requires explicit job routing logic rather than assuming uniform capability.
- Remote infrastructure tooling (Tailscale + RustDesk) significantly simplifies managing a small multi-machine setup without needing a full VPN/server stack.


