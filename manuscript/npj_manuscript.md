# Aerodynamic Boundary-Layer Scaling and Enclosure Regimes Across Spaceflight Plant Growth Hardware: A Multi-Chamber OpenFOAM CFD Framework under Variable Gravity

**Richard Barker$^{1,*}$, Henry Ewald$^{1}$, and Astrobotany Consortium$^{1}$**

$^{1}$Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN 47907, USA  
$^*$Corresponding author: `rbarker@purdue.edu`

---

## Abstract

Plants cultivated in extraterrestrial habitats encounter a physical environment devoid of natural gravity-driven buoyancy ($Gr \to 0$), expanding unstirred fluid boundary layers around vegetative canopies and drastically elevating aerodynamic resistance ($r_a = 1/g_{bl}$). Here, we present a systematic, multi-chamber 3D computational fluid dynamics (CFD) investigation comparing four distinct spaceflight and controlled-environment agricultural hardware architectures across four gravitational regimes: Earth ($1.0\text{ g}$), Mars ($0.38\text{ g}$), Moon ($0.166\text{ g}$), and Microgravity ($0\text{ g}$). Using an OpenFOAM v2606 finite-volume framework with conformal multi-solid analytic geometries, we model: (i) the compact **Microgreen Chamber** ($2.33\text{ L}$, through-flow confined jet), (ii) the **NASA Vegetable Production System (VEGGIE/VPS)** ($37.6\text{ L}$, top suction with passive cabin air induction), (iii) the **NASA Advanced Plant Habitat (APH)** ($83.4\text{ L}$, ducted closed-loop opposing cross-flow), and (iv) the **NASA Space Shuttle CHROMEX / Plant Growth Unit (PGU/PGC)** ($49.57\text{ L}$ macro chassis, $0.866\text{ L}$ canisters with Brinkman-Darcy rooting foam). Parametric gravity sweeps reveal that ceiling-mounted LED arrays induce stable thermal stratification on Earth ($Ri \approx 0.14 - 1.55$), which suppresses vertical exchange; in microgravity, this stratification collapses, rendering purely forced convection ($Ri = 0$) superior in turbulent kinetic energy. In VEGGIE, low-fan microgravity operation leads to a critical $52.8\%$ canopy stagnation volume ($g_{bl} = 0.219\text{ mol m}^{-2}\text{s}^{-1}$), elevating fungal mold vulnerability. In CHROMEX sealed canisters, pure diffusion ($Pe < 1$) drives root-zone hypoxia ($O_2 < 5\%$) within 35 minutes, providing a biophysical basis for historical flight transcriptomic alcohol dehydrogenase ($ADH$) upregulation. Transient fan-stoppage tests reveal that on Earth, natural buoyancy maintains a basal conductance floor ($g_{bl} \approx 0.36\text{ mol m}^{-2}\text{s}^{-1}$), whereas in microgravity, total aerodynamic collapse suffocates the canopy within 3.5–8.9 minutes. Conversely, APH maintains invariant $g_{bl} \approx 1.07\text{ mol m}^{-2}\text{s}^{-1}$ across all gravities. Analysis of suspended bioaerosols establishes a fundamental biosecurity trade-off: VEGGIE exports $100\%$ of aerosolized fungal spores directly into astronaut living quarters ($t_{50} = 13.8\text{ s}$), whereas APH achieves rapid internal HEPA scrubbing ($t_{50} = 18.4\text{ s}$) with zero cabin burden. These findings establish quantitative aerodynamic criteria for designing next-generation bioregenerative life support systems for Lunar and Martian surface missions.

---

## 1. Introduction & Biophysical Foundations

### 1.1 Opportunities and Imperatives of Space Agriculture
As human space exploration transitions from low-Earth orbit (LEO) sorties toward sustained surface outposts on the Moon (NASA Artemis Base Camp) and multi-year transits to Mars, biological life support systems become indispensable. Physical-chemical resupply paradigms become logistically prohibitive across deep-space distances. Higher plants provide essential multi-functional life support: they convert metabolic carbon dioxide into breathable oxygen via photosynthetic photolysis, produce purified potable water through transpirational distillation, recycle nitrogenous and mineral waste from sanitized organic effluent, and synthesize fresh secondary nutrients (including carotenoids, potassium, vitamin C, and polyphenols) that degrade rapidly in pre-packaged freeze-dried rations. Furthermore, interactive horticultural engagement delivers profound behavioral and psychological countermeasures against the sensory monotony and confinement of deep-space habitats.

### 1.2 The Microgravity Fluid Challenge & Buoyancy Cessation
Despite these compelling opportunities, cultivating crops in extraterrestrial environments confronts a severe, fundamental physical impediment: the reduction or total absence of gravity-driven natural convection. On Earth ($1.0\text{ g}$), temperature differences between warm sunlit or LED-illuminated foliage and the cooler surrounding atmosphere generate spontaneous density gradients (Rayleigh-Bénard buoyancy, $Gr > 10^7$). This buoyant updraft continuously strips the unstirred laminar boundary layer adhering to leaf surfaces, facilitating rapid diffusive exchange of $CO_2$ and $H_2O$ vapor. In microgravity ($0\text{ g}$), the gravitational acceleration vector vanishes ($g \to 0$), causing the Grashof number ($Gr = g \beta \Delta T L^3 / \nu^2$) and Rayleigh number ($Ra = Gr \cdot Pr$) to drop to identically zero.

### 1.3 Fractional Gravity on the Moon ($0.166\text{ g}$) and Mars ($0.38\text{ g}$)
On the Lunar surface ($g = 1.62\text{ m/s}^2$) and Martian surface ($g = 3.72\text{ m/s}^2$), fractional gravitational fields restore a partial buoyant convective capability ($Gr_{Moon} \approx 16.5\% Gr_{Earth}$; $Gr_{Mars} \approx 37.9\% Gr_{Earth}$). However, as established by our Richardson scaling analysis ($Ri = Gr / Re^2$), this fractional buoyancy remains inadequate to strip thick boundary layers without active forced ventilation. Unless engineered ventilation is precisely tailored, lunar and martian greenhouses will operate in an unstable mixed-convection regime prone to thermal stratification and localized suffocation pockets.

### 1.4 Photosynthetic Suppression & Photorespiratory Waste (RuBisCO Kinetics)
The thickening of unstirred fluid boundary layers directly impairs photosynthetic efficiency through the Farquhar-von Caemmerer-Berry (FvCB) biochemical model. The net photosynthetic assimilation rate ($A_{net}$) is governed by the chloroplastic $CO_2$ concentration ($C_c$):
$$A_{net} = \left(1 - \frac{\Gamma^*}{C_c}\right) \min(W_c, W_j, W_p) - R_d$$
where $\Gamma^*$ is the $CO_2$ compensation point, $W_c$ is RuBisCO-limited carboxylation, and $W_j$ is electron transport-limited RuBP regeneration. When aerodynamic boundary-layer resistance ($r_a = 1/g_{bl}$) expands, the concentration drop between the bulk canopy atmosphere ($C_a$) and leaf intercellular airspaces ($C_i$) widens dramatically: $C_i = C_a - A_{net}(r_a + r_s)$. Under depleted intercellular $CO_2$ ($C_i < 150\text{ ppm}$), the oxygenation reaction catalyzed by RuBisCO increases exponentially relative to carboxylation ($v_o / v_c = 2\Gamma^* / C_i$), shunting energy into the photorespiratory glycolate pathway. This wasteful oxygenation can consume over $40\%$ of photosynthetic ATP and NADPH, drastically suppressing biomass yield.

### 1.5 Guttation, Boundary-Layer Humidity Saturation, and Pathogen Epidemics
In tandem with carbon starvation, thick boundary layers trap transpired water vapor, elevating local boundary layer relative humidity ($RH > 95\%$). This suppresses transpirational evaporative cooling (causing leaf thermal stress) and abolishes the transpirational pull required for xylem mineral transport (inducing calcium deficiency and physiological tipburn). To relieve positive root hydrostatic pressure, plants undergo hyper-guttation, exuding nutrient-rich liquid droplets along hydathodes. In microgravity, surface tension pins these unevaporated droplets to leaf margins, creating ideal microclimatic incubators for phytopathogenic fungal spore germination (such as *Fusarium oxysporum* and *Botrytis cinerea*).

---

## 2. Hardware Architecture & Dimensional Specifications

| Parameter | Microgreen Chamber | VEGGIE (VPS) | Advanced Plant Habitat (APH) | CHROMEX (PGU / PGC) |
|:---|:---|:---|:---|:---|
| **Payload Classification** | Benchtop Phenotyping | Deployable Space Garden | Closed-Loop Research Phytotron | Shuttle Middeck Locker Replacement |
| **Enclosure Structure** | Rigid acrylic + hood | Collapsible FEP bellows | Carbon-fiber composite | Middeck chassis + 6 Lexan PGCs |
| **Growth Footprint ($A$)** | $0.0224\text{ m}^2$ ($120 \times 187\text{ mm}$) | $0.1075\text{ m}^2$ ($292 \times 368\text{ mm}$) | $0.1708\text{ m}^2$ ($454 \times 408\text{ mm}$) | $0.0274\text{ m}^2$ (6× $95 \times 48\text{ mm}$) |
| **Canopy Air Volume ($V_{air}$)** | $2.33\text{ L}$ | $37.61\text{ L}$ (nominal) | $83.36\text{ L}$ (shoot zone) | $4.10\text{ L}$ total ($0.684\text{ L}$ / PGC) |
| **Total Growth Height** | $96.7\text{ mm}$ (to hood) | $350.0\text{ mm}$ (nominal height) | $450.0\text{ mm}$ (clear shoot zone) | $190.0\text{ mm}$ (canister height) |
| **Primary Flow Driver** | 1$\times$ Axial Fan ($\varnothing40\text{ mm}$) | 1$\times$ Top Suction Fan ($\varnothing50\text{ mm}$) | 2$\times$ Symmetric ECS Blowers | PGU chassis fan + PGC needle AES |
| **Airflow Topology** | Through-flow confined jet | Bottom-up forced suction | Opposing cross-flow sweep | Creeping percolation / Pure diffusion |
| **Nominal Flow Rate ($Q$)** | $11.8\text{ m}^3/\text{h}$ ($3.27\text{ L/s}$) | $85.0\text{ m}^3/\text{h}$ ($23.61\text{ L/s}$) | $26.4\text{ m}^3/\text{h}$ ($7.34\text{ L/s}$) | $0.001\text{ m}^3/\text{h}$ ($1.0\text{ L/h}$ AES) |
| **Canopy Forced Velocity** | $0.262\text{ m/s}$ (bulk mean) | $0.150\text{ m/s}$ (mean draft) | $0.300 - 1.500\text{ m/s}$ (regulated) | $0.001 - 0.010\text{ m/s}$ ($\text{Re} \ll 100$) |
| **Air Exchange Rate ($\text{ACH}$)** | $5,051\text{ h}^{-1}$ ($\tau = 0.71\text{ s}$) | $2,260\text{ h}^{-1}$ ($\tau = 1.60\text{ s}$) | $317\text{ h}^{-1}$ ($\tau = 11.35\text{ s}$) | $1.16\text{ h}^{-1}$ (AES $\tau = 51.9\text{ min}$) |
| **Environmental Control** | Ambient laboratory | Cabin-coupled ($\Delta T = +2^\circ\text{C}$) | Closed loop (±0.5°C, ±5% RH) | PGU lamp cooling / optional AES |
| **Cabin Interface Coupling** | Sealed phenotyping unit | Open continuous exchange | Closed EXPRESS Rack payload | Shuttle Middeck Locker Replacement |

---

## 3. Results & Discussion

### 3.1 Gravity Scaling & the Richardson Number Trajectory

| Chamber | Gravity Regime | $g\text{ (m/s}^2\text{)}$ | $Gr$ | $Re$ | $Ri\text{ } (Gr/Re^2)$ | Convective Regime | Dominant Aerodynamic Mechanism |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **Microgreen** | Earth ($1.0\text{ g}$) | $9.81$ | $3.87 \times 10^{5}$ | $1,669$ | $0.1405$ | Mixed Convection | Confined jet + ceiling thermal stratification |
| | Mars ($0.38\text{ g}$) | $3.72$ | $1.47 \times 10^{5}$ | $1,669$ | $0.0533$ | Forced-Dominated | Jet momentum dominates; weak stratification |
| | Moon ($0.166\text{ g}$) | $1.62$ | $6.39 \times 10^{4}$ | $1,669$ | $0.0232$ | Forced-Dominated | Buoyancy negligible; forward jet core |
| | Microgravity ($0\text{ g}$) | $0.00$ | $0.00$ | $1,669$ | $0.0000$ | Purely Forced | Flapping confined jet; unstratified canopy |
| **VEGGIE** | Earth ($1.0\text{ g}$) | $9.81$ | $1.83 \times 10^{7}$ | $3,463$ | $1.5511$ | Mixed (Buoyant) | Thermal plume assists upward chimney draft |
| | Mars ($0.38\text{ g}$) | $3.72$ | $6.95 \times 10^{6}$ | $3,463$ | $0.5880$ | Mixed (Transitional) | Weak plume; fan suction required for draw |
| | Moon ($0.166\text{ g}$) | $1.62$ | $3.03 \times 10^{6}$ | $3,463$ | $0.2561$ | Forced-Dominated | Low draft velocity; mold risk at low fan |
| | Microgravity ($0\text{ g}$) | $0.00$ | $0.00$ | $3,463$ | $0.0000$ | Purely Forced | Unstirred boundary layer without high fan |
| **APH** | Earth ($1.0\text{ g}$) | $9.81$ | $3.90 \times 10^{7}$ | $17,810$ | $0.1246$ | Forced-Dominated | Dual opposing cross-jets suppress plume |
| | Mars ($0.38\text{ g}$) | $3.72$ | $1.48 \times 10^{7}$ | $17,810$ | $0.0473$ | Strongly Forced | Piston-like upward sweep across shoot zone |
| | Moon ($0.166\text{ g}$) | $1.62$ | $6.44 \times 10^{6}$ | $17,810$ | $0.0206$ | Strongly Forced | Uniform boundary layer across Science Carrier |
| | Microgravity ($0\text{ g}$) | $0.00$ | $0.00$ | $17,810$ | $0.0000$ | Purely Forced | Fully engineered forced recirculation sweep |
| **CHROMEX PGC** | Earth ($1.0\text{ g}$) | $9.81$ | $1.98 \times 10^{6}$ | $123$ | $131.29$ | Buoyant Creeping | Creeping laminar jet; natural convection dominates |
| | Microgravity ($0\text{ g}$) | $0.00$ | $0.00$ | $123$ | $0.0000$ | Purely Creeping | Darcy percolation / pure diffusion ($Pe < 1$) |

### 3.2 Canopy Aerodynamic Conductance ($g_{bl}$) & Stagnation Risk

| Hardware | Gravity | Operating Mode | $\overline{U}_{canopy}\text{ (m/s)}$ | $\text{TKE}\text{ (m}^2/\text{s}^2\text{)}$ | $\delta_{bl}\text{ (mm)}$ | $Sh_{CO2}$ | $g_{bl}\text{ (mol m}^{-2}\text{s}^{-1}\text{)}$ | Stagnant Vol. ($\%$) |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **Microgreen** | $1.0\text{ g}$ | Baseline | $0.262$ | $4.82 \times 10^{-3}$ | $2.41$ | $28.4$ | $0.724$ | $14.2\%$ |
| | $0.0\text{ g}$ | Microgravity | $0.262$ | $4.40 \times 10^{-3}$ | $2.54$ | $27.0$ | $0.688$ | $9.6\%$ |
| **VEGGIE** | $1.0\text{ g}$ | Low Fan | $0.065$ | $1.12 \times 10^{-3}$ | $4.82$ | $14.2$ | $0.362$ | $32.4\%$ |
| | $1.0\text{ g}$ | High Fan | $0.150$ | $3.45 \times 10^{-3}$ | $3.18$ | $21.6$ | $0.551$ | $11.2\%$ |
| | $0.0\text{ g}$ | Low Fan | $0.065$ | $0.68 \times 10^{-3}$ | $7.95$ | $8.6$ | **$0.219$ (Bottleneck)** | **$52.8\%$ (Severe Risk)** |
| | $0.0\text{ g}$ | High Fan | $0.150$ | $3.02 \times 10^{-3}$ | $3.40$ | $20.2$ | $0.515$ | $15.4\%$ |
| **APH** | $1.0\text{ g}$ | Nominal ($0.6\text{ m/s}$) | $0.600$ | $1.24 \times 10^{-2}$ | $1.58$ | $43.2$ | $1.102$ | $2.1\%$ |
| | $0.0\text{ g}$ | Nominal ($0.6\text{ m/s}$) | $0.600$ | $1.19 \times 10^{-2}$ | $1.63$ | $42.0$ | $1.071$ | $2.6\%$ |
| | $0.0\text{ g}$ | High ($1.5\text{ m/s}$) | $1.500$ | $3.65 \times 10^{-2}$ | $0.98$ | $68.4$ | $1.745$ | $0.4\%$ |
| **CHROMEX** | $0.0\text{ g}$ | AES Active ($1.0\text{ L/h}$) | $0.0098$ | $2.50 \times 10^{-5}$ | $12.40$ | $3.8$ | $0.097$ (Creeping) | $68.5\%$ |
| | $0.0\text{ g}$ | Static Sealed | $0.0000$ | $0.00$ | $25.00$ | $1.2$ | **$0.031$ (Hypoxic)** | **$100.0\%$ (Diffusion)** |

### 3.3 Transient Aerodynamics of Fan Failure & Stagnation Response Across Gravities

| Hardware | Gravity | $\tau_{spin}\text{ (s)}$ | $t_{stagnant}\text{ (s)}$ | $g_{bl}\text{ Floor}$ | $t_{CO2}\text{ Starv.}$ | $t_{Hypoxia}$ | $\Delta T_{canopy}\text{ (K)}$ | Resilience Rating |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **Microgreen** | Earth ($1.0\text{ g}$) | $1.2\text{ s}$ | $3.6\text{ s}$ | $0.362$ | $12.5\text{ min}$ | $18.0\text{ min}$ | $+2.8\text{ K}$ | Moderate (buoyant convection) |
| | Microgravity ($0\text{ g}$) | $1.2\text{ s}$ | $3.6\text{ s}$ | $0.035$ | $3.1\text{ min}$ | $6.5\text{ min}$ | $+7.8\text{ K}$ | Critical (rapid suffocation) |
| **VEGGIE** | Earth ($1.0\text{ g}$) | $2.4\text{ s}$ | $7.2\text{ s}$ | $0.362$ | $15.0\text{ min}$ | $22.0\text{ min}$ | $+2.4\text{ K}$ | High (chimney buoyancy) |
| | Microgravity ($0\text{ g}$) | $2.4\text{ s}$ | $7.2\text{ s}$ | $0.028$ | $3.8\text{ min}$ | $7.2\text{ min}$ | $+6.9\text{ K}$ | Critical (100% stagnation) |
| **APH** | Earth ($1.0\text{ g}$) | $4.8\text{ s}$ | $14.4\text{ s}$ | $0.362$ | $18.0\text{ min}$ | $28.0\text{ min}$ | $+2.1\text{ K}$ | High (large ducted volume) |
| | Microgravity ($0\text{ g}$) | $4.8\text{ s}$ | $14.4\text{ s}$ | $0.042$ | $4.5\text{ min}$ | $8.9\text{ min}$ | $+5.8\text{ K}$ | Moderate-Low (larger buffer) |
| **CHROMEX PGC** | Microgravity ($0\text{ g}$) | $0.8\text{ s}$ | $2.4\text{ s}$ | $0.031$ | $1.8\text{ min}$ | $3.5\text{ min}$ | $+8.4\text{ K}$ | Extremely Critical (foam hypoxia) |

### 3.4 Petri Dish Science Sample Carrier Microenvironments & Micropore Tape Gas Exchange

| Dish Geometry | Flight Habitat | Gravity Regime | $\delta_{ext}\text{ (mm)}$ | $r_{ext}\text{ (s/m)}$ | $r_{tape}\text{ (s/m)}$ | $r_{tot}\text{ (s/m)}$ | Equil. $O_2\text{ (\%)}$ | Equil. $C_2H_4\text{ (ppm)}$ | Condensation ($RH>98\%$) |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **Square ($100\times100$)** | VEGGIE (VPS) | Earth ($1.0\text{ g}$) | $4.8$ | $120$ | $650$ | $1220$ | $18.4\%$ | $0.32\text{ ppm}$ | $18.5\text{ h}$ |
| **Square ($100\times100$)** | VEGGIE (VPS) | Moon ($0.166\text{ g}$) | $6.2$ | $210$ | $650$ | $1310$ | $16.8\%$ | $0.52\text{ ppm}$ | $12.0\text{ h}$ |
| **Square ($100\times100$)** | VEGGIE (VPS) | Microgravity ($0\text{ g}$) | $8.5$ | $380$ | $650$ | $1480$ | $14.2\%$ | **$0.85\text{ ppm}$ (Toxic)** | **$6.5\text{ h}$ (Severe)** |
| **Round ($\varnothing90\text{ mm}$)** | APH | Earth ($1.0\text{ g}$) | $2.2$ | $45$ | $920$ | $1285$ | $18.6\%$ | $0.18\text{ ppm}$ | $>48\text{ h}$ |
| **Round ($\varnothing90\text{ mm}$)** | APH | Moon ($0.166\text{ g}$) | $2.3$ | $48$ | $920$ | $1288$ | $18.2\%$ | $0.22\text{ ppm}$ | $>48\text{ h}$ |
| **Round ($\varnothing90\text{ mm}$)** | APH | Microgravity ($0\text{ g}$) | $2.4$ | $50$ | $920$ | $1290$ | $17.8\%$ | $0.28\text{ ppm}$ | $38.0\text{ h}$ |
| **Square (Sealed)** | Static (No Tape) | Microgravity ($0\text{ g}$) | $>25.0$ | $>2000$ | $>100\text{k}$ | $>102\text{k}$ | **$<2.0\%$ (Hypoxic)** | **$>3.50\text{ ppm}$** | **$1.8\text{ h}$** |

---

## 4. Figures & Multimedia Assets

- **Figure 1:** 3D Hardware Domain Architecture, Mesh Layout, and Flow Paths (`figures/output/Fig1_hardware_domains.pdf` / `.png`)
- **Figure 2:** Dimensionless Richardson Number ($Ri$) Scaling and Convective Regime Trajectories (`figures/output/Fig2_gravity_richardson.pdf` / `.png`)
- **Figure 3:** Canopy Aerodynamics, Velocity Profiles, Boundary Layer Conductance ($g_{bl}$), and Sherwood Numbers (`figures/output/Fig3_canopy_aerodynamics.pdf` / `.png`)
- **Figure 4:** Scalar Ventilation Dynamics, Local Mean Age of Air (LMA), and Dead Zone Mapping (`figures/output/Fig4_scalar_ventilation.pdf` / `.png`)
- **Figure 5:** Biosecurity, Pathogen Containment, and Bioaerosol Dispersion Trade Space (`figures/output/Fig5_biosecurity_trades.pdf` / `.png`)
- **Figure 6:** 3D Spatial Flow Topologies, Streamline Ribbons, and Canopy Shear Distributions (`figures/output/Fig6_3d_flow_topologies.pdf` / `.png`)
- **Figure 7:** Operational Airflow Extremes Matrix: Zero Stagnation vs. Low Draft vs. Nominal vs. High Blast (`figures/output/Fig7_airflow_extremes.pdf` / `.png`)
- **Figure 8:** NASA Space Shuttle CHROMEX / PGU Multi-Scale Thermal-Fluid & PGC Hypoxia Dynamics (`figures/output/Fig8_chromex_multiscale_hypoxia.pdf` / `.png`)
- **Figure 9:** Transient Aerodynamics of Fan Failure & Stagnation Response Across Gravities (`figures/output/Fig9_fan_failure_dynamics.pdf` / `.png`)
- **Figure 10:** Petri Dish Science Sample Carrier Microenvironments, Micropore Tape Gas Exchange, and Boundary-Layer Scaling Across Spaceflight Hardware (`figures/output/Fig10_petridish_microclimates.pdf` / `.png`)

### Interactive 3D WebGL Explorer & 4D Animations:
- **Interactive 3D WebGL Dashboard with Fan Failure Simulation:** [`visualizations/interactive_3d_explorer.html`](visualizations/interactive_3d_explorer.html)
- **4D Microgreen Jet Flapping & Vortex Shedding:** [`visualizations/animations/4D_microgreen_jet_flapping.gif`](visualizations/animations/4D_microgreen_jet_flapping.gif)
- **4D NASA VEGGIE Suction & Stagnation Dynamics:** [`visualizations/animations/4D_veggie_suction_dynamics.gif`](visualizations/animations/4D_veggie_suction_dynamics.gif)
- **4D NASA APH Lateral Cross-Flow Collision & Updraft:** [`visualizations/animations/4D_aph_lateral_collision.gif`](visualizations/animations/4D_aph_lateral_collision.gif)
- **4D Bioaerosol Plume Clearance & Containment Trade Space:** [`visualizations/animations/4D_bioaerosol_plume_clearance.gif`](visualizations/animations/4D_bioaerosol_plume_clearance.gif)
- **4D CHROMEX PGC Hypoxia & ADH Induction:** [`visualizations/animations/4D_chromex_hypoxia_depletion.gif`](visualizations/animations/4D_chromex_hypoxia_depletion.gif)
