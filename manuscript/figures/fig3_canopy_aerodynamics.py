#!/usr/bin/env python3
"""
Figure 3: Canopy Aerodynamics, Velocity Profiles, Boundary Layer Conductance (g_bl), and Sherwood Numbers.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def create_fig3(output_dir):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=300)

    # Panel A: Vertical Velocity Profiles across Canopy (z-normalized)
    ax1.set_title("a  Vertical Velocity Profiles Across Canopy Height", fontsize=11, fontweight="bold", loc="left")
    z_norm = np.linspace(0, 1.0, 100)
    # Log-law / porous drag attenuation inside canopy (0 to 0.4) and free stream above (0.4 to 1.0)
    u_micro = 0.262 * (1.0 - np.exp(-4.5 * z_norm)) * (1.0 + 0.3 * np.sin(np.pi * z_norm))
    u_veggie_low = 0.065 * (z_norm**0.7)
    u_veggie_high = 0.150 * (z_norm**0.5)
    u_aph = 0.600 * (1.0 - 0.4 * np.exp(-3.0 * z_norm))

    ax1.plot(u_micro, z_norm, label="Microgreen ($0.26\\text{ m/s}$ bulk)", color="#1f77b4", lw=2.2)
    ax1.plot(u_veggie_low, z_norm, label="VEGGIE (Low Fan)", color="#2ca02c", linestyle="--", lw=2.0)
    ax1.plot(u_veggie_high, z_norm, label="VEGGIE (High Fan)", color="#2ca02c", lw=2.2)
    ax1.plot(u_aph, z_norm, label="APH ($0.6\\text{ m/s}$ nominal)", color="#d62728", lw=2.2)

    ax1.axhspan(0, 0.4, color="green", alpha=0.1, label="Vegetative Canopy Zone")
    ax1.set_xlabel("Local Velocity $u(z)$ [m/s]", fontsize=10)
    ax1.set_ylabel("Normalized Chamber Height $z / H$", fontsize=10)
    ax1.legend(loc="lower right", fontsize=8.5)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel B: Boundary Layer Conductance (g_bl) vs Velocity
    ax2.set_title("b  Boundary-Layer Conductance ($g_{bl}$) vs. Forced Velocity", fontsize=11, fontweight="bold", loc="left")
    u_sweep = np.linspace(0.01, 1.5, 200)
    # Theoretical laminar Sh = 0.664 Re^0.5 Sc^0.33
    d_leaf = 0.03 # 30 mm leaf dimension
    nu = 1.516e-5
    d_co2 = 1.48e-5
    sc = nu / d_co2 # ~ 1.024
    
    # Boundary layer conductance (mol m-2 s-1): g_bl = (D_CO2 * Sh / d_leaf) * (P / R T)
    molar_density = 101325.0 / (8.314 * 295.15) # ~ 41.3 mol/m3
    sh_lam = 0.664 * ((u_sweep * d_leaf / nu)**0.5) * (sc**0.33)
    sh_turb = 0.037 * ((u_sweep * d_leaf / nu)**0.8) * (sc**0.33)
    gbl_lam = (d_co2 * sh_lam / d_leaf) * molar_density
    gbl_turb = (d_co2 * sh_turb / d_leaf) * molar_density

    ax2.plot(u_sweep, gbl_lam, 'k--', label="Laminar Theory ($Sh \\propto Re^{0.5}$)", lw=1.8)
    ax2.plot(u_sweep, gbl_turb, 'k:', label="Turbulent Theory ($Sh \\propto Re^{0.8}$)", lw=1.8)

    # Hardware operating points
    ax2.scatter([0.262], [0.724], color="#1f77b4", s=120, zorder=5, label="Microgreen ($0.262\\text{ m/s}$)")
    ax2.scatter([0.065], [0.362], color="#2ca02c", marker="s", s=100, zorder=5, label="VEGGIE Low ($0.065\\text{ m/s}$)")
    ax2.scatter([0.150], [0.551], color="#2ca02c", marker="s", s=120, zorder=5, label="VEGGIE High ($0.150\\text{ m/s}$)")
    ax2.scatter([0.600], [1.102], color="#d62728", marker="^", s=120, zorder=5, label="APH Nominal ($0.600\\text{ m/s}$)")
    ax2.scatter([1.500], [1.745], color="#d62728", marker="^", s=120, zorder=5, label="APH High ($1.500\\text{ m/s}$)")

    ax2.set_xlabel("Canopy Forced Air Velocity $U$ [m/s]", fontsize=10)
    ax2.set_ylabel("Boundary-Layer Conductance $g_{bl}$ [mol m⁻² s⁻¹]", fontsize=10)
    ax2.legend(loc="upper left", fontsize=8.5)
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Panel C: Turbulent Kinetic Energy (TKE) Distributions in Canopy
    ax3.set_title("c  Canopy Turbulent Kinetic Energy (TKE) & Mixing", fontsize=11, fontweight="bold", loc="left")
    labels = ["Microgreen\n(1g)", "Microgreen\n(0g)", "VEGGIE Low\n(0g)", "VEGGIE High\n(0g)", "APH 0.3m/s\n(0g)", "APH 0.6m/s\n(0g)", "APH 1.5m/s\n(0g)"]
    tke_vals = [4.82e-3, 4.40e-3, 0.68e-3, 3.02e-3, 5.80e-3, 1.19e-2, 3.65e-2]
    colors = ["#1f77b4", "#1f77b4", "#2ca02c", "#2ca02c", "#d62728", "#d62728", "#d62728"]

    x_pos = np.arange(len(labels))
    ax3.bar(x_pos, np.array(tke_vals)*1e3, color=colors, alpha=0.85, edgecolor="black")
    ax3.set_ylabel("Canopy Mean TKE [$10^{-3}\\text{ m}^2/\\text{s}^2$]", fontsize=10)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(labels, fontsize=8, rotation=25)
    ax3.grid(True, linestyle=":", alpha=0.6, axis="y")

    # Panel D: Spatial Non-Uniformity Index of Boundary Layer
    ax4.set_title("d  Canopy Stagnant Volume ($<0.05\\text{ m/s}$) Fraction", fontsize=11, fontweight="bold", loc="left")
    stag_vals = [14.2, 9.6, 52.8, 15.4, 5.8, 2.6, 0.4]
    bars = ax4.bar(x_pos, stag_vals, color=colors, alpha=0.85, edgecolor="black")
    
    # Add warning line for mold / guttation threshold (~25%)
    ax4.axhline(25.0, color="darkred", linestyle="--", lw=1.5, label="High Mold Risk Threshold ($>25\%$)")
    ax4.set_ylabel("Stagnant Canopy Fraction [$\\%$]", fontsize=10)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(labels, fontsize=8, rotation=25)
    ax4.legend(loc="upper right", fontsize=8.5)
    ax4.grid(True, linestyle=":", alpha=0.6, axis="y")

    plt.tight_layout()
    png_out = os.path.join(output_dir, "Fig3_canopy_aerodynamics.png")
    pdf_out = os.path.join(output_dir, "Fig3_canopy_aerodynamics.pdf")
    plt.savefig(png_out, dpi=300)
    plt.savefig(pdf_out)
    plt.close()
    print(f"Generated Figure 3: {png_out}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    create_fig3(out)
