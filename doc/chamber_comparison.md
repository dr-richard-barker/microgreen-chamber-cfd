# Spaceflight Plant Growth Chamber Aerodynamic Comparison: Microgreen vs. VEGGIE vs. APH

Reference engineering specification and CFD modeling comparison across three spaceflight and controlled-environment plant growth chambers:
1. **Microgreen Chamber** (Barker Lab / AIRI baseline)
2. **VEGGIE / VPS** (NASA Vegetable Production System; Massa et al., 2017)
3. **APH** (NASA Advanced Plant Habitat; Morrow et al., 2016 ICES-2016-320)

---

## 1. Executive Summary

| Feature | Microgreen Chamber | VEGGIE (VPS) | APH |
|:---|:---|:---|:---|
| **Role / Class** | Compact phenotyping / educational | Space crop garden (semi-open) | Research-grade phytotron (closed-loop) |
| **Enclosure Type** | Sealed box with curved parabolic hood | Flexible transparent FEP bellows | Rigid sealed carbon-fiber composite |
| **Growth Area** | 0.0224 m² (120 × 186.7 mm) | 0.1075 m² (292 × 368 mm) | 0.1708 m² (454 × 408 mm effective) |
| **Usable Canopy Volume** | 2.33 L (max height 96.7 mm) | 37.6 L – 45.0 L (at 350 mm bellows) | 83.4 L shoot volume (450 mm clear height) |
| **Total Enclosure Volume** | 2.33 L | ~40.6 L (including pillows) | 92.8 L (shoot + root zone) |
| **Root Zone Module** | Flush bottom tray (25 mm) | 6x arcillite plant pillows (40 mm) | 4-quadrant Science Carrier (51 mm) |
| **Airflow Driver** | 1x Sunon MF50100V2 axial blower | 1x Top centrifugal suction fan | 2x Lateral ECS recirculation blowers |
| **Inlet / Outlet Path** | Ø40 mm inlet port → Ø40 mm outlet | 4x Base perimeter slots → top exhaust | 2x Lower lateral slots → 4x ceiling perimeter |
| **Bulk Velocity Target** | ~0.26 m/s (11.8 m³/h operating point) | Variable (Low / High settings) | 0.3 – 1.5 m/s (software-regulated, 0.1 m/s step) |
| **Environmental Control** | None (ambient laboratory) | ISS cabin-dependent | Full automated control (T, RH, CO₂, C₂H₄) |
| **Cabin Interface** | Independent / sealed | Direct open mass/thermal exchange | Express Rack quad-locker closed loop |

---

## 2. Airflow Architecture & Topology

```
A. Microgreen Chamber (Through-flow Jet)
    [Inlet Ø40mm] ───> Confined Jet ───> Wall impingement / Recirculation ───> [Outlet Ø40mm]
    - Dominant mode: Unsteady flapping jet over short tray (186.7 mm depth)

B. VEGGIE (Bottom-up Suction)
    [ISS Cabin Air] ───> [4x Base Slots] ───> Upward canopy wash ───> [Top Fan Exhaust] ───> [Cabin]
    - Dominant mode: Upward forced draft driven by top suction; open to cabin humidity/CO2

C. APH (Opposing Cross-flow & Upward Sweep)
    [Left ECS Slot]  ───> [Diffuser] ──┐
                                       ├──> Collision & Upward Sweep ───> [Ceiling Exhausts] ───> [ECS Loop]
    [Right ECS Slot] ───> [Diffuser] ──┘
    - Dominant mode: Symmetrical opposing wall jets meeting over Science Carrier, rising through canopy
```

---

## 3. Environmental & Boundary Condition Comparison

| Environmental Parameter | Microgreen Chamber | VEGGIE (Massa et al., 2017) | APH (Morrow et al., 2016) |
|:---|:---|:---|:---|
| **Air Temperature ($T$)** | Ambient lab (~20–22°C) | ISS Cabin + 1.5–3.0°C (~22–26°C) | 18.0°C to 30.0°C (±0.5°C) |
| **Relative Humidity ($RH$)** | Ambient (30–60%) | 65%–85%+ (cabin exchange) | 50% to 90% (±3–5% active control) |
| **$CO_2$ Concentration** | Ambient (~420 ppm) | ISS Cabin (~2800–4000 ppm) | 400 to 5,000 ppm (±50 ppm) |
| **Ethylene ($C_2H_4$)** | Uncontrolled | ISS Cabin levels (~20–50 ppb) | Catalytic scrubbing to ≤ 25 ppb |
| **Lighting Heat Load** | Top LED board (~38.4 W) | Overhead LED cap (RGB, 200–450 µmol/m²/s) | 5-channel GLA LED (0–1000 µmol/m²/s, liquid cooled) |
| **Thermal Boundary Condition** | Conjugate / heat flux on hood | Sensible heat rejection to cabin | Liquid coldplate to ISS Moderate Temp Loop (MTL) |

---

## 4. CFD Physical Regimes & Richardson Number Framework

The comparative gravity study evaluates the transition from mixed buoyancy-driven convection on Earth ($1\text{ g}$) to purely forced convection in microgravity ($0\text{ g}$).

The governing dimensionless group is the **Richardson Number ($Ri$)**:
$$Ri = \frac{Gr}{Re^2} = \frac{g \beta \Delta T L}{U_{ref}^2}$$

| Regime | $Ri$ Condition | Physical Interpretation | Spaceflight Consequence |
|:---|:---|:---|:---|
| **Forced Convection** | $Ri \ll 0.1$ | Momentum/fan dominates; buoyancy negligible | Microgravity ($\mu\text{g}$) nominal operating state |
| **Mixed Convection** | $0.1 \le Ri \le 10$ | Fan and buoyancy compete; strong plume interaction | Earth ($1\text{ g}$) baseline and fractional gravity |
| **Natural Convection** | $Ri \gg 10$ | Buoyancy dominates; stagnant pockets if fans off | Ground-test unventilated failure mode |

### Chamber-Specific Regime Mapping:
1. **Microgreen Chamber ($1\text{ g}$):** Stable ceiling thermal stratification ($LED$ at top) acts to *suppress* vertical mixing, making $0\text{ g}$ better mixed than $1\text{ g}$.
2. **VEGGIE ($1\text{ g}$ vs $0\text{ g}$):** In $1\text{ g}$, warm air rises toward top fan (aligned with buoyancy). In $0\text{ g}$, natural convection vanishes, causing leaf boundary layer resistance ($r_a$) to rise unless high fan speed is engaged (preventing fungal infection).
3. **APH ($1\text{ g}$ vs $0\text{ g}$):** High forced velocity ($0.3–1.5\text{ m/s}$) keeps $Ri \ll 1$ throughout the chamber, suppressing thermal stratification across the 4 quadrants.

---

## 5. References

1. **Massa, G.D., et al. (2017)**. "VEG-01: Veggie Hardware Validation Testing on the International Space Station". *Open Agriculture*, 2(1): 33–41. DOI: [10.1515/opag-2017-0003](https://doi.org/10.1515/opag-2017-0003)
2. **Morrow, R.C., et al. (2016)**. "A New Plant Habitat Facility for the ISS". *46th International Conference on Environmental Systems*, ICES-2016-320.
3. **Monje, O., et al. (2019)**. "Hardware Validation of the Advanced Plant Habitat on ISS". *49th International Conference on Environmental Systems*, ICES-2019-247.
4. **Ewald, H. & Barker, R. (2026)**. *Microgreen Chamber CFD Specification and Solver Framework (OpenFOAM v2606)*.
