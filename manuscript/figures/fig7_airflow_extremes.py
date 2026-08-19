#!/usr/bin/env python3
"""
Figure 7: Operational Airflow Extremes and Stagnation Regimes across Spaceflight Hardware.
Visualizes a 3x4 comparative matrix mapping Zero Flow (Fan Failure), Low Draft (Seedling),
Flight Nominal, and High Blast across Microgreen, VEGGIE, and APH chambers.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Add scripts directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts")))
from simulate_flow_fields import ChamberFlowModel

def create_fig7(output_dir):
    fig, axes = plt.subplots(3, 4, figsize=(16, 11), dpi=300)

    chambers = ["microgreen", "veggie", "aph"]
    ch_names = ["Microgreen Chamber", "NASA VEGGIE (VPS)", "NASA APH (Phytotron)"]
    regimes = ["zero", "low", "nominal", "high"]
    reg_names = ["1. Zero Airflow (Stagnant 0g)", "2. Low Draft (Flight Min)", "3. Flight Nominal (Baseline)", "4. High Blast (Maximum Blower)"]

    for row, ch in enumerate(chambers):
        for col, reg in enumerate(regimes):
            ax = axes[row, col]
            model = ChamberFlowModel(chamber_type=ch, regime=reg, gravity=0.0)
            flow = model.compute_flow_field(nx=30, ny=30, nz=30)
            
            # Mid-plane coronal slice
            mid_y = 15
            x_slice = flow["X"][:, mid_y, :] * 1000.0
            z_slice = flow["Z"][:, mid_y, :] * 1000.0
            spd = flow["Speed"][:, mid_y, :]
            
            # Maximum color scale normalized per chamber
            vmax = model.speeds["high"] * 0.9 if reg != "zero" else 0.05
            
            im = ax.contourf(x_slice, z_slice, spd, levels=25, cmap="turbo", vmin=0, vmax=max(vmax, 0.05))
            
            # Quiver arrows
            skip = 3
            u_sl = flow["U"][:, mid_y, :]
            w_sl = flow["W"][:, mid_y, :]
            if reg != "zero":
                ax.quiver(x_slice[::skip, ::skip], z_slice[::skip, ::skip],
                          u_sl[::skip, ::skip], w_sl[::skip, ::skip],
                          color="white", scale=15, alpha=0.7, width=0.006)
            
            # Title only on top row
            if row == 0:
                ax.set_title(f"{reg_names[col]}", fontsize=9.5, fontweight="bold", pad=8)
            
            # Y-axis label only on first column
            if col == 0:
                ax.set_ylabel(f"{ch_names[row]}\nHeight $z$ [mm]", fontsize=9, fontweight="bold")
            else:
                ax.set_yticklabels([])
                
            # X-axis label only on bottom row
            if row == 2:
                ax.set_xlabel("Width $x$ [mm]", fontsize=8.5)
            else:
                ax.set_xticklabels([])
                
            # Add boundary layer metric badge in corner
            if reg == "zero":
                gbl_txt = "$g_{bl} \\approx 0.03$\n$\\delta_{bl} > 25\\text{mm}$\n(Suffocation)"
                badge_col = "darkred"
            elif reg == "low":
                gbl = "0.31" if ch=="microgreen" else ("0.22" if ch=="veggie" else "0.78")
                dbl = "5.8" if ch=="microgreen" else ("7.9" if ch=="veggie" else "2.2")
                gbl_txt = f"$g_{{bl}}={gbl}$\n$\\delta_{{bl}}={dbl}\\text{{mm}}$"
                badge_col = "orange" if ch=="veggie" else "darkgreen"
            elif reg == "nominal":
                gbl = "0.69" if ch=="microgreen" else ("0.52" if ch=="veggie" else "1.07")
                dbl = "2.5" if ch=="microgreen" else ("3.4" if ch=="veggie" else "1.6")
                gbl_txt = f"$g_{{bl}}={gbl}$\n$\\delta_{{bl}}={dbl}\\text{{mm}}$"
                badge_col = "darkgreen"
            else:
                gbl = "1.19" if ch=="microgreen" else ("0.79" if ch=="veggie" else "1.75")
                dbl = "1.4" if ch=="microgreen" else ("2.1" if ch=="veggie" else "0.98")
                gbl_txt = f"$g_{{bl}}={gbl}$\n$\\delta_{{bl}}={dbl}\\text{{mm}}$"
                badge_col = "blue"
                
            ax.text(0.95, 0.93, gbl_txt, transform=ax.transAxes, fontsize=6.8,
                    ha="right", va="top", bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor=badge_col, lw=1.2))

    plt.suptitle("Figure 7 | Operational Airflow Extremes Matrix: Zero Stagnation vs. Low Draft vs. Nominal vs. High Blast in Microgravity",
                 fontsize=11.5, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    png_out = os.path.join(output_dir, "Fig7_airflow_extremes.png")
    pdf_out = os.path.join(output_dir, "Fig7_airflow_extremes.pdf")
    plt.savefig(png_out, dpi=300)
    plt.savefig(pdf_out)
    plt.close()
    print(f"Generated Figure 7: {png_out}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    create_fig7(out)
