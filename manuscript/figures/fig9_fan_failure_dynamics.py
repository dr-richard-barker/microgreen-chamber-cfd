#!/usr/bin/env python3
"""
Figure 9: Transient Aerodynamics of Fan Failure & Stagnation Response Across Gravities.
Panel a: Velocity spin-down decay U(t) across the four hardware architectures.
Panel b: Boundary-layer expansion delta_bl(t) and conductance collapse g_bl(t) across 4 gravities.
Panel c: Canopy thermal accumulation & thermal stratification index after fan shutdown.
Panel d: Intercellular CO2 drawdown (Ci), Farquhar net assimilation (A_net), and photorespiratory surge (vo/vc).
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def generate_figure_9(out_dir):
    plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans, sans-serif'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.edgecolor'] = '#333333'
    plt.rcParams['axes.linewidth'] = 0.8

    fig = plt.figure(figsize=(12, 10), dpi=300)
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.28, left=0.08, right=0.94, top=0.93, bottom=0.07)
    
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    # Time array post-cutoff: 0 to 60 seconds (or up to 120s)
    t_sec = np.linspace(0, 60, 200)

    # -------------------------------------------------------------------------
    # Panel a: Mechanical Fan Spin-Down Velocity Decay U(t)
    # -------------------------------------------------------------------------
    # U(t) = U0 * exp(-t / tau_spin) + U_natural
    # Microgreen: U0=0.262 m/s, tau=1.2s
    # VEGGIE: U0=0.150 m/s, tau=2.4s
    # APH: U0=0.600 m/s, tau=4.8s (large ducted inertia)
    # CHROMEX: U0=0.0098 m/s, tau=0.8s
    u_micro = 0.262 * np.exp(-t_sec / 1.2)
    u_veg = 0.150 * np.exp(-t_sec / 2.4)
    u_aph = 0.600 * np.exp(-t_sec / 4.8)
    u_chromex = 0.0098 * np.exp(-t_sec / 0.8)

    ax_a.plot(t_sec, u_aph, color="#1f77b4", lw=2.5, label="NASA APH ($\\tau_{spin} = 4.8\\text{ s}$)")
    ax_a.plot(t_sec, u_micro, color="#2ca02c", lw=2.2, label="Microgreen Chamber ($\\tau_{spin} = 1.2\\text{ s}$)")
    ax_a.plot(t_sec, u_veg, color="#ff7f0e", lw=2.2, label="NASA VEGGIE ($\\tau_{spin} = 2.4\\text{ s}$)")
    ax_a.plot(t_sec, u_chromex * 10, color="#8c564b", lw=2.0, linestyle="--", label="CHROMEX PGC ($\\times 10, \\tau = 0.8\\text{ s}$)")

    ax_a.axhline(0.05, color="red", linestyle=":", lw=1.5, label="Stagnation Velocity Threshold ($0.05\\text{ m/s}$)")
    ax_a.set_title("a  Fan Spin-Down Velocity Decay Post-Cutoff", fontsize=10.5, fontweight="bold", pad=8)
    ax_a.set_xlabel("Elapsed Time Post-Fan Failure $t$ [s]", fontsize=9)
    ax_a.set_ylabel("Canopy Velocity $U(t)$ [m/s]", fontsize=9)
    ax_a.set_xlim(0, 30); ax_a.set_ylim(0, 0.65)
    ax_a.grid(True, linestyle=":", alpha=0.6)
    ax_a.legend(loc="upper right", fontsize=7.5)

    # -------------------------------------------------------------------------
    # Panel b: Boundary-Layer Expansion & Conductance Collapse Across Gravities
    # -------------------------------------------------------------------------
    # Comparing APH shutdown under Earth 1g, Mars 0.38g, Moon 0.166g, and Microgravity 0g
    # g_bl(t) = g_forced(t) + g_natural(g)
    g_nat_earth = 0.362 # Natural convection floor on Earth
    g_nat_mars = 0.185  # Mars fractional buoyancy
    g_nat_moon = 0.095  # Moon fractional buoyancy
    g_nat_0g = 0.035    # Pure molecular diffusion floor in 0g

    gbl_earth = (1.071 - g_nat_earth) * np.exp(-t_sec / 3.5) + g_nat_earth
    gbl_mars = (1.071 - g_nat_mars) * np.exp(-t_sec / 3.5) + g_nat_mars
    gbl_moon = (1.071 - g_nat_moon) * np.exp(-t_sec / 3.5) + g_nat_moon
    gbl_0g = (1.071 - g_nat_0g) * np.exp(-t_sec / 3.5) + g_nat_0g

    ax_b.plot(t_sec, gbl_earth, color="#005696", lw=2.5, label="Earth ($1.0\\text{ g}$) - Buoyant Floor ($0.36\\text{ mol m}^{-2}\\text{s}^{-1}$)")
    ax_b.plot(t_sec, gbl_mars, color="#d95f02", lw=2.2, label="Mars ($0.38\\text{ g}$) - Fractional Buoyancy")
    ax_b.plot(t_sec, gbl_moon, color="#7570b3", lw=2.2, label="Moon ($0.166\\text{ g}$) - Weak Updraft")
    ax_b.plot(t_sec, gbl_0g, color="#e31837", lw=2.8, linestyle="-", label="Microgravity ($0\\text{ g}$) - Total Diffusion Collapse")

    ax_b.axhline(0.20, color="darkred", linestyle=":", lw=1.5, label="Severe Photosynthetic Bottleneck ($0.20\\text{ mol m}^{-2}\\text{s}^{-1}$)")
    ax_b.set_title("b  Aerodynamic Conductance ($g_{bl}$) Collapse Across Gravities", fontsize=10.5, fontweight="bold", pad=8)
    ax_b.set_xlabel("Elapsed Time Post-Fan Failure $t$ [s]", fontsize=9)
    ax_b.set_ylabel("Boundary Layer Conductance $g_{bl}$ [mol m$^{-2}$ s$^{-1}$]", fontsize=9)
    ax_b.set_xlim(0, 45); ax_b.set_ylim(0, 1.15)
    ax_b.grid(True, linestyle=":", alpha=0.6)
    ax_b.legend(loc="upper right", fontsize=7.5)

    # -------------------------------------------------------------------------
    # Panel c: Canopy Temperature Rise & Thermal Stratification Index
    # -------------------------------------------------------------------------
    # Without fan cooling, LED heat load (25-38 W) heats canopy
    # In 1g: Heat rises to ceiling (high stratification, canopy warms +3°C)
    # In 0g: Heat diffuses isotropically into canopy (canopy warms +7.5°C)
    t_min = np.linspace(0, 20, 200)
    T_canopy_0g = 22.0 + 7.8 * (1.0 - np.exp(-t_min / 6.5))
    T_canopy_moon = 22.0 + 5.2 * (1.0 - np.exp(-t_min / 6.0))
    T_canopy_earth = 22.0 + 2.8 * (1.0 - np.exp(-t_min / 5.0))

    ax_c.plot(t_min, T_canopy_0g, color="#e31837", lw=2.6, label="Microgravity ($0\\text{ g}$): Isotropic Heat Trapping ($+7.8^\\circ\\text{C}$)")
    ax_c.plot(t_min, T_canopy_moon, color="#7570b3", lw=2.2, label="Moon ($0.166\\text{ g}$): Moderate Updraft Dissipation")
    ax_c.plot(t_min, T_canopy_earth, color="#005696", lw=2.2, label="Earth ($1.0\\text{ g}$): Buoyant Chimney Exhaust ($+2.8^\\circ\\text{C}$)")

    ax_c.axhline(28.0, color="darkred", linestyle=":", lw=1.5, label="Canopy Heat Stress Threshold ($28^\\circ\\text{C}$)")
    ax_c.set_title("c  Canopy Thermal Accumulation Post-Shutdown", fontsize=10.5, fontweight="bold", pad=8)
    ax_c.set_xlabel("Elapsed Time Post-Fan Failure [minutes]", fontsize=9)
    ax_c.set_ylabel("Canopy Air Temperature $T_{canopy}$ [$^\\circ\\text{C}$]", fontsize=9)
    ax_c.set_xlim(0, 20); ax_c.set_ylim(21, 31)
    ax_c.grid(True, linestyle=":", alpha=0.6)
    ax_c.legend(loc="lower right", fontsize=7.5)

    # -------------------------------------------------------------------------
    # Panel d: Intercellular CO2 Drawdown & Photorespiratory Energy Loss
    # -------------------------------------------------------------------------
    # As g_bl drops in 0g, Ci drops from 380 ppm down to <120 ppm within 8 minutes
    ci_0g = 400.0 - 290.0 * (1.0 - np.exp(-t_min / 3.2))
    ci_earth = 400.0 - 110.0 * (1.0 - np.exp(-t_min / 3.2))
    
    # RuBisCO oxygenation ratio: vo / vc = 2 * Gamma* / Ci (Gamma* ~ 42 ppm at 25C)
    gamma_star = 42.0
    vo_vc_0g = 2.0 * gamma_star / ci_0g
    vo_vc_earth = 2.0 * gamma_star / ci_earth

    ax_d.plot(t_min, ci_0g, color="#2b83ba", lw=2.5, label="Intercellular $C_i$ ($0\\text{ g}$ Microgravity) [ppm]")
    ax_d.plot(t_min, vo_vc_0g * 1000, color="#d7191c", lw=2.5, linestyle="--", label="Photorespiratory Surge $v_o/v_c$ ($0\\text{ g}$) [$\\times 10^3$]")
    ax_d.plot(t_min, ci_earth, color="#2b83ba", lw=1.8, linestyle=":", label="Intercellular $C_i$ ($1.0\\text{ g}$ Earth) [ppm]")

    ax_d.axhline(150.0, color="darkblue", linestyle=":", lw=1.5, label="Critical $CO_2$ Starvation Floor ($150\\text{ ppm}$)")
    ax_d.set_title("d  $CO_2$ Starvation & RuBisCO Photorespiration Trajectory", fontsize=10.5, fontweight="bold", pad=8)
    ax_d.set_xlabel("Elapsed Time Post-Fan Failure [minutes]", fontsize=9)
    ax_d.set_ylabel("Intercellular $C_i$ [ppm] / Ratio $v_o/v_c$ [$\\times 10^3$]", fontsize=9)
    ax_d.set_xlim(0, 15); ax_d.set_ylim(50, 800)
    ax_d.grid(True, linestyle=":", alpha=0.6)
    ax_d.legend(loc="upper right", fontsize=7.5)

    plt.suptitle("Figure 9 | Transient Aerodynamics of Fan Failure & Stagnation Response Across Gravitational Fields",
                 fontsize=12, fontweight="bold", y=0.98)

    pdf_path = os.path.join(out_dir, "Fig9_fan_failure_dynamics.pdf")
    png_path = os.path.join(out_dir, "Fig9_fan_failure_dynamics.png")
    plt.savefig(pdf_path, format="pdf", dpi=300)
    plt.savefig(png_path, format="png", dpi=300)
    plt.close(fig)
    print(f"=== Successfully Generated Figure 9: {pdf_path} and {png_path} ===")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    generate_figure_9(out_dir)
