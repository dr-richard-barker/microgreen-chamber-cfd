#!/usr/bin/env python3
"""
Figure 1: 3D Hardware Domain Architecture, Mesh Layout, and Flow Paths.
Compares Microgreen Chamber, VEGGIE (VPS), and Advanced Plant Habitat (APH).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def create_fig1(output_dir):
    fig = plt.figure(figsize=(14, 9), dpi=300)
    gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1.0], hspace=0.3, wspace=0.25)

    # Colors
    c_micro = "#1f77b4"
    c_veggie = "#2ca02c"
    c_aph = "#d62728"
    c_flow = "#0055d4"
    c_heat = "#ff7f0e"

    # Row 1: Hardware Schematics / 2D Cross-sections
    # Panel A: Microgreen Chamber
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_title("a  Microgreen Chamber (Through-flow Jet)", fontsize=11, fontweight="bold", loc="left")
    ax_a.plot([0, 186.7, 186.7, 0, 0], [0, 0, 96.7, 96.7, 0], 'k-', lw=1.5)
    # Parabolic hood
    xs = np.linspace(0, 186.7, 100)
    # Tray at bottom
    ax_a.add_patch(patches.Rectangle((0, 0), 186.7, 25, color="#8c564b", alpha=0.3, label="Root Tray (25mm)"))
    # Port In/Out
    ax_a.add_patch(patches.Rectangle((0, 46.7), 5, 40, color=c_flow, alpha=0.8, label="Inlet Ø40mm"))
    ax_a.add_patch(patches.Rectangle((181.7, 46.7), 5, 40, color="#d62728", alpha=0.8, label="Outlet Ø40mm"))
    # Jet stream arrow
    ax_a.annotate("", xy=(160, 66.7), xytext=(15, 66.7), arrowprops=dict(arrowstyle="->", lw=2.5, color=c_flow))
    # Recirculation vortices
    ax_a.text(93, 78, "Confined Jet Flapping", ha="center", fontsize=9, color=c_flow, style="italic")
    ax_a.text(93, 12, "Microgreen Canopy", ha="center", fontsize=9, color="#2ca02c", fontweight="bold")
    ax_a.set_xlim(-15, 205); ax_a.set_ylim(-10, 140)
    ax_a.set_xlabel("Depth $y$ [mm]", fontsize=9); ax_a.set_ylabel("Height $z$ [mm]", fontsize=9)
    ax_a.grid(True, linestyle=":", alpha=0.5)

    # Panel B: VEGGIE (VPS)
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_title("b  NASA VEGGIE (Bottom-up Suction)", fontsize=11, fontweight="bold", loc="left")
    ax_b.plot([0, 368, 368, 0, 0], [0, 0, 350, 350, 0], 'k-', lw=1.5)
    # 6 Plant pillows
    for px in [20, 140, 260]:
        ax_b.add_patch(patches.Rectangle((px, 0), 90, 40, color="#8c564b", alpha=0.4))
    ax_b.text(184, 20, "6x Plant Pillows (40mm)", ha="center", fontsize=8, color="#5c362b")
    # Base Inlets
    ax_b.add_patch(patches.Rectangle((0, 0), 15, 10, color=c_flow, alpha=0.8))
    ax_b.add_patch(patches.Rectangle((353, 0), 15, 10, color=c_flow, alpha=0.8))
    # Top Fan
    ax_b.add_patch(patches.Rectangle((159, 345), 50, 10, color="#d62728", alpha=0.8, label="Exhaust Ø50mm"))
    # Arrows upward
    ax_b.annotate("", xy=(80, 280), xytext=(25, 30), arrowprops=dict(arrowstyle="->", lw=1.8, color=c_flow))
    ax_b.annotate("", xy=(184, 330), xytext=(184, 60), arrowprops=dict(arrowstyle="->", lw=2.2, color=c_flow))
    ax_b.annotate("", xy=(288, 280), xytext=(343, 30), arrowprops=dict(arrowstyle="->", lw=1.8, color=c_flow))
    ax_b.text(184, 180, "Canopy Wash\n(Cabin-Coupled)", ha="center", fontsize=9, color=c_flow, style="italic")
    ax_b.set_xlim(-20, 390); ax_b.set_ylim(-15, 380)
    ax_b.set_xlabel("Depth $y$ [mm]", fontsize=9); ax_b.set_ylabel("Height $z$ [mm]", fontsize=9)
    ax_b.grid(True, linestyle=":", alpha=0.5)

    # Panel C: APH
    ax_c = fig.add_subplot(gs[0, 2])
    ax_c.set_title("c  NASA APH (Opposing Cross-Flow)", fontsize=11, fontweight="bold", loc="left")
    ax_c.plot([0, 454, 454, 0, 0], [0, 0, 501, 501, 0], 'k-', lw=1.5)
    # Science carrier
    ax_c.add_patch(patches.Rectangle((0, 0), 454, 51, color="#8c564b", alpha=0.4, label="Science Carrier (51mm)"))
    ax_c.text(227, 25, "4-Quadrant Science Carrier (51mm)", ha="center", fontsize=8, color="#5c362b")
    # Inlets (left & right at z=51..66mm)
    ax_c.add_patch(patches.Rectangle((0, 51), 10, 15, color=c_flow, alpha=0.9))
    ax_c.add_patch(patches.Rectangle((444, 51), 10, 15, color=c_flow, alpha=0.9))
    # Diffuser baffles
    ax_c.plot([15, 15], [51, 66], 'k--', lw=1.5)
    ax_c.plot([439, 439], [51, 66], 'k--', lw=1.5)
    # Top exhaust strips
    ax_c.add_patch(patches.Rectangle((0, 491), 30, 10, color="#d62728", alpha=0.8))
    ax_c.add_patch(patches.Rectangle((424, 491), 30, 10, color="#d62728", alpha=0.8))
    # Opposing flow arrows
    ax_c.annotate("", xy=(180, 60), xytext=(20, 60), arrowprops=dict(arrowstyle="->", lw=2.0, color=c_flow))
    ax_c.annotate("", xy=(274, 60), xytext=(434, 60), arrowprops=dict(arrowstyle="->", lw=2.0, color=c_flow))
    ax_c.annotate("", xy=(227, 450), xytext=(227, 90), arrowprops=dict(arrowstyle="->", lw=2.5, color=c_flow))
    ax_c.text(227, 260, "Symmetric Cross-Flow\n$\to$ Upward Sweep", ha="center", fontsize=9, color=c_flow, style="italic")
    ax_c.set_xlim(-25, 480); ax_c.set_ylim(-20, 530)
    ax_c.set_xlabel("Width $x$ [mm]", fontsize=9); ax_c.set_ylabel("Height $z$ [mm]", fontsize=9)
    ax_c.grid(True, linestyle=":", alpha=0.5)

    # Row 2: Comparative Bar Charts (Area, Volume, Flow Rate)
    # Panel D: Growth Area & Volume
    ax_d = fig.add_subplot(gs[1, 0])
    ax_d.set_title("d  Growth Footprint & Canopy Volume", fontsize=11, fontweight="bold", loc="left")
    chambers = ["Microgreen", "VEGGIE", "APH"]
    areas = [0.0224, 0.1075, 0.1708]
    vols = [2.33, 37.61, 83.36]
    x_idx = np.arange(len(chambers))
    w = 0.35
    ax_d.bar(x_idx - w/2, areas, width=w, color=[c_micro, c_veggie, c_aph], alpha=0.85, label="Growth Area [m²]")
    ax_d.set_ylabel("Growth Area [m²]", fontsize=9, color="black")
    ax_d.set_xticks(x_idx)
    ax_d.set_xticklabels(chambers, fontsize=9)
    ax_d.grid(True, linestyle=":", alpha=0.5, axis="y")

    ax_d2 = ax_d.twinx()
    ax_d2.bar(x_idx + w/2, vols, width=w, color=[c_micro, c_veggie, c_aph], alpha=0.4, hatch="//", label="Air Volume [L]")
    ax_d2.set_ylabel("Canopy Air Volume [L]", fontsize=9, color="black")

    # Panel E: Flow Rate & Bulk Velocity
    ax_e = fig.add_subplot(gs[1, 1])
    ax_e.set_title("e  Ventilation Rate & Bulk Velocity", fontsize=11, fontweight="bold", loc="left")
    q_vals = [11.8, 85.0, 26.4]
    u_vals = [0.262, 0.150, 0.600]
    ax_e.bar(x_idx - w/2, q_vals, width=w, color=[c_micro, c_veggie, c_aph], alpha=0.85)
    ax_e.set_ylabel("Flow Rate $Q$ [m³/h]", fontsize=9)
    ax_e.set_xticks(x_idx)
    ax_e.set_xticklabels(chambers, fontsize=9)
    ax_e.grid(True, linestyle=":", alpha=0.5, axis="y")

    ax_e2 = ax_e.twinx()
    ax_e2.plot(x_idx, u_vals, color="black", marker="D", lw=2, markersize=7)
    ax_e2.set_ylabel("Canopy Velocity $U$ [m/s]", fontsize=9)

    # Panel F: Air Exchange Rate & Residence Time
    ax_f = fig.add_subplot(gs[1, 2])
    ax_f.set_title("f  Air Exchange Rate (ACH) & $\tau_0$", fontsize=11, fontweight="bold", loc="left")
    ach_vals = [5051, 2260, 317]
    tau_vals = [0.71, 1.60, 11.35]
    ax_f.bar(x_idx - w/2, ach_vals, width=w, color=[c_micro, c_veggie, c_aph], alpha=0.85)
    ax_f.set_ylabel("Air Exchange Rate [h⁻¹]", fontsize=9)
    ax_f.set_yscale("log")
    ax_f.set_xticks(x_idx)
    ax_f.set_xticklabels(chambers, fontsize=9)
    ax_f.grid(True, linestyle=":", alpha=0.5, axis="y")

    ax_f2 = ax_f.twinx()
    ax_f2.plot(x_idx, tau_vals, color="purple", marker="s", lw=2, markersize=7)
    ax_f2.set_ylabel("Residence Time $\tau_0$ [s]", fontsize=9, color="purple")

    plt.tight_layout()
    png_out = os.path.join(output_dir, "Fig1_hardware_domains.png")
    pdf_out = os.path.join(output_dir, "Fig1_hardware_domains.pdf")
    plt.savefig(png_out, dpi=300)
    plt.savefig(pdf_out)
    plt.close()
    print(f"Generated Figure 1: {png_out}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    create_fig1(out)
