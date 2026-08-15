# EV Systems — Study Notes
*Compiled from 3 days of notes, written for someone with no electrical engineering background*

---

## 0. The Big Picture: How Power Flows Through an EV

Think of an EV as having **three separate voltage "worlds"** that all talk to each other:

```
 1V – 12V            12V – 27V              27V – 800V
 ┌──────────┐        ┌──────────────┐       ┌─────────────────┐
 │ Sensor / │  <───   │ 12V Auxiliary│  <──   │ High-Voltage     │
 │ signal   │        │ Battery /    │        │ Traction Battery │
 │ level    │        │ control      │        │ (drives the car) │
 └──────────┘        │ circuits     │       └─────────────────┘
                      └──────────────┘
```

- **1V–12V** → tiny signal-level electronics (sensors, logic chips)
- **12V–27V** → the "12V system" familiar from normal cars (lights, infotainment, control units)
- **27V–800V** → the **high-voltage traction battery** that actually powers the motor

**Key rule of thumb:** the 12V auxiliary battery still exists in an EV — it powers the low-voltage control circuits (the "brain") even when the big traction battery is disconnected. It's charged from the main battery through a **DC-DC converter**.

### Core building blocks of the power system
| Block | What it does |
|---|---|
| **BMS** (Battery Management System) | The "brain" that monitors and protects the battery pack |
| **Battery Pack → Module → Cell** | The physical hierarchy of energy storage (see Section 2) |
| **DC Converter** | *Buck* = steps voltage **down**; *Boost* = steps voltage **up** |
| **On-board Charger (OBC)** | Converts AC from the wall into DC to charge the battery |
| **Regen (regenerative braking)** | Turns braking motion back into electricity |
| **EVSE** (Electric Vehicle Supply Equipment) | The charging station/wallbox — supplies AC (slow charging) |
| **EVCE / DC Fast Charger** | Supplies DC directly to the battery — much faster |
| **V2G / V2L** (Vehicle-to-Grid / Vehicle-to-Load) | Car can send power *back* — to the grid (stabilizes it) or to power external devices |

**Difference between an ICE car and an EV:** an ICE (internal combustion engine) car generates power by burning fuel on demand; an EV *stores* power chemically in a battery pack and draws it out electrically.

---

## 1. Cells → Modules → Battery Packs

This is the fundamental hierarchy of every EV battery:

```
   CELL  →  MODULE  →  BATTERY PACK
 (basic unit) (group of cells)  (group of modules)
```

A **cell** is the basic unit of an energy storage device:

```
      +  o──── (nominal voltage measured here)
   ┌──────┐
   │ CELL │
   └──────┘
      –  o
```

### Cell chemistries and their nominal voltages

| Chemistry | Nominal Voltage | Empty | Full | Notes |
|---|---|---|---|---|
| Lead Acid | 2V/cell | 1.8V | 2.4V | Electrolyte = sulphuric acid |
| Lithium-ion NMC (Nickel Manganese Cobalt) | 3.7V | 2.8V | 4.2V | **Highest energy density**; cobalt often sourced from Congo |
| Lithium Iron Phosphate (LFP / LiFePO₄) | 3.2V | 2.5V | 3.65V | Less thermal runaway risk — safer chemistry |
| Lithium Titanate (LTO) | 2.4V | — | — | |
| Sodium-ion | 1.5V–3.0V | — | — | More charge cycles, cheaper, less volatile; good for heavy/grid storage |

**Why this matters:** NMC packs more energy into less weight (great for range) but LFP is more thermally stable (safer, longer cycle life) — this is exactly the kind of trade-off relevant to choosing cells for a second-life storage product.

### Cell shapes/formats
- **Cylindrical** (e.g., the famous "18650" cell used by Tesla)
- **Prismatic** (rectangular, boxy)
- **Pouch** (flat, flexible — used by Nissan)

### Reading a cylindrical cell code, e.g. "18650"
```
 1 8 6 5 0
 └┬┘ └┬┘ 
  │   └── Length of cell in mm (65mm)
  └────── Diameter in mm (18mm)
```

---

## 2. Series vs Parallel — Why It Matters

This is one of the most important concepts to get intuitively:

| Wiring | What increases | What stays the same | Example |
|---|---|---|---|
| **Parallel** | Capacity (Ah) | Voltage | Two 2V, 20Ah cells in parallel → 2V, **40Ah** |
| **Series** | Voltage | Capacity (Ah) | Two 2V, 20Ah cells in series → **4V**, 20Ah |

```
PARALLEL (voltage same, capacity adds)     SERIES (voltage adds, capacity same)

 +──┬──+         2V, 20Ah cell            +────2V────+   +────2V────+
 │     │        (each)                    │  20Ah    ├───┤  20Ah    │
 +──┴──+          → combined: 2V, 40Ah    +──────────+   +──────────+
                                              → combined: 4V, 20Ah
```

**Energy stored is always the same either way** — energy (in watt-hours) doesn't care how you wire the cells:

> **Watt-hours (Wh) = Amp-hours (Ah) × Voltage (V)**

Both examples above give: 20Ah × 2V × 2 cells = **80 Wh**, whether wired in series or parallel.

### Worked example
A 12V, 70Ah battery powering a 60W bulb (drawing 5A):
- Watts ÷ Voltage = Current → 60W ÷ 12V = **5 Amps**
- Capacity test (discharging): multiply hours run × current drawn = Amp-hours delivered
- Total energy = Amp-hours × Voltage → e.g. 11Ah × 12V ≈ **132 Wh** *(units matter — always double check Ah vs mAh)*

---

## 3. Capacity, C-Rating, and Energy Density

### C-Rating — "how fast can this battery be charged/discharged safely?"
> **C-rating = Current drawn ÷ Capacity**

Example: a 100Ah battery being discharged at 10A → 10A ÷ 100Ah = **0.1C**

| Chemistry | Typical max continuous C-rate |
|---|---|
| Lead acid | ~0.2C |
| Lithium | ~0.5C |

Common naming:
- **C100** → slow discharge over 100 hours (e.g. lead-acid backup use)
- **C20** → standard discharge rate
- **C10** → solar/lead-acid applications

**Rule of thumb: high current draw = less usable capacity.** Batteries deliver less total energy when discharged very fast.

### Energy Density — "how much energy per kg / per litre?"
Two different measures:

> **Energy Density (gravimetric) = Energy (Wh) ÷ Weight (kg)**
> **Volumetric Density = Energy (Wh) ÷ Volume**

| Chemistry | Typical Energy Density |
|---|---|
| NMC | 150–250 Wh/kg |
| LFP (LiFePO₄) | 90–100 Wh/kg (lower, but safer/longer life) |

Worked examples from cell testing:
| Cell | Capacity | Voltage | Weight | Wh | Wh/kg |
|---|---|---|---|---|---|
| Cell A | 3000 mAh | 3.7V | 44.35g | 11.1 | 250 |
| Cell B | 7800 mAh | 3.7V | 30.56g | 28.86 | 810 |
| Cell C | 1600 mAh | 3.7V | 41.45g | 5.92 | 142 |

*(Note: Cell B's 810 Wh/kg is implausibly high for real lithium chemistry — a good example of why you sanity-check specs. Real NMC cells top out around 250–300 Wh/kg. Always double-check weight and mAh figures against the datasheet.)*

### Converting Ah using milliamps
> **Ah = mAh ÷ 1000 × Volts** *(be careful — this gives Wh, not Ah, if you multiply by volts! Keep units straight: mAh ÷ 1000 = Ah; Ah × V = Wh)*

---

## 4. Battery Safety: Thermal Runaway

```
 Loose connection → Overheating → Fire
```

**Thermal runaway** is the dangerous chain reaction inside a lithium cell:

```
 Raised temperature
        │
        ▼
 Cell becomes more chemically reactive
        │
        ▼
 More heat generated
        │
        ▼
 Even more heat  ──── (self-reinforcing/cascading) ──── FIRE
```

This is why LFP chemistry (less prone to thermal runaway) is often chosen over NMC for stationary/safety-critical storage, even though it has lower energy density.

Other safety concepts:
- **High-voltage leakage / isolation testing** — checking that HV circuits are properly insulated from the vehicle chassis (V=IR, so leakage current reveals a breakdown in isolation)
- **DTC** (Diagnostic Trouble Code) — fault codes reported by the BMS
- **Interlock check** — inspect for loose connections on high-voltage circuits before working on them

---

## 5. Motors — How the Car Actually Moves

### Two main motor types

**1. Permanent Magnet Motor**
- Uses **neodymium** permanent magnets + stator coils
- Simple, efficient, common in EVs

**2. Induction Motor (Rotor-based)**
- Feed AC current → creates a rotating magnetic field → induces current in the rotor → rotor spins
- Used by Tesla (some models)

### The basic motor principle
```
  Magnet
   ╭───╮
   │   │  ← wire coil moves through magnetic field
   ╰─◡─╯
  ~~~~~~   (coil)
```
Moving a coil through a magnetic field induces current (or, run in reverse, running current through a coil in a magnetic field creates motion — this reversibility is *why regen braking works*).

### How power flows to the motor
```
 Traction Battery (HV, DC) ──> Inverter (DC → AC) ──> Motor (spins) ──> Wheels
```
- **Inverter**: converts DC (battery) to AC (motor needs AC to create a rotating field)
- **Auxiliary battery (12V)**: separately powers the low-voltage control circuit that manages all of this

### Regenerative Braking (Regen)
```
 Car's motion (kinetic energy)
        │
        ▼
 Wheels spin the motor (now acting as a generator)
        │
        ▼
 Motor's magnets spinning past coils ──> generates electricity
        │
        ▼
 Electricity flows back into the traction battery
```
This is the same physics as the coil/magnet diagram above — just running the motor "backwards" as a generator instead of a motor.

---

## 6. Electrical Formulas You'll Actually Use

| Formula | Meaning |
|---|---|
| **V = IR** | Voltage = Current × Resistance (Ohm's Law) |
| **I = V/R** | Current = Voltage ÷ Resistance |
| **Power = VI** | Power = Voltage × Current |
| **Power = I²R** | Power = Current² × Resistance |
| **Power = V²/R** | Power = Voltage² ÷ Resistance |
| **Energy = Power × Time** | Watt-hours = Watts × Hours |

### Resistors in circuits
```
 SERIES (resistance adds)          PARALLEL (resistance combines differently)

 ──[R1]──[R2]──                     ──┬──[R1]──┬──
   Total = R1 + R2                    └──[R2]──┘
                                    1/Rtotal = 1/R1 + 1/R2
                                    or: Rtotal = (R1×R2)/(R1+R2)
```
*Note: this is the opposite pattern from batteries! Resistors in series **add**; resistors in parallel **combine to something smaller**. Batteries in parallel add capacity; batteries in series add voltage. Don't mix these up.*

### Capacitors (opposite pattern from resistors!)
A capacitor stores energy as electric charge between two plates:
```
   ┌─────────────┐
   │ + + + + + + │  ← charged plate
   │─────────────│
   │             │  ← opposite plate
   └─────────────┘
```
| Wiring | Formula |
|---|---|
| Parallel | C_total = C1 + C2 |
| Series | C_total = (C1 × C2) / (C1 + C2) |

*(Capacitors follow the resistor pattern, not the battery pattern — parallel adds directly, series uses the product-over-sum formula.)*

---

## 7. Communication Protocols in EVs

The BMS, motor controller, and other electronic systems all need to talk to each other:

- **CAN** (Controller Area Network) — the classic automotive communication bus
- **Modbus** — common in solar/industrial systems
- **Ethernet**
- **Wireless**
- **Bluetooth**

---

## 8. Battery Aging & Degradation

Batteries wear out in two distinct ways:

| Type | Cause |
|---|---|
| **Calendar Aging** | Just from *storage* over time — worsened by high temperature and high state of charge |
| **Cyclic Aging** | From repeated charge/discharge cycles |

### Mechanisms behind aging
- **Lithium plating** — lithium metal forms a coating on the electrode instead of intercalating properly, reducing usable capacity
- **SEI Growth** (Solid Electrolyte Interphase) — a layer builds up inside the cell, increasing internal resistance over time

### Battery lifecycle stages (capacity-based)
```
 100% ──────── 80% ──────── 60% ──────── below 60%
   │             │             │              │
 New battery   1st life ends  2nd life ends  Recycling
              (5–8 yrs, EV use)  (5–10 yrs,
                                  stationary storage)
```

- **100–80% SoH**: First life — used in the EV itself (needs SoH >80% for automotive performance)
- **80–60% SoH**: Second life — repurposed for stationary applications (e.g., Battery Energy Storage Systems / BEDS, solar storage)
- **<60% SoH**: End of life — recycling

**This second-life window (80–60% SoH) is exactly the space where repurposed EV batteries for solar cold storage systems operate.**

---

## 9. Battery Assessment Process (10 Steps)

When evaluating a used/second-life battery, the standard process is:

1. **Receive battery & document review** — mileage, ID, recalls, BMS data logs
2. **Visual inspection**
3. **Voltage measurement**
4. **Insulation testing** — checking for voltage leakage
5. **Capacity testing**
6. **Internal resistance testing** *(lower internal resistance = better cell)*
7. **Temperature monitoring**
8. **Cell balancing** — checking cell-to-cell voltage variance (target: <30mV difference)
9. **BMS diagnostics**
10. **State of Health (SoH) assessment**

### Key formula: State of Health
> **SoH (%) = (Current Capacity ÷ Rated Capacity) × 100**

### Watch-outs during capacity testing
- **Deep discharge**, **cell imbalance**, and **cell failure** are the main risks
- Typical test discharge rates: **1C** (1 hour) or **⅓C** (3 hours)

### Battery assessment outcome → Residual Value
The whole point of the 10-step process is to determine what the battery is actually worth for reuse — its **residual value**.

---

## 10. Battery Circularity — The Full Lifecycle

```
1. Raw Material          2. Battery           3. Battery
   Extraction      ──>      Manufacturing ──>     Integration
   (mining)                 (cell production,     (installation,
                             pack assembly,        connection,
                             quality control)      calibration)
        │                                               │
        ▼                                               ▼
9. Manufacturing                                  4. Vehicle
   of new batteries                                  Operation
        ▲                                               │
        │                                               ▼
8. Recovery of raw    <──  7. Recycling   <──    5. Battery Assessment
   materials              (WEEE Centre,                 │
                            EnviroServe)                 ▼
                                ▲                  6. 2nd Life Application
                                └──────────────────  (Energy Storage,
                                                       5–10 years)
```

### Where raw materials come from
| Material | Main source region |
|---|---|
| Lithium | South America, Australia |
| Cobalt | Congo |
| Nickel | Sulphide ores |
| Graphite | China |

### Three circularity strategies (in order of preference — most value retained first)
1. **Reuse** — use as-is
2. **Repurpose** — give it a second life in a different application (e.g., stationary storage)
3. **Recycle** — recover raw materials when the battery is no longer usable at all

### End-of-life signals
- **Capacity loss** below 80%
- **Increased internal resistance** (>150% of original)
- **Safety concerns** (leakage)
- Manufacturer recommendations

---

## Quick-Reference Formula Sheet

| Concept | Formula |
|---|---|
| Ohm's Law | V = IR |
| Power | P = VI = I²R = V²/R |
| Energy | Wh = Power(W) × Time(h) |
| Battery energy | Wh = Ah × V |
| C-rating | C = Current drawn ÷ Capacity (Ah) |
| Energy density (gravimetric) | Wh ÷ kg |
| Energy density (volumetric) | Wh ÷ volume |
| State of Health | SoH% = (Current Capacity ÷ Rated Capacity) × 100 |
| Resistors in series | R_total = R1 + R2 |
| Resistors in parallel | R_total = (R1×R2)/(R1+R2) |
| Capacitors in parallel | C_total = C1 + C2 |
| Capacitors in series | C_total = (C1×C2)/(C1+C2) |
| Batteries in series | Voltage adds, capacity (Ah) stays same |
| Batteries in parallel | Capacity (Ah) adds, voltage stays same |

---

## The One-Page Mental Model

If you remember nothing else, remember this:

1. **Energy is stored in cells → grouped into modules → grouped into packs.**
2. **Series wiring adds voltage; parallel wiring adds capacity — but total stored energy (Wh) is the same either way.**
3. **The BMS is the brain** — protecting against thermal runaway, imbalance, and monitoring health.
4. **The battery ages** through calendar aging (storage) and cyclic aging (use) — tracked via State of Health.
5. **A battery's life doesn't end at 80% SoH** — it just moves from powering a vehicle to a second-life stationary application, and only gets recycled once it drops below ~60%.
