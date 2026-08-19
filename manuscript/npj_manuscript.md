# Aerodynamic Boundary-Layer Scaling and Enclosure Regimes Across Spaceflight Plant Growth Hardware: A Multi-Chamber OpenFOAM CFD Framework under Variable Gravity

**Richard Barker$^{1,*}$, Henry Ewald$^{1}$, and Astrobotany Consortium$^{1}$**

$^{1}$Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN 47907, USA  
$^*$Corresponding author: `rbarker@purdue.edu`

---

## Abstract

Plants cultivated in extraterrestrial habitats encounter a physical environment devoid of natural gravity-driven buoyancy ($Gr \to 0$), expanding unstirred fluid boundary layers around vegetative canopies and drastically elevating aerodynamic resistance ($r_a = 1/g_{bl}$). Here, we present a systematic, multi-chamber 3D computational fluid dynamics (CFD) investigation comparing three distinct spaceflight and controlled-environment agricultural hardware architectures across four gravitational regimes: Earth ($1.0\text{ g}$), Mars ($0.38\text{ g}$), Moon ($0.166\text{ g}$), and Microgravity ($0\text{ g}$). Using an OpenFOAM v2606 finite-volume framework with conformal multi-solid analytic geometries, we model: (i) the compact **Microgreen Chamber** ($2.33\text{ L}$, through-flow confined jet), (ii) the **NASA Vegetable Production System (VEGGIE/VPS)** ($37.6\text{ L}$, top suction with passive cabin air induction), and (iii) the **NASA Advanced Plant Habitat (APH)** ($83.4\text{ L}$, ducted closed-loop opposing cross-flow). Parametric gravity sweeps reveal that ceiling-mounted LED arrays induce stable thermal stratification on Earth ($Ri \approx 0.14 - 1.55$), which suppresses vertical exchange; counter-intuitively, microgravity collapses this stratification, rendering purely forced convection ($Ri = 0$) superior in turbulent kinetic energy and canopy clearance. In VEGGIE, low-fan microgravity operation leads to a critical $52.8\%$ canopy stagnation volume and a $39.5\%$ reduction in $CO_2$ boundary layer conductance ($g_{bl} = 0.219\text{ mol m}^{-2}\text{s}^{-1}$), elevating fungal mold vulnerability and guttation stress. Conversely, APH's opposing lateral supply jets ($0.3 - 1.5\text{ m/s}$) maintain near-ideal displacement ventilation (air exchange efficiency $\varepsilon_a \approx 45\%$) and invariant $g_{bl} \approx 1.07\text{ mol m}^{-2}\text{s}^{-1}$ across all gravity levels. Analysis of suspended bioaerosols establishes a fundamental biosecurity trade-off: VEGGIE exports $100\%$ of aerosolized fungal spores directly into astronaut living quarters ($t_{50} = 13.8\text{ s}$), whereas APH achieves rapid internal HEPA scrubbing ($t_{50} = 18.4\text{ s}$) with zero cabin burden. These findings establish quantitative aerodynamic criteria for designing next-generation bioregenerative life support systems for Lunar and Martian surface missions.

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

| Parameter | Microgreen Chamber | VEGGIE (VPS) | Advanced Plant Habitat (APH) |
|:---|:---|:---|:---|
| **Payload Classification** | Benchtop Phenotyping | Deployable Space Garden | Closed-Loop Research Phytotron |
| **Enclosure Structure** | Rigid acrylic + parabolic hood | Collapsible FEP bellows | Carbon-fiber composite & titanium frame |
| **Growth Footprint ($A$)** | $0.0224\text{ m}^2$ ($120 \times 187\text{ mm}$) | $0.1075\text{ m}^2$ ($292 \times 368\text{ mm}$) | $0.1708\text{ m}^2$ ($454 \times 408\text{ mm}$) |
| **Canopy Air Volume ($V_{air}$)** | $2.33\text{ L}$ | $37.61\text{ L}$ (nominal) | $83.36\text{ L}$ (shoot zone) |
| **Total Canopy Height** | $96.7\text{ mm}$ (to hood spring) | $350.0\text{ mm}$ (nominal height) | $450.0\text{ mm}$ (clear shoot zone) |
| **Primary Flow Driver** | 1$\times$ Axial Fan ($\varnothing40\text{ mm}$ port) | 1$\times$ Top Suction Fan ($\varnothing50\text{ mm}$) | 2$\times$ Symmetric ECS Recirculation Blowers |
| **Airflow Topology** | Through-flow confined jet | Bottom-up forced suction | Opposing lateral cross-flow $\to$ sweep |
| **Nominal Flow Rate ($Q$)** | $11.8\text{ m}^3/\text{h}$ ($3.27\text{ L/s}$) | $85.0\text{ m}^3/\text{h}$ ($23.61\text{ L/s}$) | $26.4\text{ m}^3/\text{h}$ ($7.34\text{ L/s}$) |
| **Canopy Forced Velocity** | $0.262\text{ m/s}$ (bulk mean) | $0.150\text{ m/s}$ (mean draft) | $0.300 - 1.500\text{ m/s}$ (regulated) |
| **Air Exchange Rate ($\text{ACH}$)** | $5,051\text{ h}^{-1}$ ($\tau = 0.71\text{ s}$) | $2,260\text{ h}^{-1}$ ($\tau = 1.60\text{ s}$) | $317\text{ h}^{-1}$ ($\tau = 11.35\text{ s}$) |
| **Environmental Control** | Ambient laboratory | Cabin-coupled ($\Delta T = +2^\circ\text{C}$) | Closed loop ($18-30^\circ\text{C} \pm0.5^\circ\text{C}$, $50-90\%$ RH) |
| **Cabin Interface Coupling** | Sealed phenotyping unit | Open continuous exchange | Closed-loop payload in EXPRESS Rack |

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

### 3.3 Ventilation Efficiency & Habitat Biosecurity

| Chamber | Gravity | Flow Rate ($Q$) | $\tau_0\text{ (s)}$ | $\overline{\tau}_{canopy}\text{ (s)}$ | $\varepsilon_a\text{ (\%)}$ | $t_{50}\text{ (s)}$ | Biosecurity \& Aerosol Fate |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **Microgreen** | $1.0\text{ g}$ | $11.8\text{ m}^3/\text{h}$ | $0.71$ | $6.85$ | $10.4\%$ | $14.2$ | Sealed unit: zero cabin export; corner recirculation |
| | $0.0\text{ g}$ | $11.8\text{ m}^3/\text{h}$ | $0.71$ | $5.20$ | $13.7\%$ | $11.5$ | Unstratified jet improves canopy clearance |
| **VEGGIE** | $1.0\text{ g}$ | Low ($42.5\text{ m}^3/\text{h}$) | $3.19$ | $14.20$ | $22.5\%$ | $28.6$ | Direct cabin exhaust: $100\%$ spore export to ISS |
| | $0.0\text{ g}$ | Low ($42.5\text{ m}^3/\text{h}$) | $3.19$ | $22.40$ | $14.2\%$ | $45.2$ | Critical mold risk ($52.8\%$ stagnant volume) |
| | $0.0\text{ g}$ | High ($85.0\text{ m}^3/\text{h}$) | $1.60$ | $6.10$ | $26.2\%$ | $13.8$ | High fan restores boundary layer stripping |
| **APH** | $1.0\text{ g}$ | Nom ($26.4\text{ m}^3/\text{h}$) | $11.35$ | $24.80$ | $45.8\%$ | $18.4$ | Closed loop: internal HEPA filtration ($\le25\text{ ppb}$) |
| | $0.0\text{ g}$ | Nom ($26.4\text{ m}^3/\text{h}$) | $11.35$ | $25.20$ | $45.0\%$ | $18.9$ | Piston sweep maintains $45\%$ efficiency |
| | $0.0\text{ g}$ | High ($66.0\text{ m}^3/\text{h}$) | $4.54$ | $9.60$ | $47.3\%$ | $7.2$ | Near-ideal displacement flow ($\varepsilon_a \to 50\%$) |

---

## 4. Figures & Multimedia Assets

- **Figure 1:** 3D Hardware Domain Architecture, Mesh Layout, and Flow Paths (`figures/output/Fig1_hardware_domains.pdf` / `.png`)
- **Figure 2:** Dimensionless Richardson Number ($Ri$) Scaling and Convective Regime Trajectories (`figures/output/Fig2_gravity_richardson.pdf` / `.png`)
- **Figure 3:** Canopy Aerodynamics, Velocity Profiles, Boundary Layer Conductance ($g_{bl}$), and Sherwood Numbers (`figures/output/Fig3_canopy_aerodynamics.pdf` / `.png`)
- **Figure 4:** Scalar Ventilation Dynamics, Local Mean Age of Air (LMA), and Dead Zone Mapping (`figures/output/Fig4_scalar_ventilation.pdf` / `.png`)
- **Figure 5:** Biosecurity, Pathogen Containment, and Bioaerosol Dispersion Trade Space (`figures/output/Fig5_biosecurity_trades.pdf` / `.png`)
- **Figure 6:** 3D Spatial Flow Topologies, Streamline Ribbons, and Canopy Shear Distributions (`figures/output/Fig6_3d_flow_topologies.pdf` / `.png`)
- **Figure 7:** Operational Airflow Extremes Matrix: Zero Stagnation vs. Low Draft vs. Nominal vs. High Blast (`figures/output/Fig7_airflow_extremes.pdf` / `.png`)

### Interactive 3D WebGL Explorer & 4D Animations:
- **Interactive 3D WebGL Dashboard:** [`visualizations/interactive_3d_explorer.html`](visualizations/interactive_3d_explorer.html)
- **4D Microgreen Jet Flapping & Vortex Shedding:** [`visualizations/animations/4D_microgreen_jet_flapping.gif`](visualizations/animations/4D_microgreen_jet_flapping.gif)
- **4D NASA VEGGIE Suction & Stagnation Dynamics:** [`visualizations/animations/4D_veggie_suction_dynamics.gif`](visualizations/animations/4D_veggie_suction_dynamics.gif)
- **4D NASA APH Lateral Cross-Flow Collision & Updraft:** [`visualizations/animations/4D_aph_lateral_collision.gif`](visualizations/animations/4D_aph_lateral_collision.gif)
- **4D Bioaerosol Plume Clearance & Containment Trade Space:** [`visualizations/animations/4D_bioaerosol_plume_clearance.gif`](visualizations/animations/4D_bioaerosol_plume_clearance.gif)
