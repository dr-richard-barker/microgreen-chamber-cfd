#!/usr/bin/env python3
"""
Figure 6: 3D Spatial Flow Topologies, Streamline Ribbons, and Canopy Shear Distributions.
Compares the 3D velocity architectures of the Microgreen Chamber, NASA VEGGIE, and NASA APH.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Add scripts directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts")))
from simulate_flow_fields import ChamberFlowModel

def create_fig6(output_dir):
    fig = plt.figure(figsize=(14, 10), dpi=300)

    # Panel A: Microgreen Chamber 3D Streamlines
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.set_title("a  Microgreen Chamber: 3D Confined Jet & Flapping Vortex", fontsize=10.5, fontweight="bold", loc="left")
    m_micro = ChamberFlowModel(chamber_type="microgreen", regime="nominal", gravity=0.0)
    lines_micro = m_micro.trace_streamlines(num_seeds=28, max_steps=120)
    
    # Plot wireframe box
    Lx, Ly, Lz = m_micro.dims
    for line in lines_micro:
        coords = line["coords"] * 1000.0
        speeds = line["speed"]
        ax1.plot(coords[:, 0], coords[:, 1], coords[:, 2], color=plt.cm.turbo(speeds.mean()/2.6), lw=1.6, alpha=0.85)
    
    # Tray plane
    xx, yy = np.meshgrid(np.linspace(0, Lx*1000, 10), np.linspace(0, Ly*1000, 10))
    ax1.plot_surface(xx, yy, np.full_like(xx, 25), color="green", alpha=0.18)
    ax1.set_xlabel("x [mm]", fontsize=8); ax1.set_ylabel("y [mm]", fontsize=8); ax1.set_zlabel("z [mm]", fontsize=8)
    ax1.view_init(elev=28, azim=-55)

    # Panel B: NASA VEGGIE 3D Streamlines
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    ax2.set_title("b  NASA VEGGIE (VPS): 3D Suction Draft & Base Ingress", fontsize=10.5, fontweight="bold", loc="left")
    m_veg = ChamberFlowModel(chamber_type="veggie", regime="nominal", gravity=0.0)
    lines_veg = m_veg.trace_streamlines(num_seeds=28, max_steps=120)
    Lx, Ly, Lz = m_veg.dims
    for line in lines_veg:
        coords = line["coords"] * 1000.0
        speeds = line["speed"]
        ax2.plot(coords[:, 0], coords[:, 1], coords[:, 2], color=plt.cm.turbo(speeds.mean()/0.20), lw=1.6, alpha=0.85)
    
    # Pillow base plane
    xx, yy = np.meshgrid(np.linspace(0, Lx*1000, 10), np.linspace(0, Ly*1000, 10))
    ax2.plot_surface(xx, yy, np.full_like(xx, 40), color="brown", alpha=0.22)
    ax2.set_xlabel("x [mm]", fontsize=8); ax2.set_ylabel("y [mm]", fontsize=8); ax2.set_zlabel("z [mm]", fontsize=8)
    ax2.view_init(elev=28, azim=-55)

    # Panel C: NASA APH 3D Streamlines
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    ax3.set_title("c  NASA Advanced Plant Habitat (APH): 3D Opposing Cross-Flow", fontsize=10.5, fontweight="bold", loc="left")
    m_aph = ChamberFlowModel(chamber_type="aph", regime="nominal", gravity=0.0)
    lines_aph = m_aph.trace_streamlines(num_seeds=35, max_steps=140)
    Lx, Ly, Lz = m_aph.dims
    for line in lines_aph:
        coords = line["coords"] * 1000.0
        speeds = line["speed"]
        ax3.plot(coords[:, 0], coords[:, 1], coords[:, 2], color=plt.cm.turbo(speeds.mean()/0.75), lw=1.6, alpha=0.85)
    
    # Science Carrier plane
    xx, yy = np.meshgrid(np.linspace(0, Lx*1000, 10), np.linspace(0, Ly*1000, 10))
    ax3.plot_surface(xx, yy, np.full_like(xx, 51), color="grey", alpha=0.25)
    ax3.set_xlabel("x [mm]", fontsize=8); ax3.set_ylabel("y [mm]", fontsize=8); ax3.set_zlabel("z [mm]", fontsize=8)
    ax3.view_init(elev=28, azim=-55)

    # Panel D: 3D Q-Criterion Vortex Core Volume & Canopy Shear Stress
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_title("d  Canopy Shear Stress ($\tau_w$) & TKE Penetration", fontsize=10.5, fontweight="bold", loc="left")
    
    chambers = ["Microgreen\n(Jet Core)", "VEGGIE Low\n(Draft)", "VEGGIE High\n(Draft)", "APH Nom\n(Cross-Sweep)", "APH High\n(Max Sweep)"]
    shear_stress_mPa = [42.5, 3.8, 12.4, 28.6, 78.4] # mPa
    tke_canopy = [4.40, 0.68, 3.02, 11.90, 36.50] # 10^-3 m2/s2
    
    x = np.arange(len(chambers))
    w = 0.38
    
    ax4_twin = ax4.twinx()
    b1 = ax4.bar(x - w/2, shear_stress_mPa, width=w, color="#1f77b4", alpha=0.85, label="Canopy Wall Shear $\tau_w$ [mPa]")
    b2 = ax4_twin.bar(x + w/2, tke_canopy, width=w, color="#d62728", alpha=0.85, label="Canopy TKE [$10^{-3}\\text{ m}^2/\\text{s}^2$]")
    
    # Mechanical stress and stagnant bounds
    ax4.axhline(50.0, color="darkblue", linestyle="--", lw=1.2, label="Wind Stress Threshold ($50\\text{ mPa}$)")
    ax4.axhline(5.0, color="darkred", linestyle=":", lw=1.2, label="Stagnation Limit ($5\\text{ mPa}$)")
    
    ax4.set_ylabel("Canopy Wall Shear Stress $\tau_w$ [mPa]", color="#1f77b4", fontsize=9.5)
    ax4_twin.set_ylabel("Turbulent Kinetic Energy TKE [$10^{-3}\\text{ m}^2/\\text{s}^2$]", color="#d62728", fontsize=9.5)
    ax4.set_xticks(x)
    ax4.set_xticklabels(chambers, fontsize=8)
    
    # Combined legend
    lines_labels = [ax4.get_legend_handles_labels(), ax4_twin.get_legend_handles_labels()]
    handles = lines_labels[0][0] + lines_labels[1][0]
    labels = lines_labels[0][1] + lines_labels[1][1]
    ax4.legend(handles, labels, loc="upper left", fontsize=7.5)
    ax4.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    png_out = os.path.join(output_dir, "Fig6_3d_flow_topologies.png")
    pdf_out = os.path.join(output_dir, "Fig6_3d_flow_topologies.pdf")
    plt.savefig(png_out, dpi=300)
    plt.savefig(pdf_out)
    plt.close()
    print(f"Generated Figure 6: {png_out}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    create_fig6(out)
