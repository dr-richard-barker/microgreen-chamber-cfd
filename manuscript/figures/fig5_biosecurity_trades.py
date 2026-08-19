#!/usr/bin/env python3
"""
Figure 5: Biosecurity, Pathogen Containment, and Bioaerosol Dispersion Trade Space.
Compares closed-loop HEPA filtration (APH), sealed phenotyping (Microgreen), and open cabin export (VEGGIE).
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def create_fig5(output_dir):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=300)

    # Panel A: Transient Bioaerosol Clearance Curves (Normalized Concentration vs Time)
    ax1.set_title("a  Bioaerosol Clearance Dynamics from Plant Canopy", fontsize=11, fontweight="bold", loc="left")
    t = np.linspace(0, 120, 300)
    # Concentration decay: C(t) = C0 * exp(-t / t_decay)
    # APH High (7.2s): ultra fast HEPA scrub
    c_aph_high = np.exp(-t / (7.2 / np.log(2)))
    # APH Nom (18.4s): nominal HEPA scrub
    c_aph_nom = np.exp(-t / (18.4 / np.log(2)))
    # VEGGIE High (13.8s to cabin export)
    c_veggie_high = np.exp(-t / (13.8 / np.log(2)))
    # VEGGIE Low (45.2s): slow stagnant decay
    c_veggie_low = np.exp(-t / (45.2 / np.log(2)))
    # Microgreen (14.2s internal recirculation)
    c_micro = np.exp(-t / (14.2 / np.log(2)))

    ax1.plot(t, c_aph_high, label="APH High ($t_{50} = 7.2\\text{ s}$, Closed HEPA)", color="#d62728", lw=2.2, linestyle=":")
    ax1.plot(t, c_aph_nom, label="APH Nominal ($t_{50} = 18.4\\text{ s}$, Closed HEPA)", color="#d62728", lw=2.5)
    ax1.plot(t, c_veggie_high, label="VEGGIE High ($t_{50} = 13.8\\text{ s}$, Cabin Export)", color="#2ca02c", lw=2.2)
    ax1.plot(t, c_veggie_low, label="VEGGIE Low ($t_{50} = 45.2\\text{ s}$, Stagnant Risk)", color="#2ca02c", lw=2.0, linestyle="--")
    ax1.plot(t, c_micro, label="Microgreen ($t_{50} = 14.2\\text{ s}$, Sealed)", color="#1f77b4", lw=2.0)

    ax1.axhline(0.5, color="grey", linestyle="--", alpha=0.6, label="Half-Life ($t_{50}$ Threshold)")
    ax1.set_xlabel("Time Post-Aerosolization $t$ [seconds]", fontsize=10)
    ax1.set_ylabel("Normalized Airborne Concentration $C(t) / C_0$", fontsize=10)
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 1.02)
    ax1.legend(loc="upper right", fontsize=8.5)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel B: Cabin Bioaerosol Burden vs Internal Plant Clearance
    ax2.set_title("b  Habitat Biosecurity: Cabin Export Fraction vs. Plant Clearance", fontsize=11, fontweight="bold", loc="left")
    
    # Scatter of Hardware Biosecurity Quadrants
    # X-axis: Plant canopy clearance speed (1 / t50) [1/s]
    # Y-axis: Cumulative fraction exported to astronaut living quarters [%]
    clearance_speed = [1.0/14.2, 1.0/45.2, 1.0/13.8, 1.0/18.4, 1.0/7.2]
    cabin_export = [0.0, 100.0, 100.0, 0.0, 0.0]
    names = ["Microgreen\n(Sealed)", "VEGGIE Low\n(Open)", "VEGGIE High\n(Open)", "APH Nominal\n(Closed HEPA)", "APH High\n(Closed HEPA)"]
    colors = ["#1f77b4", "#2ca02c", "#2ca02c", "#d62728", "#d62728"]

    ax2.scatter(clearance_speed, cabin_export, color=colors, s=180, edgecolor="black", zorder=5)
    for i, txt in enumerate(names):
        offset_y = -8 if cabin_export[i] > 50 else 6
        ax2.text(clearance_speed[i], cabin_export[i] + offset_y, txt, ha="center", fontsize=8.5, fontweight="bold", color=colors[i])

    ax2.axhspan(50, 105, color="red", alpha=0.1, label="High Crew Exposure Zone (Open Cabin Coupling)")
    ax2.axhspan(-5, 20, color="green", alpha=0.1, label="Biosecure Containment Zone (Closed / Sealed)")

    ax2.set_xlabel("Canopy Clearance Velocity Metric $k_{clear} = 1 / t_{50}$ [s⁻¹]", fontsize=10)
    ax2.set_ylabel("Bioaerosol / Spore Fraction Exported to ISS Cabin [$\\%$]", fontsize=10)
    ax2.set_xlim(0.01, 0.16)
    ax2.set_ylim(-10, 115)
    ax2.legend(loc="center right", fontsize=8.5)
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Panel C: Spore Deposition vs Flow Regime
    ax3.set_title("c  Estimated Surface Deposition vs. Exhaust Capture Fraction", fontsize=11, fontweight="bold", loc="left")
    categories = ["Microgreen\n(1g)", "VEGGIE Low\n(0g)", "VEGGIE High\n(0g)", "APH Nom\n(0g)", "APH High\n(0g)"]
    wall_dep = [62.0, 48.0, 18.0, 12.0, 5.0]
    filter_or_exit = [38.0, 52.0, 82.0, 88.0, 95.0]
    
    x = np.arange(len(categories))
    w = 0.55
    ax3.bar(x, wall_dep, width=w, label="Wall / Leaf Deposition [$\\%$]", color="#d95f02", alpha=0.85)
    ax3.bar(x, filter_or_exit, width=w, bottom=wall_dep, label="Exhaust / Filter Capture [$\\%$]", color="#7570b3", alpha=0.85)
    
    ax3.set_ylabel("Aerosol Particle Fate Fraction [$\\%$]", fontsize=10)
    ax3.set_xticks(x)
    ax3.set_xticklabels(categories, fontsize=8.5)
    ax3.legend(loc="upper right", fontsize=8.5)
    ax3.grid(True, linestyle=":", alpha=0.6, axis="y")

    # Panel D: Architectural Biosecurity Trade Space Matrix
    ax4.set_title("d  Hardware Design Matrix: Enclosure vs. Aerodynamic Control", fontsize=11, fontweight="bold", loc="left")
    
    # 2D Trade Space
    # X: Enclosure Isolation Level (0=Open, 1=Sealed, 2=Closed-Loop Engineered)
    # Y: Aerodynamic Boundary Layer Control (0=Passive, 1=Weak, 2=Engineered Uniform)
    ax4.scatter([0.2], [0.3], s=250, color="#2ca02c", marker="s", edgecolor="black", label="VEGGIE (Open Garden)")
    ax4.scatter([1.0], [0.8], s=250, color="#1f77b4", marker="o", edgecolor="black", label="Microgreen (Sealed Chamber)")
    ax4.scatter([1.8], [1.8], s=300, color="#d62728", marker="^", edgecolor="black", label="APH (Closed Phytotron)")

    ax4.text(0.2, 0.42, "VEGGIE:\nHigh Cabin Exchange,\nLow BL Control", ha="center", fontsize=8, color="#2ca02c")
    ax4.text(1.0, 0.95, "Microgreen:\nHigh Isolation,\nUnsteady Jet", ha="center", fontsize=8, color="#1f77b4")
    ax4.text(1.8, 1.55, "APH:\nHigh Isolation,\nPrecision Uniformity", ha="center", fontsize=8, color="#d62728")

    ax4.set_xlim(-0.1, 2.2)
    ax4.set_ylim(-0.1, 2.2)
    ax4.set_xticks([0.2, 1.0, 1.8])
    ax4.set_xticklabels(["Cabin-Coupled\n(Open)", "Sealed Enclosure\n(Passive/Simple)", "Closed-Loop\n(Active Phytotron)"], fontsize=8.5)
    ax4.set_yticks([0.3, 1.0, 1.8])
    ax4.set_yticklabels(["Low Control\n(Mixed/Plume)", "Moderate Control\n(Confined Jet)", "High Control\n(Ducted Sweep)"], fontsize=8.5)
    ax4.set_xlabel("Atmospheric Enclosure & Cabin Interface", fontsize=10)
    ax4.set_ylabel("Canopy Aerodynamic Control Level", fontsize=10)
    ax4.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    png_out = os.path.join(output_dir, "Fig5_biosecurity_trades.png")
    pdf_out = os.path.join(output_dir, "Fig5_biosecurity_trades.pdf")
    plt.savefig(png_out, dpi=300)
    plt.savefig(pdf_out)
    plt.close()
    print(f"Generated Figure 5: {png_out}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    create_fig5(out)
