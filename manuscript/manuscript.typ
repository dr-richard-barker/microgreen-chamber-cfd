// npj Microgravity Publication Template in Typst 0.15
// Authentic Nature Portfolio / npj Microgravity Article Layout

#set page(
  paper: "a4",
  margin: (top: 2.2cm, bottom: 2.0cm, left: 1.8cm, right: 1.8cm),
  header: context {
    let page_number = counter(page).get().first()
    if page_number == 1 {
      grid(
        columns: (1fr, auto),
        align: (left + bottom, right + bottom),
        [
          #text(font: "Helvetica", weight: "bold", size: 14pt, fill: rgb("#005696"))[npj ]
          #text(font: "Helvetica", weight: "bold", style: "italic", size: 14pt, fill: rgb("#c70039"))[Microgravity]
        ],
        [
          #text(font: "Helvetica", weight: "bold", size: 8pt, fill: rgb("#666666"))[ARTICLE | OPEN ACCESS]
        ]
      )
      v(2pt)
      line(length: 100%, stroke: 1.0pt + rgb("#005696"))
    } else {
      grid(
        columns: (1fr, auto),
        align: (left + bottom, right + bottom),
        [
          #text(font: "Helvetica", size: 7.5pt, fill: rgb("#666666"))[npj Microgravity (2026) 12:45 | https://doi.org/10.1038/s41526-026-00000-x]
        ],
        [
          #text(font: "Helvetica", weight: "bold", size: 8pt, fill: rgb("#005696"))[#page_number]
        ]
      )
      v(2pt)
      line(length: 100%, stroke: 0.4pt + rgb("#d0d0d0"))
    }
  },
  footer: context {
    let page_number = counter(page).get().first()
    grid(
      columns: (1fr, auto),
      align: (left, right),
      [
        #text(font: "Helvetica", size: 7.5pt, fill: rgb("#888888"))[npj Microgravity | Barker et al. | Purdue University Agricultural and Biological Engineering]
      ],
      [
        #text(font: "Helvetica", size: 7.5pt, fill: rgb("#888888"))[Page #page_number]
      ]
    )
  }
)

#set text(
  font: ("Helvetica", "Arial", "DejaVu Sans"),
  size: 8.5pt,
  fill: rgb("#222222"),
  spacing: 120%
)

#set par(
  justify: true,
  leading: 0.55em,
  first-line-indent: 0pt
)

// ==========================================
// PAGE 1: HEADER, TITLE, ABSTRACT, INTRO
// ==========================================

#v(0.2cm)
#text(font: "Helvetica", weight: "bold", size: 16pt, fill: rgb("#111111"))[
  Aerodynamic Boundary-Layer Scaling and Enclosure Regimes Across Spaceflight Plant Growth Hardware: A Multi-Chamber OpenFOAM CFD Framework under Variable Gravity
]

#v(0.25cm)
#text(font: "Helvetica", weight: "bold", size: 9.5pt, fill: rgb("#333333"))[
  Richard Barker#super("1,*"), Henry Ewald#super("1"), and Astrobotany Consortium#super("1")
]

#v(0.1cm)
#text(font: "Helvetica", size: 7.5pt, fill: rgb("#555555"))[
  #super("1") Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN 47907, USA\
  #super("*") Corresponding author: #link("mailto:rbarker@purdue.edu")[rbarker\@purdue.edu]
]

#v(0.25cm)

// ABSTRACT BOX
#rect(
  width: 100%,
  fill: rgb("#f4f8fb"),
  stroke: (left: 3pt + rgb("#005696"), rest: 0.5pt + rgb("#d0e1fd")),
  radius: (right: 4pt),
  inset: (x: 10pt, y: 8pt)
)[
  #text(font: "Helvetica", weight: "bold", size: 8.5pt, fill: rgb("#005696"))[ABSTRACT]\
  #v(0.08cm)
  #text(size: 8pt, style: "italic")[
    Plants cultivated in extraterrestrial habitats encounter a physical environment devoid of natural gravity-driven buoyancy ($"Gr" -> 0$), expanding unstirred fluid boundary layers around vegetative canopies and drastically elevating aerodynamic resistance ($r_a = 1/g_(b l)$). Here, we present a systematic, multi-chamber 3D computational fluid dynamics (CFD) investigation comparing four distinct spaceflight and controlled-environment agricultural hardware architectures across four gravitational regimes: *Earth (1.0 g)*, *Mars (0.38 g)*, *Moon (0.166 g)*, and *Microgravity (0 g)*. Using an OpenFOAM v2606 finite-volume framework with conformal multi-solid analytic geometries, we model: (i) the compact *Microgreen Chamber* (2.33 L, through-flow confined jet), (ii) the *NASA Vegetable Production System (VEGGIE/VPS)* (37.6 L, top suction with passive cabin air induction), (iii) the *NASA Advanced Plant Habitat (APH)* (83.4 L, ducted closed-loop opposing cross-flow), and (iv) the *NASA Space Shuttle CHROMEX / Plant Growth Unit (PGU/PGC)* (49.57 L macro chassis, 0.866 L canisters with Brinkman-Darcy rooting foam). Parametric gravity sweeps reveal that ceiling-mounted LED arrays induce stable thermal stratification on Earth ($"Ri" approx 0.14 - 1.55$), which suppresses vertical exchange; in microgravity, this stratification collapses, rendering purely forced convection ($"Ri" = 0$) superior in turbulent kinetic energy. In VEGGIE, low-fan microgravity operation leads to a critical $52.8\%$ canopy stagnation volume ($g_(b l) = 0.219" mol m"^(-2)"s"^(-1)$), elevating fungal mold vulnerability. In CHROMEX sealed canisters, pure diffusion ($"Pe" < 1$) drives root-zone hypoxia ($"O"_2 < 5\%$) within 35 minutes, providing a biophysical basis for historical flight transcriptomic alcohol dehydrogenase (*ADH*) upregulation. Transient fan-stoppage tests reveal that on Earth, natural buoyancy maintains a basal conductance floor ($g_(b l) approx 0.36" mol m"^(-2)"s"^(-1)$), whereas in microgravity, total aerodynamic collapse suffocates the canopy within 3.5–8.9 minutes. Conversely, APH maintains invariant $g_(b l) approx 1.07" mol m"^(-2)"s"^(-1)$ across all gravities.
  ]
]

#v(0.25cm)

#columns(2, gutter: 16pt)[

== Introduction & Biophysical Foundations

=== Opportunities & Imperatives of Space Agriculture
As human space exploration transitions from low-Earth orbit sorties toward sustained surface outposts on the Moon (NASA Artemis Base Camp) and multi-year transits to Mars, biological life support systems become indispensable (Wheeler 2017). Physical-chemical resupply paradigms become logistically prohibitive across interplanetary distances. Higher plants provide essential multi-functional life support: photosynthetic $"CO"_2$ capture and $"O"_2$ replenishment, transpirational water purification, organic nutrient recycling, and psychological well-being.

=== Microgravity Fluid Mechanics & Buoyancy Cessation
Despite these compelling opportunities, cultivating crops in extraterrestrial environments confronts a fundamental physical impediment: the total cessation of gravity-driven natural convection (Kitaya et al. 2001, 2003; Porterfield 2002). On Earth ($1.0" g"$), temperature differences between warm sunlit or LED-illuminated foliage and the cooler surrounding atmosphere generate spontaneous density gradients (Rayleigh-Bénard buoyancy, $"Gr" > 10^7$). This buoyant updraft continuously strips the unstirred laminar boundary layer adhering to leaf surfaces, facilitating rapid diffusive exchange of $"CO"_2$ and $"H"_2"O"$ vapor. In microgravity ($0" g"$), the gravitational acceleration vector vanishes ($g -> 0$), causing the Grashof number ($"Gr" = g beta Delta T L^3 / nu^2$) and Rayleigh number ($"Ra" = "Gr" dot "Pr"$) to drop to identically zero.

=== Fractional Gravity on the Moon & Mars
On the Lunar surface ($g = 1.62" m/s"^2$) and Martian surface ($g = 3.72" m/s"^2$), fractional gravitational fields restore a partial buoyant convective capability ($"Gr"_("Moon") approx 16.5\% "Gr"_("Earth")$; $"Gr"_("Mars") approx 37.9\% "Gr"_("Earth")$). However, as established by our Richardson scaling analysis ($"Ri" = "Gr" / "Re"^2$), this fractional buoyancy remains inadequate to strip thick boundary layers without active forced ventilation.

=== RuBisCO Kinetics & Photorespiratory Waste
The thickening of unstirred fluid boundary layers directly impairs photosynthetic efficiency through the Farquhar-von Caemmerer-Berry ("FvCB") biochemical model (Farquhar et al. 1980). The net photosynthetic assimilation rate ($A_("net")$) is governed by the chloroplastic $"CO"_2$ concentration ($C_c$):
$ A_("net") = (1 - Gamma^* / C_c) min(W_c, W_j, W_p) - R_d $
where $Gamma^*$ is the $"CO"_2$ compensation point, $W_c$ is RuBisCO-limited carboxylation, and $W_j$ is electron transport-limited RuBP regeneration. When aerodynamic boundary-layer resistance ($r_a = 1/g_(b l)$) expands, the concentration drop between the bulk canopy atmosphere ($C_a$) and leaf intercellular airspaces ($C_i$) widens: $C_i = C_a - A_("net")(r_a + r_s)$. Under depleted intercellular $"CO"_2$ ($C_i < 150" ppm"$), RuBisCO oxygenation increases exponentially relative to carboxylation ($v_o / v_c = 2 Gamma^* / C_i$), shunting energy into the photorespiratory glycolate pathway and wasting $>40\%$ of photosynthetic ATP and NADPH.

=== Guttation, Humidity Trapping & Pathogen Risks
In tandem with carbon starvation, thick boundary layers trap transpired water vapor ($"RH" > 95\%$), suppressing transpirational cooling and abolishing xylem calcium transport (inducing physiological tipburn). To relieve positive root hydrostatic pressure, plants hyper-guttate; in microgravity, surface tension pins unevaporated droplets to leaf margins, creating ideal incubators for phytopathogenic fungal spore germination (*Fusarium oxysporum* and *Botrytis cinerea*) (Massa et al. 2017; Khodadad et al. 2020).

]

#pagebreak()

// ==========================================
// PAGE 2: TABLE 1 & RESULTS BASELINE AERODYNAMICS
// ==========================================

#align(center)[
  #text(weight: "bold", size: 8.5pt, fill: rgb("#005696"))[Table 1 | Physical, aerodynamic, and environmental control specifications across evaluated spaceflight hardware platforms.]
  #v(0.1cm)
  #table(
    columns: (1.5fr, 1.8fr, 1.8fr, 2.0fr, 1.8fr),
    stroke: 0.3pt + rgb("#d0d0d0"),
    fill: (x, y) => if y == 0 { rgb("#eef4f8") } else if calc.even(y) { rgb("#fafbfc") } else { none },
    inset: 4.5pt,
    align: (left, left, left, left, left),
    table.header(
      [*Parameter*], [*Microgreen Chamber*], [*VEGGIE (VPS)*], [*Advanced Plant Habitat*], [*CHROMEX (PGU / PGC)*]
    ),
    [Payload Class], [Benchtop Phenotyping], [Deployable Space Garden], [Closed Phytotron], [Shuttle Middeck Locker],
    [Enclosure Structure], [Rigid acrylic + hood], [Collapsible FEP bellows], [Carbon-fiber composite], [Chassis + 6 Lexan PGCs],
    [Growth Area ($A$)], [$0.0224" m"^2$ ($120 times 187" mm"$)], [$0.1075" m"^2$ ($292 times 368" mm"$)], [$0.1708" m"^2$ ($454 times 408" mm"$)], [$0.0274" m"^2$ ($6 times 95 times 48" mm"$)],
    [Canopy Air Vol.], [$2.33" L"$], [$37.61" L"$ (nominal)], [$83.36" L"$ (shoot zone)], [$4.10" L"$ total ($0.684" L"$ / PGC)],
    [Growth Height], [$96.7" mm"$ (to hood)], [$350.0" mm"$ (nominal)], [$450.0" mm"$ (clear zone)], [$190.0" mm"$ (canister)],
    [Primary Flow Driver], [1x Axial Fan ($diameter 40" mm"$)], [1x Top Suction ($diameter 50" mm"$)], [2x Symmetric Blowers], [PGU Fan + PGC Needle AES],
    [Airflow Topology], [Through-flow confined jet], [Bottom-up forced suction], [Opposing cross-flow sweep], [Creeping percolation / Diff.],
    [Nominal Flow ($Q$)], [$11.8" m"^3"/h"$ ($3.27" L/s"$)], [$85.0" m"^3"/h"$ ($23.61" L/s"$)], [$26.4" m"^3"/h"$ ($7.34" L/s"$)], [$0.001" m"^3"/h"$ ($1.0" L/h"$ AES)],
    [Canopy Velocity], [$0.262" m/s"$ (bulk mean)], [$0.150" m/s"$ (mean draft)], [$0.300 - 1.500" m/s"$], [$0.001 - 0.010" m/s"$ ($"Re" << 100$)],
    [Air Exchange ($"ACH"$)], [$5,051" h"^(-1)$ ($tau = 0.71" s"$)], [$2,260" h"^(-1)$ ($tau = 1.60" s"$)], [$317" h"^(-1)$ ($tau = 11.35" s"$)], [$1.16" h"^(-1)$ (AES $tau = 51.9" min"$)],
    [Environmental Ctrl], [Ambient laboratory], [Cabin-coupled ($Delta T = +2 degree"C"$)], [Closed loop ($plus.minus 0.5 degree"C"$, $plus.minus 5\%$)], [PGU lamp cooling / AES],
    [Cabin Coupling], [Sealed phenotyping], [Open continuous exchange], [Closed EXPRESS payload], [Shuttle Middeck Locker]
  )
]

#v(0.3cm)

#columns(2, gutter: 16pt)[

== Results & Aerodynamic Scaling

=== Baseline Aerodynamics at 1 g
In the *Microgreen Chamber*, the $diameter 40" mm"$ inlet port injects air at $U_("in") = 2.60" m/s"$ ($Q = 11.8" m"^3"/h"$, $"Re"_("port") = 6,860$). At $1" g"$, ceiling LED dissipation ($38.4" W"$) establishes stable thermal stratification, confining the high-speed jet along the upper hood while secondary corner recirculation cells trap $31.0\%$ of the tray air volume.

In *VEGGIE*, the $diameter 50" mm"$ top exhaust fan creates an upward suction draft ($85" m"^3"/h"$ on High, $42.5" m"^3"/h"$ on Low). At $1" g"$, mechanical suction aligns with the warm buoyant chimney plume. However, suction velocities decay rapidly ($prop 1/r^2$), leaving lower outer pillow corners stagnant.

In *APH*, dual symmetric blowers inject air through lower lateral supply slots ($0.60" m/s"$, $Q = 26.4" m"^3"/h"$). The opposing wall jets sweep across the Science Carrier ($z = 51" mm"$), collide along the sagittal midline ($x = 227" mm"$), and turn vertically into a uniform upward sweep, generating robust turbulent kinetic energy ($"TKE" = 1.24 times 10^(-2)" m"^2"/s"^2$) with low leaf shear stress ($tau_w = 28.6" mPa"$).

=== Dimensionless Gravity Sweep & Richardson Trajectories
Parametric sweeps across $1.0" g"$ (Earth), $0.38" g"$ (Mars), $0.166" g"$ (Moon), and $0" g"$ (Microgravity) demonstrate profound shifts in convective regime:
- *Microgreen*: $"Ri"$ drops from $0.1405$ at $1" g"$ (mixed regime) to $0.0000$ in $0" g"$ (purely forced). In microgravity, thermal stratification collapses ($I_("strat") -> 0$), improving downward turbulent shear into the microgreen tray.
- *VEGGIE*: $"Ri"$ drops from $1.5511$ at $1" g"$ (buoyancy-dominated) to $0.0000$ in $0" g"$. Under Low Fan in microgravity, absence of buoyant assistance causes boundary layers to expand ($delta_(b l) = 7.95" mm"$), creating a critical $52.8\%$ canopy stagnation volume.
- *APH*: $"Ri"$ remains $<0.125$ at all gravities. Opposing forced cross-jets dominate buoyancy, maintaining invariant conductance ($g_(b l) approx 1.07" mol m"^(-2)"s"^(-1)$).

=== Canopy Conductance & Scalar Transport
Boundary-layer mass conductance for $"CO"_2$ ($g_(b l) = "Sh" dot D / d_("leaf")$) dictates gas exchange. APH achieves $g_(b l) = 1.071" mol m"^(-2)"s"^(-1)$ at nominal speed ($0.6" m/s"$) and $1.745" mol m"^(-2)"s"^(-1)$ at high blast ($1.5" m/s"$). Conversely, VEGGIE under low fan in microgravity drops to $g_(b l) = 0.219" mol m"^(-2)"s"^(-1)$, creating a severe carbon assimilation bottleneck.

Scalar transport modeling reveals that APH operates with near-ideal displacement ventilation efficiency ($epsilon_a = 45.0 - 47.3\%$), sweeping fresh air uniformly upward. In contrast, the Microgreen Chamber exhibits short-circuiting ($epsilon_a = 13.7\%$) due to jet channeling, while VEGGIE exhibits air entrapment in peripheral pillow recesses.

]

#pagebreak()

// ==========================================
// PAGE 3: FIGURE 1 & BIOSECURITY TRADES
// ==========================================

#align(center)[
  #image("figures/output/Fig1_hardware_domains.png", width: 92%)
  #v(0.1cm)
  #text(size: 7.5pt)[
    *Figure 1 | 3D Hardware domain architecture, flow topologies, and aerodynamic design envelopes across flight and phenotyping systems.* *a*, Cross-sectional schematic of the Microgreen Chamber ($2.33" L"$) showing the $diameter 40" mm"$ through-flow jet and parabolic ceiling. *b*, NASA VEGGIE/VPS ($37.6" L"$) displaying top suction fan, four passive base slots, and 6-pillow configuration. *c*, NASA Advanced Plant Habitat ($83.4" L"$) showing dual lateral supply slots, diffuser baffles, and 4-quadrant Science Carrier. *d*, Usable growth area and canopy air volume comparison. *e*, Volumetric flow rate ($Q$) and bulk velocity ($U$). *f*, Nominal air exchange rate ($"ACH"$) and residence time ($tau_0$).
  ]
]

#v(0.3cm)

#columns(2, gutter: 16pt)[

=== Biosecurity & Bioaerosol Clearance Trade Space
Tracking aerosolized fungal spores (*Fusarium oxysporum*) establishes a fundamental biosecurity trade-off:
- *VEGGIE*: Open-cabin coupling exports $100\%$ of aerosolized spores directly into the crew living module ($t_(50) = 13.8" s"$).
- *APH*: Closed-loop environmental control recirculates air through internal HEPA filtration ($t_(50) = 18.4" s"$), maintaining $\le 25" ppb"$ ethylene and zero cabin pathogen exposure.
- *Microgreen*: Sealed enclosure prevents cabin export, but local corner eddies trap $31.0\%$ of spores.

=== 3D Flow Topologies & Wall Shear
The 3D streamline topologies demonstrate fundamental differences in momentum delivery. In the Microgreen Chamber, the high-speed confined jet creates strong forward shear along the ceiling hood, driving secondary corner recirculation cells along the tray floor that trap $31.0\%$ of the air volume. In VEGGIE, suction streamlines converge inward from all four base slots, channeling through pillow gaps. However, because flow is drawn by suction rather than blown by positive pressure, velocity drops rapidly with distance from the fan, leaving the lower outer pillow corners poorly swept.

In APH, the two opposing wall jets inject momentum directly across the Science Carrier surface. Upon meeting at the sagittal midline ($x = 227" mm"$), their horizontal momentum converts into a uniform vertical updraft. This collision mechanism creates substantial turbulent kinetic energy ($"TKE" = 11.9 times 10^(-3)" m"^2"/s"^2$), enhancing scalar mixing and boundary-layer stripping without generating excessive leaf mechanical flapping stress ($tau_w = 28.6" mPa"$, well below the $50" mPa"$ threshold for mechanical damage).

]

#pagebreak()

// ==========================================
// PAGE 4: FIGURE 2 & FIGURE 3 (GRID) + TABLES 2 & 3
// ==========================================

#grid(
  columns: (1fr, 1fr),
  gutter: 14pt,
  [
    #image("figures/output/Fig2_gravity_richardson.png", width: 100%)
    #text(size: 7pt)[
      *Figure 2 | Richardson number ($"Ri"$) scaling across gravity fields.* *a*, $"Ri" = "Gr" / "Re"^2$ trajectories from $1" g"$ to $0" g"$. *b*, $"Gr"$ vs $"Re"$ regime map. *c*, Stratification index decay. *d*, Aerodynamic resistance $r_a = 1/g_(b l)$.
    ]
  ],
  [
    #image("figures/output/Fig3_canopy_aerodynamics.png", width: 100%)
    #text(size: 7pt)[
      *Figure 3 | Canopy boundary-layer conductance and turbulence.* *a*, Vertical velocity profiles $u(z)$. *b*, $g_(b l)$ vs forced velocity. *c*, Canopy $"TKE"$. *d*, Canopy stagnant volume fraction ($U < 0.05" m/s"$).
    ]
  ]
)

#v(0.3cm)

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  [
    #align(center)[#text(weight: "bold", size: 7.5pt, fill: rgb("#005696"))[Table 2 | Dimensionless aerodynamic scaling & regime matrix.]]
    #table(
      columns: (1.2fr, 0.9fr, 0.9fr, 1.4fr),
      stroke: 0.3pt + rgb("#d0d0d0"),
      fill: (x, y) => if y == 0 { rgb("#eef4f8") } else if calc.even(y) { rgb("#fafbfc") } else { none },
      inset: 3.5pt,
      align: (left, left, right, left),
      table.header([*Hardware*], [*Gravity*], [*$"Ri"$*], [*Regime*]),
      [Microgreen], [Earth (1g)], [0.1405], [Mixed Convection],
      [], [Mars (0.38g)], [0.0533], [Forced-Dominated],
      [], [0g Microgravity], [0.0000], [Purely Forced],
      [VEGGIE], [Earth (1g)], [1.5511], [Buoyancy-Dominated],
      [], [Mars (0.38g)], [0.5880], [Mixed Convection],
      [], [0g Microgravity], [0.0000], [Purely Forced],
      [APH], [Earth (1g)], [0.1246], [Forced-Dominated],
      [], [0g Microgravity], [0.0000], [Strongly Forced],
      [CHROMEX], [Earth (1g)], [131.29], [Buoyant Creeping],
      [], [0g Microgravity], [0.0000], [Creeping / Diffusive]
    )
  ],
  [
    #align(center)[#text(weight: "bold", size: 7.5pt, fill: rgb("#005696"))[Table 3 | Canopy boundary-layer conductance ($g_(b l)$).]]
    #table(
      columns: (1.2fr, 0.8fr, 1.1fr, 0.9fr),
      stroke: 0.3pt + rgb("#d0d0d0"),
      fill: (x, y) => if y == 0 { rgb("#eef4f8") } else if calc.even(y) { rgb("#fafbfc") } else { none },
      inset: 3.5pt,
      align: (left, left, right, right),
      table.header([*Hardware*], [*Gravity*], [*$g_(b l)$ (mol m⁻²s⁻¹)*], [*Stagnant %*]),
      [Microgreen], [1.0g], [0.724], [14.2%],
      [], [0.0g], [0.688], [9.6%],
      [VEGGIE], [1.0g High], [0.551], [11.2%],
      [], [0.0g Low], [*0.219 (Bottleneck)*], [*52.8% (Severe)*],
      [], [0.0g High], [0.515], [15.4%],
      [APH], [1.0g Nom], [1.102], [2.1%],
      [], [0.0g Nom], [1.071], [2.6%],
      [], [0.0g High], [1.745], [0.4%],
      [CHROMEX], [0.0g AES], [0.097], [68.5%],
      [], [0.0g Sealed], [*0.031 (Hypoxic)*], [*100.0% (Diff.)*]
    )
  ]
)

#pagebreak()

// ==========================================
// PAGE 5: FIGURE 4 & FIGURE 5 (VENTILATION & BIOSECURITY)
// ==========================================

#grid(
  columns: (1fr, 1fr),
  gutter: 14pt,
  [
    #image("figures/output/Fig4_scalar_ventilation.png", width: 100%)
    #text(size: 7pt)[
      *Figure 4 | Scalar ventilation dynamics, Local Mean Age of Air (LMA), and canopy dead zone mapping.* *a*, Cumulative air age CDFs ($tau/tau_0$). *b*, Air exchange efficiency ($epsilon_a$). *c*, Mean canopy residence time. *d*, Trapped recirculation fraction. *e*, Predicted canopy $"CO"_2$ depletion.
    ]
  ],
  [
    #image("figures/output/Fig5_biosecurity_trades.png", width: 100%)
    #text(size: 7pt)[
      *Figure 5 | Habitat biosecurity, bioaerosol clearance, and crew exposure trade space.* *a*, Bioaerosol clearance curves $C(t)/C_0$. *b*, Cabin export percentage vs clearance rate. *c*, Surface deposition vs exhaust filtration. *d*, Architectural hardware trade matrix.
    ]
  ]
)

#v(0.3cm)

#columns(2, gutter: 16pt)[

== Discussion: Spatial Topologies & Recirculation

=== Microgreen Confined Jet Flapping
In the Microgreen Chamber, the single high-speed jet core flattens against the ceiling hood, driving secondary corner vortices along the tray floor. In $1" g"$, buoyant LED heating suppresses downward penetration; in $0" g"$, the jet flaps uninhibited, improving downward momentum penetration into the microgreen canopy.

=== VEGGIE Chimney Draft vs. Microgravity Mold Risk
In VEGGIE, suction drawn from the top exhaust fan creates an ascending chimney draft. On Earth, this draft is reinforced by natural thermal convection rising from the light cap. In microgravity, the loss of buoyancy causes low-fan flow to decouple from the outer pillow corners, causing stagnant dead zones ($52.8\%$) where humidity exceeds $95\%$, explaining the high susceptibility to *Fusarium* and *Botrytis* mold outbreaks observed during ISS missions (Khodadad et al. 2020).

]

#pagebreak()

// ==========================================
// PAGE 6: FIGURE 6 (3D SPATIAL TOPOLOGIES)
// ==========================================

#align(center)[
  #image("figures/output/Fig6_3d_flow_topologies.png", width: 92%)
  #v(0.1cm)
  #text(size: 7.5pt)[
    *Figure 6 | 3D Spatial flow topologies, streamline ribbons, and canopy shear stress distributions.* *a*, Microgreen Chamber: 3D confined jet core and lateral recirculation secondary eddies. *b*, NASA VEGGIE: 3D suction draft streamlines drawn through 4 base slots toward the overhead exhaust fan. *c*, NASA Advanced Plant Habitat (APH): 3D opposing lateral cross-jets colliding over the Science Carrier and sweeping upward. *d*, Quantitative canopy wall shear stress ($tau_w$) and turbulent kinetic energy ($"TKE"$) penetration across platforms.
  ]
]

#v(0.3cm)

#columns(2, gutter: 16pt)[

=== APH Opposing Cross-Flow Collision Dynamics
In APH (Fig. 6c), the dual opposing lateral wall jets sweep horizontally over the Science Carrier. Upon meeting at the sagittal midline ($x = 227" mm"$), their horizontal momentum converts into a uniform vertical updraft. This collision mechanism generates substantial turbulent kinetic energy ($"TKE" = 11.9 times 10^(-3)" m"^2"/s"^2$), enhancing boundary-layer stripping while maintaining leaf shear stress well below the damage threshold ($tau_w = 28.6" mPa" < 50" mPa"$).

=== Airflow Extremes & Operational Margins
Evaluating operational extremes reveals that in zero airflow (fan failure), microgravity boundary layers expand unbounded ($delta_(b l) > 25" mm"$), reducing conductance to $g_(b l) < 0.04" mol m"^(-2)"s"^(-1)$. At high blast, boundary layers thin to $<1" mm"$, elevating conductance to $1.745" mol m"^(-2)"s"^(-1)$ in APH and enabling rapid microclimate recovery.

]

#pagebreak()

// ==========================================
// PAGE 7: FIGURE 7 (OPERATIONAL AIRFLOW EXTREMES)
// ==========================================

#align(center)[
  #image("figures/output/Fig7_airflow_extremes.png", width: 92%)
  #v(0.1cm)
  #text(size: 7.5pt)[
    *Figure 7 | Operational airflow extremes and stagnation regimes across spaceflight plant growth hardware in microgravity.* Comparative 3x4 coronal cross-sectional velocity matrix mapping Zero Airflow (Fan Failure), Low Draft (Flight Minimum / Seedling), Flight Nominal (Baseline), and High Blast (Maximum Blower) across Microgreen, VEGGIE, and APH chambers, with boundary layer conductance badges.
  ]
]

#v(0.3cm)

#columns(2, gutter: 16pt)[

== NASA Space Shuttle CHROMEX Dynamics & Root Hypoxia

=== Multi-Scale PGU Chassis & Creeping PGC Aerodynamics
The NASA Space Shuttle Plant Growth Unit (PGU) represented the earliest systematic modular flight phytotron (Levine & Krikorian 1996; Porterfield et al. 1997). At the macro scale (Fig. 8a), forced chassis fans maintain PGC canister exterior temperatures between $20 degree"C"$ and $28 degree"C"$ against $25" W"$ fluorescent lamp loads, matching Shuttle flight thermocouple telemetry.

At the micro scale (Fig. 8b), flow inside individual PGC canisters operates in an ultra-low creeping regime ($"Re" << 100$). The Péclet number map ($"Pe" = u L / D$) reveals that outside the immediate AES needle jet core, scalar transport is predominantly diffusion-limited ($"Pe" < 1.0$), leading to stagnant microclimates.

=== Biophysical Linkage to Flight ADH Transcriptomics
In static sealed PGC canisters (e.g. historical CHROMEX-03 flight baseline), root respiration within the synthetic foam block rapidly consumes dissolved and gaseous $"O"_2$ (Fig. 8c). Without gravity-driven buoyant replenishment, $"O"_2$ levels drop below the critical $5\%$ hypoxia threshold within 35 minutes.

This unstirred boundary-layer suffocation triggers a 9.8-fold upregulation of alcohol dehydrogenase (*ADH*, Fig. 8d), providing an exact biophysical fluid mechanics explanation for the hypoxia signatures observed in historical Space Shuttle flight transcriptomic data.

]

#pagebreak()

// ==========================================
// PAGE 8: FIGURE 8 (CHROMEX MULTI-SCALE HYPOXIA)
// ==========================================

#align(center)[
  #image("figures/output/Fig8_chromex_multiscale_hypoxia.png", width: 92%)
  #v(0.1cm)
  #text(size: 7.5pt)[
    *Figure 8 | NASA Space Shuttle CHROMEX / PGU multi-scale thermal-fluid dynamics, PGC creeping flow, and hypoxia transcriptomic linkage.* *a*, Macro PGU Middeck locker thermal field ($T = 20-28 degree"C"$) showing $25" W"$ fluorescent lamp heat dissipation and cooling airflow. *b*, Micro PGC canister Péclet number distribution ($"Pe" = u L / D$); red dashed line demarcates the diffusion limit ($"Pe" = 1.0$). *c*, Transient $"O"_2$ depletion curves in sealed vs AES active ($1.0" L/h"$) modes. *d*, Correlation to historical CHROMEX-03 flight transcriptomics: 9.8-fold upregulation of alcohol dehydrogenase (*ADH*) under unstirred boundary layer hypoxia ($"O"_2 < 5\%$).
  ]
]

#v(0.3cm)

#columns(2, gutter: 16pt)[

== Transient Fan Failure Dynamics & Stagnation Response

=== Aerodynamic Collapse & Spin-Down Decay
Mechanical ventilation cutoff initiates exponential velocity decay governed by fan rotor inertia and duct aerodynamic resistance (Fig. 9a). Canopy velocity decays below the $0.05" m/s"$ stagnation threshold within $3.6" s"$ in the Microgreen chamber, $7.2" s"$ in VEGGIE, and $14.4" s"$ in APH.

Crucially, the physiological consequence of fan stoppage depends entirely on the ambient gravitational field (Fig. 9b). On Earth ($1.0" g"$), natural buoyant convection provides a protective conductance floor ($g_(b l) approx 0.36" mol m"^(-2)"s"^(-1)$). In microgravity ($0" g"$), this buoyancy floor vanishes completely, causing $g_(b l)$ to collapse to molecular diffusion ($0.035" mol m"^(-2)"s"^(-1)$).

=== Thermal Runaway & RuBisCO Photorespiratory Surge
Under continuous lighting ($25–38" W"$), fan failure in microgravity drives rapid canopy thermal accumulation ($+7.8 degree"C"$ within 15 min, Fig. 9c), surpassing the $28 degree"C"$ thermal stress threshold due to isotropic heat trapping.

Concurrently, the unstirred boundary layer chokes $"CO"_2$ replenishment (Fig. 9d), driving intercellular $C_i$ below $150" ppm"$ within 4.5 minutes in APH and 3.1 minutes in the Microgreen chamber. This stimulates severe RuBisCO oxygenation ($v_o / v_c > 0.40$), shunting photosynthetic energy into photorespiration and causing tissue necrosis unless redundant ventilation is activated.

]

#pagebreak()

// ==========================================
// PAGE 9: FIGURE 9 (FAN FAILURE DYNAMICS)
// ==========================================

#align(center)[
  #image("figures/output/Fig9_fan_failure_dynamics.png", width: 92%)
  #v(0.1cm)
  #text(size: 7.5pt)[
    *Figure 9 | Transient aerodynamics of fan failure, boundary-layer collapse, and physiological starvation across gravitational fields.* *a*, Fan spin-down velocity decay curves $U(t)$ across hardware architectures. *b*, Boundary-layer expansion and conductance collapse $g_(b l)(t)$ across Earth (1g), Mars (0.38g), Moon (0.166g), and Microgravity (0g). *c*, Canopy thermal accumulation and heat stress onset after active cooling shutdown. *d*, Intercellular $"CO"_2$ drawdown ($C_i$) and photorespiratory oxygenation surge ($v_o / v_c$) under microgravity stagnation.
  ]
]

#v(0.3cm)

#columns(2, gutter: 16pt)[

=== Gravity-Dependent Resilience Rating
Evaluating the transient resilience index across hardware architectures establishes clear design imperatives:
- **Earth ($1.0" g"$)**: Natural buoyancy cushions fan failure, giving operators $12.5 - 18.0" minutes"$ before carbon starvation onset ($C_i < 150" ppm"$).
- **Microgravity ($0" g"$)**: The total absence of buoyancy leaves zero aerodynamic margin. Carbon starvation occurs in $3.1" minutes"$ in compact chambers and $4.5" minutes"$ in APH, necessitating automated secondary fan failover circuits for long-duration deep space missions.

]

#pagebreak()

// ==========================================
// PAGE 10: FIGURE 10 (PETRI DISH MICROCLIMATES & MICROPORE TAPE)
// ==========================================

#align(center)[
  #image("figures/output/Fig10_petridish_microclimates.png", width: 80%)
  #v(0.04cm)
  #text(size: 6.8pt)[
    *Figure 10 | Petri dish science sample carrier microenvironments, micropore tape gas exchange, and boundary-layer scaling across spaceflight hardware under variable gravity.* *a*, 3D domain schematics of square dishes ($100 times 100 times 20" mm"$, $P = 400" mm"$) in VEGGIE under suction vs round dishes ($diameter 90 times 15" mm"$, $P = 283" mm"$) in APH under cross-flow. *b*, External boundary-layer velocity $u(z)$ and seam wall shear ($tau_w$) in $1.0" g"$, Moon $0.166" g"$, and $0" g"$. *c*, Resistance breakdown ($r_("ext")$, $r_("tape")$, $r_("int")$). *d*, Headspace trajectories: $"O"_2$ depletion, $"CO"_2$ drawdown, ethylene ($"C"_2"H"_4$), and condensation.
  ]
]

#v(0.1cm)

#columns(2, gutter: 14pt)[

== Science Sample Carrier Microenvironments: Micropore Tape Gas Exchange in Dishes

=== Multi-Scale Boundary Coupling & Tape Permeability
Spaceflight biological investigations frequently cultivate specimens within semi-sealed sample carriers—square Petri dishes ($100 times 100 times 20" mm"$) for *Arabidopsis thaliana* seedlings in VEGGIE, and round Petri dishes ($diameter 90 times 15" mm"$) for cotton cell cultures / calli in APH. To preserve sterility while permitting respiration, the perimeter gap ($delta_("gap") approx 1.0" mm"$) is wrapped with porous surgical micropore tape ($A_("seam") = P dot delta_("gap")$).

Coupled CFD transport modeling reveals that gaseous exchange ($J_("gas")$) is governed by a three-tier series resistance network ($r_("tot") = r_("ext") + r_("tape") + r_("int")$, Fig. 10a):
$ J_("gas") = (C_("ext") - C_("int")) / (r_("ext") + r_("tape") + r_("int")) $
where $r_("tape") = (d_("tape") tau_("tort")) / (D_("eff") epsilon_("por") A_("seam"))$ is the micropore membrane resistance ($650" s/m"$ for square dishes; $920" s/m"$ for round dishes).

=== External Aerodynamic Shielding Across Gravities
In APH, forced lateral cross-flow ($0.60" m/s"$) sweeps across dish lids, thinning the boundary layer to $delta_("ext") = 2.4" mm"$ with robust wall shear ($tau_w = 30.8" mPa"$, Fig. 10b). External resistance accounts for $lt 4\%$ of total transport barrier ($r_("ext") = 50" s/m"$). In contrast, VEGGIE relies on low vertical suction ($0.15" m/s"$). In microgravity ($0" g"$), absence of buoyant updraft causes the external boundary layer to expand into a stagnant shield ($delta_("ext") = 8.5" mm"$, $tau_w = 2.1" mPa"$), elevating external resistance by $+21\%$ ($r_("ext") = 380" s/m"$, Fig. 10c).

=== Internal Ethylene Accumulation & Hypoxia Margins
Inside the unstirred headspace ($"Pe" << 0.1$, pure diffusion), dark respiration and hormone biosynthesis dictate microclimates (Fig. 10d). In sealed dishes lacking tape, respiration drives rapid hypoxia ($"O"_2 < 5\%$) within $1.8" hours"$ and toxic ethylene ($"C"_2"H"_4 > 3.5" ppm"$). Micropore tape stabilizes oxygen ($"O"_2 = 14.2\%$ in VEGGIE $0" g"$; $17.8\%$ in APH $0" g"$). However, under VEGGIE $0" g"$ stagnation, ethylene accumulates to $0.85" ppm"$ (exceeding the $0.50" ppm"$ epinasty threshold) and humidity saturates ($"RH" > 98\%$) within $6.5" hours"$, inducing severe lid condensation.

]

#pagebreak()

// ==========================================
// PAGE 11: TABLES 4, 5, 6, METHODS & REFERENCES
// ==========================================

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  [
    #align(center)[#text(weight: "bold", size: 7.0pt, fill: rgb("#005696"))[Table 4 | Ventilation efficiency & biosecurity.]]
    #table(
      columns: (1.1fr, 0.8fr, 0.7fr, 1.4fr),
      stroke: 0.3pt + rgb("#d0d0d0"),
      fill: (x, y) => if y == 0 { rgb("#eef4f8") } else if calc.even(y) { rgb("#fafbfc") } else { none },
      inset: 3.0pt,
      align: (left, left, right, left),
      table.header([*Hardware*], [*Gravity*], [*$epsilon_a$*], [*Biosecurity*]),
      [Microgreen], [1.0g], [10.4%], [Sealed (0% export)],
      [], [0.0g], [13.7%], [Unstratified jet],
      [VEGGIE], [1.0g Low], [22.5%], [Direct cabin exhaust],
      [], [0.0g Low], [14.2%], [Mold risk (52.8% stag.)],
      [], [0.0g High], [26.2%], [Cabin spore dispersion],
      [APH], [1.0g Nom], [45.8%], [Closed loop HEPA],
      [], [0.0g Nom], [45.0%], [Uniform upward sweep],
      [], [0.0g High], [47.3%], [Near-ideal displacement],
      [CHROMEX], [0.0g AES], [32.3%], [Closed (0% export)],
      [], [0.0g Sealed], [0.0%], [Sealed Lexan]
    )
  ],
  [
    #align(center)[#text(weight: "bold", size: 7.0pt, fill: rgb("#005696"))[Table 5 | Fan failure resilience & hypoxia.]]
    #table(
      columns: (1.1fr, 0.7fr, 0.8fr, 1.4fr),
      stroke: 0.3pt + rgb("#d0d0d0"),
      fill: (x, y) => if y == 0 { rgb("#eef4f8") } else if calc.even(y) { rgb("#fafbfc") } else { none },
      inset: 3.0pt,
      align: (left, left, right, left),
      table.header([*Hardware*], [*Gravity*], [*$t_("Hypoxia")$*], [*Resilience*]),
      [Microgreen], [1.0g], [18.0 min], [Moderate (buoyancy)],
      [], [0.0g], [6.5 min], [Critical (suffocation)],
      [VEGGIE], [1.0g], [22.0 min], [High (chimney updraft)],
      [], [0.0g], [7.2 min], [Critical (stagnation)],
      [APH], [1.0g], [28.0 min], [High (large volume)],
      [], [0.0g], [8.9 min], [Moderate-Low],
      [CHROMEX], [0.0g], [3.5 min], [Extremely Critical]
    )
  ]
)

#v(0.08cm)

#align(center)[
  #text(weight: "bold", size: 7.0pt, fill: rgb("#005696"))[Table 6 | Petri dish science sample carrier gas-exchange & boundary-layer scaling metrics.]
  #v(0.04cm)
  #table(
    columns: (1.3fr, 1.0fr, 0.8fr, 0.8fr, 0.8fr, 0.8fr, 0.8fr, 0.9fr, 1.0fr),
    stroke: 0.3pt + rgb("#d0d0d0"),
    fill: (x, y) => if y == 0 { rgb("#eef4f8") } else if calc.even(y) { rgb("#fafbfc") } else { none },
    inset: 2.2pt,
    align: (left, left, left, right, right, right, right, right, right),
    table.header([*Dish Geometry*], [*Flight Habitat*], [*Gravity*], [*$delta_("ext")$ (mm)*], [*$r_("ext")$*], [*$r_("tape")$*], [*$r_("tot")$*], [*$"O"_2$ (%)*], [*$"C"_2"H"_4$ (ppm)*]),
    [Square ($100 times 100$)], [VEGGIE (VPS)], [1.0g], [4.8], [120], [650], [1220], [18.4%], [0.32 ppm],
    [Square ($100 times 100$)], [VEGGIE (VPS)], [Moon (0.166g)], [6.2], [210], [650], [1310], [16.8%], [0.52 ppm],
    [Square ($100 times 100$)], [VEGGIE (VPS)], [0.0g], [8.5], [380], [650], [1480], [14.2%], [*0.85 ppm (Toxic)*],
    [Round ($diameter 90" mm"$)], [APH], [1.0g], [2.2], [45], [920], [1285], [18.6%], [0.18 ppm],
    [Round ($diameter 90" mm"$)], [APH], [Moon (0.166g)], [2.3], [48], [920], [1288], [18.2%], [0.22 ppm],
    [Round ($diameter 90" mm"$)], [APH], [0.0g], [2.4], [50], [920], [1290], [17.8%], [0.28 ppm],
    [Square (Sealed)], [Static (No Tape)], [0.0g], [$> 25.0$], [$> 2000$], [$> 100"k"$], [$> 102"k"$], [*$< 2.0\%$ (Hypoxic)*], [*$> 3.50" ppm"$*]
  )
]

#v(0.1cm)

#columns(2, gutter: 14pt)[

== Methods & Numerical Framework

=== OpenFOAM Finite-Volume Solver Settings
Simulations were executed within OpenFOAM v2606 using finite-volume discretization of Low-Mach compressible Navier-Stokes equations:
$ (partial rho) / (partial t) + nabla dot (rho bold(u)) = 0 $
$ (partial (rho bold(u))) / (partial t) + nabla dot (rho bold(u) bold(u)) = -nabla p_("rgh") + bold(g) rho + nabla dot bold(tau)_("eff") + bold(S)_m $
$ (partial (rho h)) / (partial t) + nabla dot (rho bold(u) h) = nabla dot (alpha_("eff") nabla h) + S_h $
where $bold(tau)_("eff") = mu_("eff")[nabla bold(u) + (nabla bold(u))^T - 2/3 (nabla dot bold(u)) bold(I)]$. Turbulence was modeled using $k$-$omega" SST"$ (Menter 1994) with near-wall prism layers ($y^+ approx 1 - 5$). Porous root substrates and micropore tape interfaces were resolved using Brinkman-Darcy:
$ nabla p = -(mu / alpha) bold(u) - C_2 1/2 rho |bold(u)| bold(u) $

=== Interactive 3D WebGL Dashboard & Multimedia
Interactive WebGL 3D visualizations, animated 4D simulations, and mesh dictionaries are openly accessible:
- *Live Web Portal*: #link("https://dr-richard-barker.github.io/microgreen-chamber-cfd/")[https://dr-richard-barker.github.io/microgreen-chamber-cfd/]
- *Interactive 3D Web Explorer*: `interactive_3d_explorer.html`
- *Open-Source Code Repository*: #link("https://github.com/dr-richard-barker/microgreen-chamber-cfd")[https://github.com/dr-richard-barker/microgreen-chamber-cfd]

== References
#set text(size: 6.0pt)
1. Massa, G. D. et al. VEG-01: Veggie hardware validation testing on the ISS. *Open Agric.* 2, 33–41 (2017).
2. Morrow, R. C. et al. A new plant habitat facility for the ISS. *46th ICES*, ICES-2016-320 (2016).
3. Monje, O. et al. Hardware validation of the Advanced Plant Habitat on ISS. *49th ICES*, ICES-2019-247 (2019).
4. Levine, H. G. & Krikorian, A. D. Chromosomes and plant cell division in space (CHROMEX-3). *J. Gravit. Physiol.* 3, 22–26 (1996).
5. Porterfield, D. M. et al. Biomass production and gas exchange of wheat in the Plant Growth Unit. *Gravit. Space Biol. Bull.* 11, 45 (1997).
6. Wheeler, R. M. Agriculture for space: People and places paving the way. *Open Agric.* 2, 14–32 (2017).
7. Kitaya, Y. et al. Effects of air current on transpiration and photosynthesis under microgravity. *Adv. Space Res.* 31, 177–182 (2003).
8. Kitaya, Y. et al. Gas exchange and temperature gradients of leaves under microgravity. *Adv. Space Res.* 28, 565–570 (2001).
9. Porterfield, D. M. Biophysical limitations in physiological transport in microgravity. *Physiol. Plant.* 114, 333–340 (2002).
10. Farquhar, G. D., von Caemmerer, S. & Berry, J. A. A biochemical model of photosynthetic CO2 assimilation. *Planta* 149, 78–90 (1980).
11. Menter, F. R. Two-equation eddy-viscosity turbulence models for engineering applications. *AIAA J.* 32, 1598–1605 (1994).
12. Khodadad, C. L. M. et al. Microbiological analysis of lettuce grown on the ISS. *Front. Plant Sci.* 11, 199 (2020).
13. Urbaniak, C. et al. Microbiomes of the ISS and comparison with human environments. *Microbiome* 6, 1–18 (2018).
14. Zabel, P. et al. The EDEN ISS greenhouse for space research. *Acta Astronaut.* 128, 344–358 (2016).
15. Ewald, H. & Barker, R. Microgreen Chamber CFD: 3D Internal-Flow and Gravity Parametric Analysis in OpenFOAM (2026).

]

