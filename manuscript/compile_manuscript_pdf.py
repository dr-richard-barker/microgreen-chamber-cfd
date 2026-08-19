#!/usr/bin/env python3
"""
Compile a publication-grade npj Microgravity manuscript PDF using Matplotlib's native vector PDF engine.
Includes:
- Correct Purdue University Department of Agricultural and Biological Engineering affiliation
- Well-balanced Cover Page with no awkward empty space
- Dedicated Introduction Page on Space Agriculture, Microgravity vs. Lunar gravity, Gaseous exchange, and Photorespiration
- Formatted tables with explicit colWidths and clean text wrapping (no spillover)
- Figures 1–7 (3D topologies, 4D simulation dynamics, operational airflow extremes)
- Methods, References, and Multimedia Availability
"""

import os
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches
import matplotlib.image as mpimg

def generate_pdf(pdf_path):
    root = os.path.dirname(os.path.abspath(__file__))
    fig_dir = os.path.join(root, "figures", "output")
    
    plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans, sans-serif'
    plt.rcParams['font.family'] = 'sans-serif'
    
    c_nature_blue = "#005696"
    c_nature_red = "#e31837"
    c_dark = "#222222"
    c_grey = "#555555"

    with PdfPages(pdf_path) as pdf:
        
        # =========================================================================
        # PAGE 1: Journal Header, Title, Authors, Abstract, Overview & Table 1
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        # Header bar
        ax.plot([0.08, 0.92], [0.94, 0.94], color=c_nature_blue, lw=2.5)
        ax.text(0.08, 0.95, "npj ", fontsize=18, fontweight="bold", color=c_nature_blue, va="bottom")
        ax.text(0.14, 0.95, "Microgravity", fontsize=18, fontweight="bold", fontstyle="italic", color=c_nature_red, va="bottom")
        ax.text(0.92, 0.95, "ARTICLE | OPEN ACCESS", fontsize=9, fontweight="bold", color=c_grey, ha="right", va="bottom")
        
        # Title
        title_text = "Aerodynamic Boundary-Layer Scaling and Enclosure Regimes Across\nSpaceflight Plant Growth Hardware: A Multi-Chamber OpenFOAM CFD\nFramework under Variable Gravity"
        ax.text(0.08, 0.90, title_text, fontsize=13, fontweight="bold", color="#111111", va="top", linespacing=1.25)
        
        # Authors & Affiliations (Updated to Purdue ABE)
        ax.text(0.08, 0.815, "Richard Barker*, Henry Ewald, and Astrobotany Consortium", fontsize=9.5, fontweight="bold", color="#333333", va="top")
        affils = "Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN 47907, USA.\n*Corresponding author: rbarker@purdue.edu"
        ax.text(0.08, 0.795, affils, fontsize=8.0, color=c_grey, va="top", linespacing=1.25)
        
        # Abstract Box
        rect = patches.FancyBboxPatch((0.08, 0.585), 0.84, 0.185, boxstyle="round,pad=0.015,rounding_size=0.01",
                                      facecolor="#f4f8fb", edgecolor=c_nature_blue, lw=1.2)
        ax.add_patch(rect)
        ax.text(0.10, 0.755, "ABSTRACT", fontsize=8.5, fontweight="bold", color=c_nature_blue, va="top")
        
        abstract_body = (
            "Plants cultivated in extraterrestrial habitats encounter a physical environment devoid of natural gravity-driven buoyancy "
            "($Gr \\to 0$), expanding unstirred fluid boundary layers around vegetative canopies and drastically elevating aerodynamic resistance "
            "($r_a = 1/g_{bl}$). Here, we present a systematic, multi-chamber 3D computational fluid dynamics (CFD) investigation comparing three "
            "distinct spaceflight and controlled-environment agricultural hardware architectures across four gravitational regimes: Earth ($1.0\\text{ g}$), "
            "Mars ($0.38\\text{ g}$), Moon ($0.166\\text{ g}$), and Microgravity ($0\\text{ g}$). Using an OpenFOAM v2606 finite-volume framework with conformal "
            "multi-solid analytic geometries, we model: (i) the compact Microgreen Chamber ($2.33\\text{ L}$, through-flow confined jet), (ii) the NASA Vegetable "
            "Production System (VEGGIE/VPS) ($37.6\\text{ L}$, top suction with passive cabin air induction), and (iii) the NASA Advanced Plant Habitat (APH) "
            "($83.4\\text{ L}$, ducted closed-loop opposing cross-flow). Parametric gravity sweeps reveal that ceiling-mounted LED arrays induce stable thermal "
            "stratification on Earth ($Ri \\approx 0.14 - 1.55$), which suppresses vertical exchange; counter-intuitively, microgravity collapses this stratification, "
            "rendering purely forced convection ($Ri = 0$) superior in turbulent kinetic energy and canopy clearance. In VEGGIE, low-fan microgravity operation "
            "leads to a critical $52.8\\%$ canopy stagnation volume and a $39.5\\%$ reduction in $CO_2$ boundary layer conductance ($g_{bl} = 0.219\\text{ mol m}^{-2}\\text{s}^{-1}$), "
            "elevating fungal mold vulnerability and guttation stress. Conversely, APH's opposing lateral supply jets ($0.3 - 1.5\\text{ m/s}$) maintain near-ideal "
            "displacement ventilation (air exchange efficiency $\\varepsilon_a \\approx 45\\%$) and invariant $g_{bl} \\approx 1.07\\text{ mol m}^{-2}\\text{s}^{-1}$ across all gravity levels."
        )
        ax.text(0.10, 0.735, abstract_body, fontsize=7.2, color=c_dark, va="top", linespacing=1.22, wrap=True)
        
        # Executive Summary / Overview Narrative filling the space above Table 1
        ax.text(0.08, 0.560, "EXECUTIVE HARDWARE ARCHITECTURE COMPARISON", fontsize=9.0, fontweight="bold", color=c_nature_blue, va="top")
        ov_text = (
            "Spaceflight plant production systems must reconcile structural mass, electrical power constraints, and crew safety with strict physiological "
            "aerodynamic requirements. Table 1 summarizes the primary engineering, aerodynamic, and environmental control envelopes across the three "
            "evaluated platforms: the benchtop Microgreen Chamber ($2.33\\text{ L}$), the deployable NASA VEGGIE system ($37.61\\text{ L}$), and the quad-locker "
            "NASA Advanced Plant Habitat ($83.36\\text{ L}$). Whereas VEGGIE operates via open continuous exchange with ISS cabin atmosphere, APH represents a fully "
            "isolated closed-loop phytotron with active thermal, relative humidity, $CO_2$, and photocatalytic ethylene scrubbers."
        )
        ax.text(0.08, 0.540, ov_text, fontsize=7.3, color=c_dark, va="top", linespacing=1.2, wrap=True)
        
        # Table 1 (Carefully proportioned with explicit column widths)
        ax.text(0.08, 0.440, "Table 1 | Physical, aerodynamic, and environmental control specifications across evaluated hardware platforms.", fontsize=7.8, fontweight="bold", color="#111111", va="top")
        
        t1_headers = ["Parameter", "Microgreen Chamber", "VEGGIE (VPS)", "Advanced Plant Habitat (APH)"]
        t1_rows = [
            ["Payload Class", "Benchtop Phenotyping", "Deployable Space Garden", "Closed-Loop Research Phytotron"],
            ["Enclosure Structure", "Rigid acrylic + hood", "Collapsible FEP bellows", "Carbon-fiber composite & titanium"],
            ["Growth Footprint (A)", "0.0224 m² (120×187 mm)", "0.1075 m² (292×368 mm)", "0.1708 m² (454×408 mm)"],
            ["Canopy Air Vol. (V_air)", "2.33 L", "37.61 L (nominal)", "83.36 L (shoot growth zone)"],
            ["Total Growth Height", "96.7 mm (to hood spring)", "350.0 mm (nominal height)", "450.0 mm (clear shoot zone)"],
            ["Primary Flow Driver", "1× Axial Fan (Ø40mm port)", "1× Top Suction Fan (Ø50mm)", "2× Symmetric ECS Blowers"],
            ["Airflow Topology", "Through-flow confined jet", "Bottom-up forced suction", "Opposing lateral cross-flow -> sweep"],
            ["Nominal Flow Rate (Q)", "11.8 m³/h (3.27 L/s)", "85.0 m³/h (23.61 L/s)", "26.4 m³/h (7.34 L/s)"],
            ["Canopy Forced Velocity", "0.262 m/s (bulk mean)", "0.150 m/s (mean draft)", "0.300 - 1.500 m/s (regulated)"],
            ["Air Exchange Rate", "5,051 h⁻¹ (τ = 0.71 s)", "2,260 h⁻¹ (τ = 1.60 s)", "317 h⁻¹ (τ = 11.35 s)"],
            ["Environmental Control", "Ambient laboratory", "Cabin-coupled (ΔT = +2°C)", "Closed loop (18-30°C ±0.5°C, 50-90% RH)"],
            ["Cabin Atmosphere Coupling", "Sealed phenotyping unit", "Open continuous exchange", "Closed-loop payload in EXPRESS Rack"]
        ]
        table_ax = fig.add_axes([0.08, 0.05, 0.84, 0.37])
        table_ax.axis('off')
        tab = table_ax.table(cellText=t1_rows, colLabels=t1_headers, colWidths=[0.22, 0.25, 0.25, 0.28], cellLoc='left', loc='center')
        tab.auto_set_font_size(False)
        tab.set_fontsize(7.0)
        tab.scale(1.0, 1.28)
        for (r, c), cell in tab.get_celld().items():
            cell.set_edgecolor("#d0d0d0")
            if r == 0:
                cell.set_facecolor("#eef4f8")
                cell.set_text_props(weight='bold', color=c_nature_blue)
            else:
                if r % 2 == 0:
                    cell.set_facecolor("#fafbfc")
        
        pdf.savefig(fig)
        plt.close(fig)
        
        # =========================================================================
        # PAGE 2 (NEW): Comprehensive Introduction & Space Agriculture Biophysics
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        ax.text(0.08, 0.94, "INTRODUCTION & BIOPHYSICAL FOUNDATIONS", fontsize=11, fontweight="bold", color=c_nature_blue, va="top")
        
        intro_p1 = (
            "Opportunities and Imperatives of Space Agriculture:\n"
            "As human space exploration transitions from low-Earth orbit (LEO) sorties toward sustained surface habitats on the Moon "
            "(NASA Artemis Base Camp) and multi-year transits to Mars, biological life support systems become indispensable. Physical-chemical "
            "resupply paradigms become logistically prohibitive across deep-space distances. Plants provide essential multi-functional life support: "
            "they convert metabolic carbon dioxide into breathable oxygen via photosynthetic photolysis, produce purified potable water through "
            "transpirational distillation, recycle nitrogenous and mineral waste from sanitized organic effluent, and synthesize fresh secondary "
            "nutrients (including carotenoids, potassium, vitamin C, and polyphenols) that degrade rapidly in pre-packaged freeze-dried rations. "
            "Furthermore, interactive horticultural engagement delivers profound behavioral and psychological countermeasures against the sensory "
            "monotony and confinement of deep-space habitats.\n\n"
            "The Microgravity Fluid Challenge & Buoyancy Cessation:\n"
            "Despite these compelling opportunities, cultivating crops in extraterrestrial environments confronts a severe, fundamental physical "
            "impediment: the reduction or total absence of gravity-driven natural convection. On Earth ($1.0\\text{ g}$), temperature differences between warm "
            "sunlit or LED-illuminated foliage and the cooler surrounding atmosphere generate spontaneous density gradients (Rayleigh-Bénard buoyancy, "
            "$Gr > 10^7$). This buoyant updraft continuously strips the unstirred laminar boundary layer adhering to leaf surfaces, facilitating "
            "rapid diffusive exchange of $CO_2$ and $H_2O$ vapor. In microgravity ($0\\text{ g}$), the gravitational acceleration vector vanishes ($g \\to 0$), "
            "causing the Grashof number ($Gr = g \\beta \\Delta T L^3 / \\nu^2$) and Rayleigh number ($Ra = Gr \\cdot Pr$) to drop to identically zero."
        )
        ax.text(0.08, 0.91, intro_p1, fontsize=7.4, color=c_dark, va="top", linespacing=1.22, wrap=True)
        
        intro_p2 = (
            "Fractional Gravity on the Moon ($0.166\\text{ g}$) and Mars ($0.38\\text{ g}$):\n"
            "On the Lunar surface ($g = 1.62\\text{ m/s}^2$) and Martian surface ($g = 3.72\\text{ m/s}^2$), fractional gravitational fields restore a partial "
            "buoyant convective capability ($Gr_{Moon} \\approx 16.5\\% Gr_{Earth}$; $Gr_{Mars} \\approx 37.9\\% Gr_{Earth}$). However, as established by our Richardson "
            "scaling analysis ($Ri = Gr / Re^2$), this fractional buoyancy remains inadequate to strip thick boundary layers without active forced ventilation. "
            "Unless engineered ventilation is precisely tailored, lunar and martian greenhouses will operate in an unstable mixed-convection regime prone to "
            "thermal stratification and localized suffocation pockets.\n\n"
            "Photosynthetic Suppression & Photorespiratory Waste (RuBisCO Kinetics):\n"
            "The thickening of unstirred fluid boundary layers directly impairs photosynthetic efficiency through the Farquhar-von Caemmerer-Berry (FvCB) "
            "biochemical model. The net photosynthetic assimilation rate ($A_{net}$) is governed by the chloroplastic $CO_2$ concentration ($C_c$):\n"
            "    A_{net} = \\left(1 - \\frac{\\Gamma^*}{C_c}\\right) \\min(W_c, W_j, W_p) - R_d\n"
            "where $\\Gamma^*$ is the $CO_2$ compensation point, $W_c$ is RuBisCO-limited carboxylation, and $W_j$ is electron transport-limited RuBP regeneration. "
            "When aerodynamic boundary-layer resistance ($r_a = 1/g_{bl}$) expands, the concentration drop between the bulk canopy atmosphere ($C_a$) and leaf "
            "intercellular airspaces ($C_i$) widens dramatically: $C_i = C_a - A_{net}(r_a + r_s)$. Under depleted intercellular $CO_2$ ($C_i < 150\\text{ ppm}$), "
            "the oxygenation reaction catalyzed by RuBisCO increases exponentially relative to carboxylation ($v_o / v_c = 2\\Gamma^* / C_i$), shunting energy into "
            "the photorespiratory glycolate pathway. This wasteful oxygenation can consume over $40\\%$ of photosynthetic ATP and NADPH, drastically suppressing biomass yield.\n\n"
            "Guttation, Boundary-Layer Humidity Saturation, and Pathogen Epidemics:\n"
            "In tandem with carbon starvation, thick boundary layers trap transpired water vapor, elevating local boundary layer relative humidity ($RH > 95\\%$). "
            "This suppresses transpirational evaporative cooling (causing leaf thermal stress) and abolishes the transpirational pull required for xylem mineral "
            "transport (inducing calcium deficiency and physiological tipburn). To relieve positive root hydrostatic pressure, plants undergo hyper-guttation, "
            "exuding nutrient-rich liquid droplets along hydathodes. In microgravity, surface tension pins these unevaporated droplets to leaf margins, creating "
            "ideal microclimatic incubators for phytopathogenic fungal spore germination (such as Fusarium oxysporum and Botrytis cinerea)."
        )
        ax.text(0.08, 0.49, intro_p2, fontsize=7.4, color=c_dark, va="top", linespacing=1.22, wrap=True)
        
        pdf.savefig(fig)
        plt.close(fig)

        # =========================================================================
        # PAGE 3: Figure 1 & Baseline Aerodynamics
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        fig1_img = mpimg.imread(os.path.join(fig_dir, "Fig1_hardware_domains.png"))
        ax_img = fig.add_axes([0.08, 0.43, 0.84, 0.52])
        ax_img.imshow(fig1_img)
        ax_img.axis('off')
        
        fig1_cap = (
            "Figure 1 | 3D Hardware domain architecture, flow topologies, and aerodynamic design envelopes across the three flight and phenotyping systems. "
            "a, Cross-sectional schematic of the Microgreen Chamber (2.33 L volume) showing the Ø40 mm through-flow jet and parabolic ceiling. "
            "b, NASA VEGGIE/VPS (37.6 L) displaying top suction fan, four passive base slots, and 6-pillow configuration. "
            "c, NASA Advanced Plant Habitat (83.4 L) showing dual lateral supply slots, diffuser baffles, and 4-quadrant Science Carrier. "
            "d, Usable growth area and canopy air volume comparison. e, Volumetric flow rate (Q) and bulk velocity (U). "
            "f, Nominal air exchange rate (ACH) and residence time (τ0)."
        )
        ax.text(0.08, 0.41, fig1_cap, fontsize=7.5, color=c_dark, va="top", linespacing=1.25, wrap=True)
        
        ax.text(0.08, 0.33, "RESULTS: BASELINE 1 g AERODYNAMICS", fontsize=9.5, fontweight="bold", color=c_nature_blue, va="top")
        res_col1 = (
            "Microgreen Confined Jet Flow Structure:\n"
            "In the Microgreen Chamber, the Ø40 mm inlet port injects air at\n"
            "U_in = 2.60 m/s (Re_port = 6,860, Q = 11.8 m³/h). The jet discharges\n"
            "longitudinally across the 186.7 mm depth. At 1 g, thermal dissipation\n"
            "from the ceiling LED (38.4 W) creates stable thermal stratification,\n"
            "confining the high-speed jet core along the upper parabolic hood and\n"
            "dampening downward turbulent shear into the microgreen tray.\n"
            "Time-accurate PIMPLE simulations reveal periodic jet flapping (±18.2% RMS).\n\n"
            "VEGGIE Top Suction Plume Mechanics:\n"
            "In VEGGIE, the Ø50 mm top exhaust fan creates an upward suction draft\n"
            "(85 m³/h on High, 42.5 m³/h on Low). At 1 g, the mechanical suction aligns\n"
            "constructively with the buoyant plume rising from the warm LED light cap,\n"
            "producing a central chimney draft that accelerates core flow but leaves\n"
            "peripheral pillow corners stagnant."
        )
        ax.text(0.08, 0.305, res_col1, fontsize=7.4, color=c_dark, va="top", linespacing=1.2)
        
        res_col2 = (
            "APH Opposing Lateral Jet Collision & Updraft Sweep:\n"
            "In APH, dual symmetric ECS blowers deliver air through lateral lower\n"
            "supply slots (w = 408 mm, h = 15 mm) at controlled speeds (0.3 - 1.5 m/s,\n"
            "nominal 0.6 m/s, Q = 26.4 m³/h). The opposing wall jets sweep horizontally\n"
            "across the Science Carrier (z = 51 mm), collide along the central sagittal\n"
            "plane (x = 227 mm), and turn vertically into a uniform upward sweep.\n\n"
            "This opposed-jet collision generates strong turbulent kinetic energy\n"
            "(TKE = 1.24 × 10⁻² m²/s²) while preventing high-velocity point-shear damage\n"
            "on delicate apical meristems, achieving an exceptionally high and uniform\n"
            "boundary layer conductance across the entire growth footprint."
        )
        ax.text(0.50, 0.305, res_col2, fontsize=7.4, color=c_dark, va="top", linespacing=1.2)
        
        pdf.savefig(fig)
        plt.close(fig)

        # =========================================================================
        # PAGE 4: Figure 2 & Table 2 (Gravity Sweep & Richardson Trajectories)
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        fig2_img = mpimg.imread(os.path.join(fig_dir, "Fig2_gravity_richardson.png"))
        ax_img = fig.add_axes([0.08, 0.46, 0.84, 0.49])
        ax_img.imshow(fig2_img)
        ax_img.axis('off')
        
        fig2_cap = (
            "Figure 2 | Richardson number (Ri) scaling, buoyancy collapse, and aerodynamic regime transitions across gravitational fields. "
            "a, Ri = Gr / Re² trajectory as a function of gravity g; horizontal bands demarcate forced-dominated (Ri < 0.1), mixed (0.1 ≤ Ri ≤ 1.0), and buoyant (Ri > 1.0) regimes. "
            "b, Grashof (Gr) vs. Reynolds (Re) regime map. c, Thermal stratification index (I_strat) decay from 1 g to μg. "
            "d, Canopy aerodynamic resistance (r_a = 1/g_bl) under variable gravity."
        )
        ax.text(0.08, 0.44, fig2_cap, fontsize=7.5, color=c_dark, va="top", linespacing=1.25, wrap=True)
        
        ax.text(0.08, 0.36, "Table 2 | Dimensionless aerodynamic scaling and convection regime matrix across hardware under variable gravity.", fontsize=7.8, fontweight="bold", color="#111111", va="top")
        
        t2_headers = ["Chamber", "Gravity Regime", "g (m/s²)", "Gr", "Re", "Ri (Gr/Re²)", "Convective Regime", "Dominant Aerodynamic Mechanism"]
        t2_rows = [
            ["Microgreen", "Earth (1.0g)", "9.81", "3.87e5", "1,669", "0.1405", "Mixed Convection", "Confined jet + ceiling thermal stratification"],
            ["", "Mars (0.38g)", "3.72", "1.47e5", "1,669", "0.0533", "Forced-Dominated", "Jet momentum dominates; weak stratification"],
            ["", "Moon (0.166g)", "1.62", "6.39e4", "1,669", "0.0232", "Forced-Dominated", "Buoyancy negligible; forward jet core"],
            ["", "Microgravity (0g)", "0.00", "0.00", "1,669", "0.0000", "Purely Forced", "Flapping confined jet; unstratified canopy"],
            ["VEGGIE", "Earth (1.0g)", "9.81", "1.83e7", "3,463", "1.5511", "Mixed (Buoyant)", "Thermal plume assists upward fan chimney draft"],
            ["", "Mars (0.38g)", "3.72", "6.95e6", "3,463", "0.5880", "Mixed (Transitional)", "Weak plume; fan suction required for draw"],
            ["", "Moon (0.166g)", "1.62", "3.03e6", "3,463", "0.2561", "Forced-Dominated", "Low draft velocity; mold risk at low fan"],
            ["", "Microgravity (0g)", "0.00", "0.00", "3,463", "0.0000", "Purely Forced", "Unstirred boundary layer without high fan"],
            ["APH", "Earth (1.0g)", "9.81", "3.90e7", "17,810", "0.1246", "Forced-Dominated", "Dual opposing cross-jets suppress buoyant plume"],
            ["", "Mars (0.38g)", "3.72", "1.48e7", "17,810", "0.0473", "Strongly Forced", "Piston-like upward sweep across shoot zone"],
            ["", "Moon (0.166g)", "1.62", "6.44e6", "17,810", "0.0206", "Strongly Forced", "Uniform boundary layer across Science Carrier"],
            ["", "Microgravity (0g)", "0.00", "0.00", "17,810", "0.0000", "Purely Forced", "Fully engineered forced recirculation sweep"]
        ]
        table_ax = fig.add_axes([0.08, 0.05, 0.84, 0.28])
        table_ax.axis('off')
        tab2 = table_ax.table(cellText=t2_rows, colLabels=t2_headers, colWidths=[0.12, 0.12, 0.08, 0.08, 0.08, 0.10, 0.14, 0.28], cellLoc='left', loc='center')
        tab2.auto_set_font_size(False)
        tab2.set_fontsize(6.8)
        tab2.scale(1.0, 1.25)
        for (r, c), cell in tab2.get_celld().items():
            cell.set_edgecolor("#d0d0d0")
            if r == 0:
                cell.set_facecolor("#eef4f8")
                cell.set_text_props(weight='bold', color=c_nature_blue)
            else:
                if r % 2 == 0:
                    cell.set_facecolor("#fafbfc")
                    
        pdf.savefig(fig)
        plt.close(fig)

        # =========================================================================
        # PAGE 5: Figure 3 & Table 3 (Canopy Aerodynamics & Conductance g_bl)
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        fig3_img = mpimg.imread(os.path.join(fig_dir, "Fig3_canopy_aerodynamics.png"))
        ax_img = fig.add_axes([0.08, 0.46, 0.84, 0.49])
        ax_img.imshow(fig3_img)
        ax_img.axis('off')
        
        fig3_cap = (
            "Figure 3 | Canopy microclimatic boundary-layer profiles, turbulence, and mass conductance (g_bl). "
            "a, Vertical velocity profiles normalized by chamber height (z/H). b, Boundary-layer conductance g_bl for CO2 mass transfer as a function of forced velocity U, compared against laminar (Sh $\\propto$ Re^0.5) and turbulent (Sh $\\propto$ Re^0.8) theory. "
            "c, Canopy turbulent kinetic energy (TKE) across operational modes. d, Canopy stagnant volume fraction (U < 0.05 m/s) with fungal pathogen risk threshold."
        )
        ax.text(0.08, 0.44, fig3_cap, fontsize=7.5, color=c_dark, va="top", linespacing=1.25, wrap=True)
        
        ax.text(0.08, 0.36, "Table 3 | Canopy boundary-layer aerodynamic parameters and effective conductance (g_bl) across platforms.", fontsize=7.8, fontweight="bold", color="#111111", va="top")
        
        t3_headers = ["Hardware", "Gravity", "Operating Mode", "U_canopy (m/s)", "TKE (m²/s²)", "δ_bl (mm)", "Sh_CO2", "g_bl (mol m⁻²s⁻¹)", "Stagnant Vol (%)"]
        t3_rows = [
            ["Microgreen", "1.0g", "Baseline", "0.262", "4.82e-3", "2.41", "28.4", "0.724", "14.2%"],
            ["", "0.0g", "Microgravity", "0.262", "4.40e-3", "2.54", "27.0", "0.688", "9.6%"],
            ["VEGGIE", "1.0g", "Low Fan", "0.065", "1.12e-3", "4.82", "14.2", "0.362", "32.4%"],
            ["", "1.0g", "High Fan", "0.150", "3.45e-3", "3.18", "21.6", "0.551", "11.2%"],
            ["", "0.0g", "Low Fan", "0.065", "0.68e-3", "7.95", "8.6", "0.219 (Bottleneck)", "52.8% (Severe Risk)"],
            ["", "0.0g", "High Fan", "0.150", "3.02e-3", "3.40", "20.2", "0.515", "15.4%"],
            ["APH", "1.0g", "Nominal (0.6 m/s)", "0.600", "1.24e-2", "1.58", "43.2", "1.102", "2.1%"],
            ["", "0.0g", "Nominal (0.6 m/s)", "0.600", "1.19e-2", "1.63", "42.0", "1.071", "2.6%"],
            ["", "0.0g", "High (1.5 m/s)", "1.500", "3.65e-2", "0.98", "68.4", "1.745", "0.4%"]
        ]
        table_ax = fig.add_axes([0.08, 0.07, 0.84, 0.26])
        table_ax.axis('off')
        tab3 = table_ax.table(cellText=t3_rows, colLabels=t3_headers, colWidths=[0.12, 0.08, 0.18, 0.12, 0.10, 0.09, 0.09, 0.12, 0.10], cellLoc='left', loc='center')
        tab3.auto_set_font_size(False)
        tab3.set_fontsize(7.0)
        tab3.scale(1.0, 1.3)
        for (r, c), cell in tab3.get_celld().items():
            cell.set_edgecolor("#d0d0d0")
            if r == 0:
                cell.set_facecolor("#eef4f8")
                cell.set_text_props(weight='bold', color=c_nature_blue)
            else:
                if r % 2 == 0:
                    cell.set_facecolor("#fafbfc")
                    
        pdf.savefig(fig)
        plt.close(fig)

        # =========================================================================
        # PAGE 6: Figure 4 & Figure 5 (Ventilation Dynamics & Biosecurity Trades)
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        fig4_img = mpimg.imread(os.path.join(fig_dir, "Fig4_scalar_ventilation.png"))
        ax_img4 = fig.add_axes([0.08, 0.54, 0.84, 0.42])
        ax_img4.imshow(fig4_img)
        ax_img4.axis('off')
        
        fig4_cap = "Figure 4 | Scalar ventilation dynamics, Local Mean Age of Air (LMA), and canopy dead zone mapping. a, CDF of air age normalized by residence time. b, Air exchange efficiency (ε_a). c, Mean canopy age vs τ0. d, Trapped recirculation fraction. e, Predicted canopy CO2 depletion."
        ax.text(0.08, 0.525, fig4_cap, fontsize=7.2, color=c_dark, va="top", linespacing=1.2, wrap=True)
        
        fig5_img = mpimg.imread(os.path.join(fig_dir, "Fig5_biosecurity_trades.png"))
        ax_img5 = fig.add_axes([0.08, 0.08, 0.84, 0.41])
        ax_img5.imshow(fig5_img)
        ax_img5.axis('off')
        
        fig5_cap = "Figure 5 | Habitat biosecurity, bioaerosol clearance, and crew exposure trade space. a, Bioaerosol clearance curves C(t)/C0. b, Cabin export percentage vs clearance speed k_clear. c, Surface deposition vs exhaust filtration. d, Two-dimensional architectural hardware trade matrix."
        ax.text(0.08, 0.065, fig5_cap, fontsize=7.2, color=c_dark, va="top", linespacing=1.2, wrap=True)
        
        pdf.savefig(fig)
        plt.close(fig)

        # =========================================================================
        # PAGE 7: Figure 6 (3D Spatial Flow Topologies) & 3D Topologies Discussion
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        fig6_img = mpimg.imread(os.path.join(fig_dir, "Fig6_3d_flow_topologies.png"))
        ax_img6 = fig.add_axes([0.08, 0.42, 0.84, 0.54])
        ax_img6.imshow(fig6_img)
        ax_img6.axis('off')
        
        fig6_cap = (
            "Figure 6 | 3D Spatial flow topologies, streamline ribbons, and canopy shear stress distributions. "
            "a, Microgreen Chamber: 3D confined jet core and lateral recirculation secondary eddies. "
            "b, NASA VEGGIE: 3D suction draft streamlines drawn through 4 base slots toward the overhead exhaust fan. "
            "c, NASA Advanced Plant Habitat (APH): 3D opposing lateral cross-jets colliding over the Science Carrier and sweeping upward. "
            "d, Quantitative canopy wall shear stress (τ_w) and turbulent kinetic energy (TKE) penetration across platforms."
        )
        ax.text(0.08, 0.40, fig6_cap, fontsize=7.5, color=c_dark, va="top", linespacing=1.25, wrap=True)
        
        ax.text(0.08, 0.32, "3D FLOW TOPOLOGY & TURBULENT RECIRCULATION", fontsize=9.5, fontweight="bold", color=c_nature_blue, va="top")
        f6_col1 = (
            "3D Streamline Structure & Flow Separation:\n"
            "The 3D streamline topologies (Fig. 6a–c) demonstrate fundamental\n"
            "differences in momentum delivery. In the Microgreen Chamber, the high-speed\n"
            "confined jet creates strong forward shear along the ceiling hood, driving\n"
            "secondary corner recirculation cells along the tray floor that trap 31.0%\n"
            "of the air volume.\n\n"
            "In VEGGIE, suction streamlines converge inward from all four base slots,\n"
            "channeling through pillow gaps. However, because flow is drawn by suction\n"
            "rather than blown by positive pressure, velocity drops rapidly with distance\n"
            "from the fan (proportional to 1/r^2), leaving the lower outer pillow corners poorly swept."
        )
        ax.text(0.08, 0.295, f6_col1, fontsize=7.5, color=c_dark, va="top", linespacing=1.2)
        
        f6_col2 = (
            "Opposing Jet Collision Dynamics in APH:\n"
            "In APH (Fig. 6c), the two opposing wall jets inject momentum directly across\n"
            "the Science Carrier surface. Upon meeting at the sagittal midline (x = 227 mm),\n"
            "their horizontal momentum converts into a uniform vertical updraft.\n\n"
            "This collision mechanism creates substantial turbulent kinetic energy\n"
            "(TKE = 11.9 × 10⁻³ m²/s²), enhancing scalar mixing and boundary-layer stripping\n"
            "without generating excessive leaf mechanical flapping stress (τ_w = 28.6 mPa,\n"
            "well below the 50 mPa threshold for mechanical damage)."
        )
        ax.text(0.50, 0.295, f6_col2, fontsize=7.5, color=c_dark, va="top", linespacing=1.2)
        
        pdf.savefig(fig)
        plt.close(fig)

        # =========================================================================
        # PAGE 8: Figure 7 (Airflow Extremes 3x4 Matrix) & Extremes Discussion
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        fig7_img = mpimg.imread(os.path.join(fig_dir, "Fig7_airflow_extremes.png"))
        ax_img7 = fig.add_axes([0.08, 0.42, 0.84, 0.54])
        ax_img7.imshow(fig7_img)
        ax_img7.axis('off')
        
        fig7_cap = (
            "Figure 7 | Operational airflow extremes and stagnation regimes across spaceflight plant growth hardware in microgravity. "
            "Comparative 3x4 coronal cross-sectional velocity matrix mapping Zero Airflow (Fan Failure), Low Draft (Flight Minimum / Seedling), "
            "Flight Nominal (Baseline), and High Blast (Maximum Blower) across Microgreen, VEGGIE, and APH chambers, with boundary layer conductance badges."
        )
        ax.text(0.08, 0.40, fig7_cap, fontsize=7.5, color=c_dark, va="top", linespacing=1.25, wrap=True)
        
        ax.text(0.08, 0.32, "OPERATIONAL EXTREMES & FAN FAILURE RISKS", fontsize=9.5, fontweight="bold", color=c_nature_blue, va="top")
        f7_col1 = (
            "Zero Airflow Stagnation Extreme (Microgravity Fan Failure):\n"
            "When mechanical ventilation ceases in microgravity (Fig. 7, Column 1),\n"
            "fluid velocity drops to zero everywhere (U = 0 m/s). Because natural thermal\n"
            "buoyancy is zero (Gr = 0), no convective plume can develop.\n\n"
            "Under this total stagnation regime, heat and mass transfer occur solely by\n"
            "molecular diffusion. The aerodynamic boundary layer expands unbounded\n"
            "(δ_bl > 25 mm), reducing conductance to g_bl < 0.04 mol m⁻² s⁻¹. Transpired\n"
            "water vapor rapidly saturates the canopy microclimate (RH -> 100%), while CO2\n"
            "is depleted within minutes, causing severe physiological hypoxia and death."
        )
        ax.text(0.08, 0.295, f7_col1, fontsize=7.5, color=c_dark, va="top", linespacing=1.2)
        
        f7_col2 = (
            "High Blast Extreme & Rapid Microclimate Recovery:\n"
            "At maximum airflow (Fig. 7, Column 4; APH 1.5 m/s, VEGGIE 140 m³/h,\n"
            "Microgreen 5.0 m/s), boundary layers are stripped down to δ_bl < 1.0 mm,\n"
            "elevating conductance to g_bl = 1.745 mol m⁻² s⁻¹ in APH.\n\n"
            "This high-flow regime enables rapid recovery from volatile surges or\n"
            "thermal spikes, clearing bioaerosols in t_50 = 7.2 s. However, in VEGGIE,\n"
            "operating at high blast accelerates spore export directly into the crew living\n"
            "cabin, highlighting the imperative of closed-loop filtration for high-speed BLSS."
        )
        ax.text(0.50, 0.295, f7_col2, fontsize=7.5, color=c_dark, va="top", linespacing=1.2)
        
        pdf.savefig(fig)
        plt.close(fig)

        # =========================================================================
        # PAGE 9: Methods, Table 4 (Biosecurity), References, Code Availability
        # =========================================================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        # Table 4 (Top of Page 9)
        ax.text(0.08, 0.95, "Table 4 | Ventilation efficiency, local age of air, and biosecurity containment dynamics across platforms.", fontsize=7.8, fontweight="bold", color="#111111", va="top")
        
        t4_headers = ["Chamber", "Gravity", "Flow Rate (Q)", "τ0 (s)", "Mean Age (s)", "Eff. ε_a (%)", "t50 (s)", "Biosecurity & Aerosol Fate"]
        t4_rows = [
            ["Microgreen", "1.0g", "11.8 m³/h", "0.71", "6.85", "10.4%", "14.2", "Sealed: zero cabin export; corner recirculation"],
            ["", "0.0g", "11.8 m³/h", "0.71", "5.20", "13.7%", "11.5", "Unstratified jet improves canopy clearance"],
            ["VEGGIE", "1.0g", "Low (42.5 m³/h)", "3.19", "14.20", "22.5%", "28.6", "Direct cabin exhaust: 100% spore export to ISS"],
            ["", "0.0g", "Low (42.5 m³/h)", "3.19", "22.40", "14.2%", "45.2", "Critical mold risk (52.8% stagnant volume)"],
            ["", "0.0g", "High (85.0 m³/h)", "1.60", "6.10", "26.2%", "13.8", "High fan restores boundary layer stripping"],
            ["APH", "1.0g", "Nom (26.4 m³/h)", "11.35", "24.80", "45.8%", "18.4", "Closed loop: internal HEPA filtration (≤25 ppb)"],
            ["", "0.0g", "Nom (26.4 m³/h)", "11.35", "25.20", "45.0%", "18.9", "Piston sweep maintains 45% efficiency"],
            ["", "0.0g", "High (66.0 m³/h)", "4.54", "9.60", "47.3%", "7.2", "Near-ideal displacement flow (ε_a -> 50%)"]
        ]
        table_ax4 = fig.add_axes([0.08, 0.72, 0.84, 0.20])
        table_ax4.axis('off')
        tab4 = table_ax4.table(cellText=t4_rows, colLabels=t4_headers, colWidths=[0.11, 0.08, 0.15, 0.08, 0.09, 0.09, 0.08, 0.32], cellLoc='left', loc='center')
        tab4.auto_set_font_size(False)
        tab4.set_fontsize(6.8)
        tab4.scale(1.0, 1.25)
        for (r, c), cell in tab4.get_celld().items():
            cell.set_edgecolor("#d0d0d0")
            if r == 0:
                cell.set_facecolor("#eef4f8")
                cell.set_text_props(weight='bold', color=c_nature_blue)
            else:
                if r % 2 == 0:
                    cell.set_facecolor("#fafbfc")
        
        # Methods Summary (2 Columns)
        ax.text(0.08, 0.69, "METHODS & MULTIMEDIA AVAILABILITY", fontsize=9.5, fontweight="bold", color=c_nature_blue, va="top")
        m_col1 = (
            "Numerical Discretization & Solver Settings:\n"
            "Simulations were executed within OpenFOAM v2606 using finite-volume\n"
            "discretization of the Low-Mach compressible Navier-Stokes equations:\n"
            "∂ρ/∂t + ∇·(ρu) = 0\n"
            "∂(ρu)/∂t + ∇·(ρuu) = -∇p_rgh - (g·r)∇ρ + ∇·[μ_eff(∇u + (∇u)^T - 2/3(∇·u)I)]\n"
            "∂(ρh)/∂t + ∇·(ρuh) = ∇·(α_eff ∇h) + ρ(u·g) + S_h\n\n"
            "Turbulence was modeled using the Shear Stress Transport (k-ω SST) model\n"
            "with prism boundary layers (y⁺ ~ 1-5). Discretization employed bounded\n"
            "second-order linear upwind schemes for momentum and enthalpy."
        )
        ax.text(0.08, 0.67, m_col1, fontsize=7.2, color=c_dark, va="top", linespacing=1.2)
        
        m_col2 = (
            "Interactive 3D & 4D Multimedia Assets:\n"
            "Interactive WebGL 3D visualizations, animated 4D time-resolved simulations,\n"
            "and all mesh dictionaries are openly accessible:\n"
            "• Interactive 3D Web Explorer: interactive_3d_explorer.html\n"
            "• 4D Jet Flapping & Vortex Shedding: 4D_microgreen_jet_flapping.gif\n"
            "• 4D VEGGIE Suction & Stagnation: 4D_veggie_suction_dynamics.gif\n"
            "• 4D APH Cross-Flow Collision: 4D_aph_lateral_collision.gif\n"
            "• 4D Bioaerosol Plume Dispersion: 4D_bioaerosol_plume_clearance.gif\n\n"
            "Open-Source Repository:\n"
            "https://github.com/HenryEwald/microgreen-chamber-cfd"
        )
        ax.text(0.50, 0.67, m_col2, fontsize=7.2, color=c_dark, va="top", linespacing=1.2)
        
        # References (Bottom Half)
        ax.text(0.08, 0.40, "REFERENCES", fontsize=9.5, fontweight="bold", color=c_nature_blue, va="top")
        refs = [
            "1. Massa, G. D. et al. VEG-01: Veggie hardware validation testing on the ISS. Open Agric. 2, 33–41 (2017).",
            "2. Morrow, R. C. et al. A new plant habitat facility for the ISS. 46th ICES, ICES-2016-320 (2016).",
            "3. Monje, O. et al. Hardware validation of the Advanced Plant Habitat on ISS. 49th ICES, ICES-2019-247 (2019).",
            "4. Wheeler, R. M. Agriculture for space: People and places paving the way. Open Agric. 2, 14–32 (2017).",
            "5. Kitaya, Y. et al. Effects of air current on transpiration and photosynthesis under microgravity. Adv. Space Res. 31, 177–182 (2003).",
            "6. Kitaya, Y. et al. Gas exchange and temperature gradients of leaves under microgravity. Adv. Space Res. 28, 565–570 (2001).",
            "7. Porterfield, D. M. Biophysical limitations in physiological transport in microgravity. Physiol. Plant. 114, 333–340 (2002).",
            "8. Musgrave, M. E. et al. Gravity independence of seed cycling in Brassica rapa. Planta 203, S110–S119 (1997).",
            "9. Paul, A.-L. & Ferl, R. J. Epigenomics in spaceflight: modifications under spaceflight stressors. Front. Genet. 8, 139 (2017).",
            "10. Farquhar, G. D., von Caemmerer, S. & Berry, J. A. A biochemical model of photosynthetic CO2 assimilation. Planta 149, 78–90 (1980).",
            "11. Menter, F. R. Two-equation eddy-viscosity turbulence models for engineering applications. AIAA J. 32, 1598–1605 (1994).",
            "12. Khodadad, C. L. M. et al. Microbiological analysis of lettuce grown on the ISS. Front. Plant Sci. 11, 199 (2020).",
            "13. Urbaniak, C. et al. Microbiomes of the ISS and comparison with human environments. Microbiome 6, 1–18 (2018).",
            "14. Zabel, P. et al. The EDEN ISS greenhouse for space research. Acta Astronaut. 128, 344–358 (2016).",
            "15. Ewald, H. & Barker, R. Microgreen Chamber CFD: 3D Internal-Flow and Gravity Parametric Analysis in OpenFOAM (2026)."
        ]
        ref_text = "\n".join(refs)
        ax.text(0.08, 0.38, ref_text, fontsize=6.8, color="#444444", va="top", linespacing=1.35)
        
        # Footer
        ax.text(0.50, 0.03, "npj Microgravity | Barker et al. | Purdue University Agricultural and Biological Engineering", fontsize=7.5, color=c_grey, ha="center")
        
        pdf.savefig(fig)
        plt.close(fig)

    print(f"=== Successfully Compiled 9-Page Publication PDF: {pdf_path} ===")

if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "npj_manuscript.pdf")
    generate_pdf(out_pdf)
