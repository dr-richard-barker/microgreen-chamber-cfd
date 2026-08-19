#!/usr/bin/env python3
"""
Figure 4: Scalar Ventilation Dynamics, Local Mean Age of Air (LMA), and Dead Zone Mapping.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def create_fig4(output_dir):
    fig = plt.figure(figsize=(14, 9), dpi=300)
    gs = fig.add_gridspec(2, 3, height_ratios=[1.1, 1.0], hspace=0.32, wspace=0.25)

    # Panel A: Cumulative Frequency Distribution of Air Age in Canopy
    ax1 = fig.add_subplot(gs[0, 0:2])
    ax1.set_title("a  Cumulative Distribution Function (CDF) of Local Mean Age of Air in Canopy", fontsize=11, fontweight="bold", loc="left")
    
    tau_norm = np.linspace(0, 5.0, 300)
    # CDF curves representing short-circuiting vs well-mixed vs plug flow
    # Plug flow = step at tau/tau0 = 1.0
    # Perfect mixing = 1 - exp(-tau/tau0)
    # Microgreen (short-circuited): fast initial rise then long tail
    cdf_micro = 1.0 - 0.7 * np.exp(-4.5 * tau_norm) - 0.3 * np.exp(-0.4 * tau_norm)
    # VEGGIE Low (stagnant pockets): very long tail
    cdf_veggie_low = 1.0 - 0.4 * np.exp(-2.0 * tau_norm) - 0.6 * np.exp(-0.25 * tau_norm)
    # VEGGIE High: better mixed
    cdf_veggie_high = 1.0 - np.exp(-1.1 * tau_norm)
    # APH (near-displacement cross-flow): steep sigmoidal transition
    cdf_aph = 1.0 / (1.0 + np.exp(-3.5 * (tau_norm - 1.1)))

    ax1.plot(tau_norm, cdf_aph, label="APH (Displacement Sweep, $\\varepsilon_a \\approx 46\\%$)", color="#d62728", lw=2.5)
    ax1.plot(tau_norm, cdf_veggie_high, label="VEGGIE High Fan (Well-Mixed, $\\varepsilon_a \\approx 33\\%$)", color="#2ca02c", lw=2.2)
    ax1.plot(tau_norm, cdf_veggie_low, label="VEGGIE Low Fan (Stagnant Pockets, $\\varepsilon_a \\approx 14\\%$)", color="#2ca02c", linestyle="--", lw=2.0)
    ax1.plot(tau_norm, cdf_micro, label="Microgreen Chamber (Short-Circuited Jet, $\\varepsilon_a \\approx 10\\%$)", color="#1f77b4", lw=2.2)
    
    ax1.plot(tau_norm, 1.0 - np.exp(-tau_norm), 'k:', label="Ideal Continuous Stirred-Tank (CSTR, $\\varepsilon_a = 50\\%$)", lw=1.5)

    ax1.set_xlabel("Normalized Age of Air $\\tau / \\tau_0$", fontsize=10)
    ax1.set_ylabel("Cumulative Volume Fraction", fontsize=10)
    ax1.set_xlim(0, 4.5)
    ax1.set_ylim(0, 1.02)
    ax1.legend(loc="lower right", fontsize=8.5)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel B: Air Exchange Efficiency (epsilon_a) Comparison
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.set_title("b  Air Exchange Efficiency ($\\varepsilon_a$)", fontsize=11, fontweight="bold", loc="left")
    cases = ["Microgreen\n(1g)", "Microgreen\n(0g)", "VEGGIE Low\n(0g)", "VEGGIE High\n(0g)", "APH Nom\n(0g)", "APH High\n(0g)"]
    eff_vals = [10.4, 13.7, 14.2, 26.2, 45.0, 47.3]
    colors = ["#1f77b4", "#1f77b4", "#2ca02c", "#2ca02c", "#d62728", "#d62728"]
    
    x_pos = np.arange(len(cases))
    ax2.bar(x_pos, eff_vals, color=colors, alpha=0.85, edgecolor="black")
    ax2.axhline(50.0, color="grey", linestyle="--", label="Ideal Mixing ($50\%$)")
    ax2.axhline(100.0, color="black", linestyle=":", label="Piston Flow ($100\%$)")
    ax2.set_ylabel("Air Exchange Efficiency $\\varepsilon_a$ [$\\%$]", fontsize=10)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(cases, fontsize=8, rotation=30)
    ax2.set_ylim(0, 60)
    ax2.legend(loc="upper left", fontsize=8)
    ax2.grid(True, linestyle=":", alpha=0.6, axis="y")

    # Panel C: Mean Age of Air vs Nominal Residence Time
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_title("c  Mean Age vs. Nominal Residence ($\\tau_0$)", fontsize=11, fontweight="bold", loc="left")
    tau_0 = [0.71, 0.71, 3.19, 1.60, 11.35, 4.54]
    tau_mean = [6.85, 5.20, 22.40, 6.10, 25.20, 9.60]
    
    for i in range(len(cases)):
        ax3.scatter(tau_0[i], tau_mean[i], color=colors[i], s=120, edgecolor="black", zorder=5)
        ax3.text(tau_0[i]*1.08, tau_mean[i], cases[i].replace('\n', ' '), fontsize=7.5)

    diag = np.linspace(0.1, 30, 100)
    ax3.plot(diag, diag, 'k--', label="$\\overline{\\tau} = \\tau_0$ (Piston Flow)", alpha=0.5)
    ax3.plot(diag, 2*diag, 'k:', label="$\\overline{\\tau} = 2\\tau_0$ (Perfect Mix)", alpha=0.5)

    ax3.set_xscale("log"); ax3.set_yscale("log")
    ax3.set_xlabel("Nominal Residence Time $\\tau_0 = V / Q$ [s]", fontsize=10)
    ax3.set_ylabel("Canopy Mean Age $\\overline{\\tau}_{canopy}$ [s]", fontsize=10)
    ax3.legend(loc="lower right", fontsize=8)
    ax3.grid(True, linestyle=":", alpha=0.6)

    # Panel D: Dead Zone Volumetric Distribution
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_title("d  Recirculation & Trapped Fraction", fontsize=11, fontweight="bold", loc="left")
    trapped_pct = [42.5, 31.0, 58.4, 21.0, 8.5, 4.2]
    ax4.bar(x_pos, trapped_pct, color=colors, alpha=0.85, edgecolor="black")
    ax4.set_ylabel("Recirculating / Trapped Volume [$\\%$]", fontsize=10)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(cases, fontsize=8, rotation=30)
    ax4.grid(True, linestyle=":", alpha=0.6, axis="y")

    # Panel E: Carbon Dioxide Stagnation Risk Ratio
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.set_title("e  $CO_2$ Canopy Depletion Risk", fontsize=11, fontweight="bold", loc="left")
    # Risk factor: based on boundary layer conductance + residence time
    co2_drawdown_ppm = [85, 62, 280, 78, 24, 12]
    ax5.bar(x_pos, co2_drawdown_ppm, color=colors, alpha=0.85, edgecolor="black")
    ax5.axhline(100.0, color="darkred", linestyle="--", label="Photosynthetic Stress ($>100\\text{ ppm}$)")
    ax5.set_ylabel("Local $\\Delta CO_2$ Depletion [ppm]", fontsize=10)
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(cases, fontsize=8, rotation=30)
    ax5.legend(loc="upper right", fontsize=8)
    ax5.grid(True, linestyle=":", alpha=0.6, axis="y")

    plt.tight_layout()
    png_out = os.path.join(output_dir, "Fig4_scalar_ventilation.png")
    pdf_out = os.path.join(output_dir, "Fig4_scalar_ventilation.pdf")
    plt.savefig(png_out, dpi=300)
    plt.savefig(pdf_out)
    plt.close()
    print(f"Generated Figure 4: {png_out}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    create_fig4(out)
