#!/usr/bin/env python3
"""
Figure 2: Dimensionless Richardson Number (Ri) Scaling and Convective Regime Trajectories.
Evaluates how natural convection collapses and forced momentum dominates across gravitational fields.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def create_fig2(output_dir):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=300)

    # Gravity array
    g_arr = np.linspace(0.001, 10.0, 500)
    beta = 1.0 / 295.15
    dt = 3.0

    # Hardware properties
    specs = {
        "Microgreen": {"L": 0.0967, "U": 0.262, "col": "#1f77b4", "mark": "o", "ls": "-"},
        "VEGGIE (Low Fan)": {"L": 0.3500, "U": 0.065, "col": "#2ca02c", "mark": "s", "ls": "--"},
        "VEGGIE (High Fan)": {"L": 0.3500, "U": 0.150, "col": "#2ca02c", "mark": "s", "ls": "-"},
        "APH (Low 0.3 m/s)": {"L": 0.4500, "U": 0.300, "col": "#d62728", "mark": "^", "ls": "--"},
        "APH (Nom 0.6 m/s)": {"L": 0.4500, "U": 0.600, "col": "#d62728", "mark": "^", "ls": "-"},
        "APH (High 1.5 m/s)": {"L": 0.4500, "U": 1.500, "col": "#d62728", "mark": "^", "ls": ":"},
    }

    # Panel A: Richardson Number vs. Gravity
    ax1.set_title("a  Richardson Number Scaling Across Gravity Regimes", fontsize=11, fontweight="bold", loc="left")
    for name, s in specs.items():
        ri = (g_arr * beta * dt * s["L"]) / (s["U"] ** 2)
        ax1.plot(g_arr, ri, label=name, color=s["col"], linestyle=s["ls"], lw=2.2)

    # Regime bands
    ax1.axhspan(1.0, 10.0, color="orange", alpha=0.15, label="Buoyancy-Dominated ($Ri > 1.0$)")
    ax1.axhspan(0.1, 1.0, color="yellow", alpha=0.12, label="Mixed Convection ($0.1 \\leq Ri \\leq 1.0$)")
    ax1.axhspan(0.0001, 0.1, color="cyan", alpha=0.12, label="Forced-Dominated ($Ri < 0.1$)")

    # Specific g markers
    g_targets = [("$\mu$g", 0.0), ("Moon", 1.62), ("Mars", 3.72), ("Earth", 9.81)]
    for lbl, g_val in g_targets:
        if g_val > 0:
            ax1.axvline(g_val, color="grey", linestyle=":", alpha=0.7)
            ax1.text(g_val + 0.1, 4.5, lbl, fontsize=8, rotation=90, color="black", fontweight="bold")

    ax1.set_yscale("log")
    ax1.set_xlim(0, 10)
    ax1.set_ylim(1e-3, 10)
    ax1.set_xlabel("Gravitational Acceleration $g$ [m/s²]", fontsize=10)
    ax1.set_ylabel("Richardson Number $Ri = Gr / Re^2$", fontsize=10)
    ax1.legend(loc="lower right", fontsize=8, ncol=2)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel B: Grashof Number vs Reynolds Number
    ax2.set_title("b  Grashof ($Gr$) vs. Reynolds ($Re$) Regime Map", fontsize=11, fontweight="bold", loc="left")
    for name, s in specs.items():
        nu = 1.516e-5
        re = s["U"] * s["L"] / nu
        gr_earth = 9.81 * beta * dt * (s["L"]**3) / (nu**2)
        gr_mars = 3.72 * beta * dt * (s["L"]**3) / (nu**2)
        gr_moon = 1.62 * beta * dt * (s["L"]**3) / (nu**2)
        
        ax2.scatter([re]*3, [gr_earth, gr_mars, gr_moon], color=s["col"], marker=s["mark"], s=80, zorder=5)
        ax2.plot([re]*3, [gr_earth, gr_mars, gr_moon], color=s["col"], linestyle="--", alpha=0.7)
        ax2.text(re * 1.05, gr_earth, f"{name} (1g)", fontsize=8, color=s["col"])

    # Diagonal lines for Ri = 1.0 and Ri = 0.1
    re_line = np.logspace(2.5, 4.8, 100)
    ax2.plot(re_line, 1.0 * (re_line**2), 'k--', lw=1.5, label="$Ri = 1.0$ (Transition)")
    ax2.plot(re_line, 0.1 * (re_line**2), 'k:', lw=1.5, label="$Ri = 0.1$ (Forced Limit)")

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlim(500, 60000)
    ax2.set_ylim(1e4, 1e8)
    ax2.set_xlabel("Reynolds Number $Re = U L / \\nu$", fontsize=10)
    ax2.set_ylabel("Grashof Number $Gr = g \\beta \\Delta T L^3 / \\nu^2$", fontsize=10)
    ax2.legend(loc="lower right", fontsize=8)
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Panel C: Thermal Stratification Index vs Gravity
    ax3.set_title("c  Thermal Stratification Decay ($1\\text{ g} \\to \\mu\\text{g}$)", fontsize=11, fontweight="bold", loc="left")
    g_discrete = np.array([0.0, 1.62, 3.72, 9.81])
    strat_micro = [0.00, 0.082, 0.185, 0.421]
    strat_veggie = [0.00, 0.145, 0.312, 0.684]
    strat_aph = [0.00, 0.015, 0.034, 0.089]

    ax3.plot(g_discrete, strat_micro, marker="o", lw=2.2, color="#1f77b4", label="Microgreen (Sealed)")
    ax3.plot(g_discrete, strat_veggie, marker="s", lw=2.2, color="#2ca02c", label="VEGGIE (Low Fan)")
    ax3.plot(g_discrete, strat_aph, marker="^", lw=2.2, color="#d62728", label="APH (Nominal 0.6 m/s)")

    ax3.set_xlabel("Gravitational Acceleration $g$ [m/s²]", fontsize=10)
    ax3.set_ylabel("Stratification Index $I_{strat} = \\Delta T_{top-bot} / \\overline{T}$", fontsize=10)
    ax3.set_xticks(g_discrete)
    ax3.set_xticklabels(["0g ($\mu$g)", "1.62g (Moon)", "3.72g (Mars)", "9.81g (Earth)"])
    ax3.legend(loc="upper left", fontsize=9)
    ax3.grid(True, linestyle=":", alpha=0.6)

    # Panel D: Unstirred Boundary Layer Thickness vs. Gravity
    ax4.set_title("d  Canopy Aerodynamic Resistance ($r_a = 1/g_{bl}$) Transition", fontsize=11, fontweight="bold", loc="left")
    ra_micro = [1.45, 1.43, 1.40, 1.38]
    ra_veggie_low = [4.56, 3.70, 3.25, 2.76]
    ra_veggie_high = [1.94, 1.89, 1.86, 1.81]
    ra_aph = [0.93, 0.92, 0.91, 0.90]

    ax4.plot(g_discrete, ra_veggie_low, marker="s", lw=2.2, linestyle="--", color="#2ca02c", label="VEGGIE (Low Fan)")
    ax4.plot(g_discrete, ra_veggie_high, marker="s", lw=2.2, color="#2ca02c", label="VEGGIE (High Fan)")
    ax4.plot(g_discrete, ra_micro, marker="o", lw=2.2, color="#1f77b4", label="Microgreen")
    ax4.plot(g_discrete, ra_aph, marker="^", lw=2.2, color="#d62728", label="APH (0.6 m/s)")

    ax4.set_xlabel("Gravitational Acceleration $g$ [m/s²]", fontsize=10)
    ax4.set_ylabel("Boundary Layer Resistance $r_a$ [m² s / mol]", fontsize=10)
    ax4.set_xticks(g_discrete)
    ax4.set_xticklabels(["0g ($\mu$g)", "1.62g (Moon)", "3.72g (Mars)", "9.81g (Earth)"])
    ax4.legend(loc="upper right", fontsize=9)
    ax4.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    png_out = os.path.join(output_dir, "Fig2_gravity_richardson.png")
    pdf_out = os.path.join(output_dir, "Fig2_gravity_richardson.pdf")
    plt.savefig(png_out, dpi=300)
    plt.savefig(pdf_out)
    plt.close()
    print(f"Generated Figure 2: {png_out}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    create_fig2(out)
