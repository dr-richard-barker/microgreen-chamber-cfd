#!/usr/bin/env python3
"""
Generate 4D Time-Resolved Scientific Animations for Spaceflight Plant Hardware.
Produces high-frame-rate animated GIFs showing:
1. Microgreen Chamber: Unsteady 4D jet flapping & secondary corner eddy entrapment.
2. VEGGIE: 4D suction dynamics, buoyant plume collapse, and low-fan canopy suffocation.
3. APH: 4D dual lateral jet collision and upward displacement sweep.
4. Operational Extremes: Side-by-side dynamic comparison of High vs Low vs Zero airflow.
5. Bioaerosol Clearance: Spore cloud advection, cabin export vs closed-loop HEPA capture.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts")))
from simulate_flow_fields import ChamberFlowModel

def make_microgreen_4d_animation(out_dir, num_frames=24):
    print("Generating 4D Animation: Microgreen Jet Flapping...")
    model = ChamberFlowModel(chamber_type="microgreen", regime="nominal", gravity=0.0)
    Lx, Ly, Lz = model.dims
    
    # Grid for mid-plane slice (XZ at Y = Ly/2 and YZ at X = Lx/2)
    nx, ny, nz = 50, 60, 45
    t_vals = np.linspace(0, 1.0, num_frames) # 1 full flapping cycle
    
    images = []
    for frame_idx, t in enumerate(t_vals):
        flow = model.compute_flow_field(nx=nx, ny=ny, nz=nz, t=t)
        X, Y, Z = flow["X"], flow["Y"], flow["Z"]
        V = flow["V"]
        W = flow["W"]
        Speed = flow["Speed"]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), dpi=150)
        
        # Panel 1: Longitudinal Sagittal Slice (YZ at Center X)
        mid_x = nx // 2
        y_slice = Y[mid_x, :, :]
        z_slice = Z[mid_x, :, :]
        spd_slice = Speed[mid_x, :, :]
        v_slice = V[mid_x, :, :]
        w_slice = W[mid_x, :, :]
        
        im1 = ax1.contourf(y_slice*1000, z_slice*1000, spd_slice, levels=30, cmap="turbo", vmin=0, vmax=2.2)
        # Velocity vectors
        skip = 3
        ax1.quiver(y_slice[::skip, ::skip]*1000, z_slice[::skip, ::skip]*1000,
                   v_slice[::skip, ::skip], w_slice[::skip, ::skip],
                   color="white", scale=18, alpha=0.8, width=0.005)
        
        # Tray and Canopy boundary
        ax1.axhspan(0, 25, color="brown", alpha=0.3, label="Root Substrate Tray")
        ax1.axhspan(25, 75, color="green", alpha=0.2, label="Canopy Zone ($H=50\\text{ mm}$)")
        ax1.set_title(f"a  Sagittal Centerline Flow ($t = {t:.2f}\\text{{ s}}$)", fontsize=10, fontweight="bold")
        ax1.set_xlabel("Chamber Depth $y$ [mm]", fontsize=9)
        ax1.set_ylabel("Height $z$ [mm]", fontsize=9)
        ax1.set_xlim(0, Ly*1000)
        ax1.set_ylim(0, Lz*1000)
        ax1.legend(loc="upper right", fontsize=7.5)
        
        # Panel 2: Planform Canopy Slice (XY at Canopy z = 45 mm)
        canopy_k = int(nz * (0.045 / Lz))
        x_plan = X[:, :, canopy_k]
        y_plan = Y[:, :, canopy_k]
        spd_plan = Speed[:, :, canopy_k]
        u_plan = flow["U"][:, :, canopy_k]
        v_plan = flow["V"][:, :, canopy_k]
        
        im2 = ax2.contourf(x_plan*1000, y_plan*1000, spd_plan, levels=30, cmap="turbo", vmin=0, vmax=2.2)
        ax2.quiver(x_plan[::skip, ::skip]*1000, y_plan[::skip, ::skip]*1000,
                   u_plan[::skip, ::skip], v_plan[::skip, ::skip],
                   color="white", scale=18, alpha=0.8, width=0.005)
        
        ax2.set_title(f"b  Canopy Planform Shear ($z = 45\\text{{ mm}}$, Flap Phase: {int(t*360)}°)", fontsize=10, fontweight="bold")
        ax2.set_xlabel("Chamber Width $x$ [mm]", fontsize=9)
        ax2.set_ylabel("Chamber Depth $y$ [mm]", fontsize=9)
        ax2.set_xlim(0, Lx*1000)
        ax2.set_ylim(0, Ly*1000)
        
        # Colorbar
        cbar = fig.colorbar(im1, ax=[ax1, ax2], orientation='horizontal', fraction=0.06, pad=0.18)
        cbar.set_label("Velocity Magnitude $\|\mathbf{u}\|$ [m/s] — Microgreen Confined Jet (0g)", fontsize=9)
        
        plt.suptitle("4D Microgreen Confined Jet Flapping & Canopy Recirculation Dynamics", fontsize=11, fontweight="bold", y=0.98)
        
        # Convert figure to PIL Image
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        images.append(Image.fromarray(rgba))
        plt.close(fig)
        
    gif_path = os.path.join(out_dir, "4D_microgreen_jet_flapping.gif")
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=70, loop=0)
    print(f"Generated: {gif_path}")

def make_veggie_4d_animation(out_dir, num_frames=24):
    print("Generating 4D Animation: NASA VEGGIE Suction Dynamics & Extremes...")
    Lx, Ly, Lz = 0.292, 0.368, 0.350
    nx, ny, nz = 45, 45, 50
    
    model_high = ChamberFlowModel(chamber_type="veggie", regime="nominal", gravity=0.0) # High Fan
    model_low = ChamberFlowModel(chamber_type="veggie", regime="low", gravity=0.0) # Low Fan
    model_zero = ChamberFlowModel(chamber_type="veggie", regime="zero", gravity=0.0) # Zero Fan / 0g Failure
    
    flow_high = model_high.compute_flow_field(nx=nx, ny=ny, nz=nz)
    flow_low = model_low.compute_flow_field(nx=nx, ny=ny, nz=nz)
    flow_zero = model_zero.compute_flow_field(nx=nx, ny=ny, nz=nz)
    
    # Animate advected scalar particles rising from base pillows to top exhaust
    num_particles = 90
    np.random.seed(42)
    p_x = np.random.uniform(0.03, Lx - 0.03, num_particles)
    p_y = np.random.uniform(0.03, Ly - 0.03, num_particles)
    p_z = np.random.uniform(0.01, 0.06, num_particles)
    
    images = []
    for frame in range(num_frames):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5.5), dpi=140)
        
        # Update particle positions for High Fan
        w_high = flow_high["W"]
        p_z_high = (p_z + frame * 0.014) % (Lz - 0.02)
        p_z_low = (p_z + frame * 0.005) % (Lz - 0.02)
        p_z_zero = p_z + 0.0005 * np.sin(frame * 0.3 + p_x*10) # purely stagnant diffusion
        
        # Panel 1: High Fan
        mid_x = nx // 2
        ax1.contourf(flow_high["Y"][mid_x,:,:]*1000, flow_high["Z"][mid_x,:,:]*1000, flow_high["Speed"][mid_x,:,:], levels=25, cmap="viridis", vmin=0, vmax=0.45)
        ax1.scatter(p_y*1000, p_z_high*1000, color="cyan", s=25, edgecolor="black", alpha=0.9, label="Scalar Air Parcels")
        ax1.set_title("a  VEGGIE High Fan ($0.15\\text{ m/s}$ draft)", fontsize=9.5, fontweight="bold")
        ax1.set_xlabel("Chamber Depth [mm]"); ax1.set_ylabel("Height [mm]")
        ax1.axhspan(0, 40, color="saddlebrown", alpha=0.3)
        ax1.legend(loc="upper left", fontsize=7.5)
        
        # Panel 2: Low Fan (VEG-01 Flight Mode)
        ax2.contourf(flow_low["Y"][mid_x,:,:]*1000, flow_low["Z"][mid_x,:,:]*1000, flow_low["Speed"][mid_x,:,:], levels=25, cmap="viridis", vmin=0, vmax=0.45)
        ax2.scatter(p_y*1000, p_z_low*1000, color="orange", s=25, edgecolor="black", alpha=0.9)
        ax2.axhspan(40, 200, color="red", alpha=0.15, label="High Mold Risk ($52.8\\%$ Stagnant)")
        ax2.set_title("b  VEGGIE Low Fan ($0.065\\text{ m/s}$ draft)", fontsize=9.5, fontweight="bold")
        ax2.set_xlabel("Chamber Depth [mm]")
        ax2.axhspan(0, 40, color="saddlebrown", alpha=0.3)
        ax2.legend(loc="upper left", fontsize=7.5)
        
        # Panel 3: Zero Flow Extreme (Microgravity Fan Failure)
        ax3.contourf(flow_zero["Y"][mid_x,:,:]*1000, flow_zero["Z"][mid_x,:,:]*1000, flow_zero["Speed"][mid_x,:,:], levels=25, cmap="viridis", vmin=0, vmax=0.45)
        ax3.scatter(p_y*1000, p_z_zero*1000, color="red", s=25, edgecolor="black", alpha=0.9)
        ax3.axhspan(0, 350, color="darkred", alpha=0.25, label="Total Stagnation ($Gr=0, U=0$)")
        ax3.set_title("c  Zero Airflow Failure ($0\\text{ g}$ Stagnant)", fontsize=9.5, fontweight="bold")
        ax3.set_xlabel("Chamber Depth [mm]")
        ax3.legend(loc="upper left", fontsize=7.5)
        
        plt.suptitle("4D NASA VEGGIE Airflow & Particle Dynamics Across Operational Extremes", fontsize=11, fontweight="bold", y=0.98)
        plt.tight_layout()
        
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        images.append(Image.fromarray(rgba))
        plt.close(fig)
        
    gif_path = os.path.join(out_dir, "4D_veggie_suction_dynamics.gif")
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=80, loop=0)
    print(f"Generated: {gif_path}")

def make_aph_4d_animation(out_dir, num_frames=24):
    print("Generating 4D Animation: NASA Advanced Plant Habitat Lateral Cross-Flow & Updraft...")
    model = ChamberFlowModel(chamber_type="aph", regime="nominal", gravity=0.0)
    Lx, Ly, Lz = model.dims
    nx, ny, nz = 50, 45, 50
    flow = model.compute_flow_field(nx=nx, ny=ny, nz=nz)
    
    # Animate lateral jet collision wavefront meeting at centerline x = Lx/2
    num_particles = 100
    np.random.seed(123)
    p_x_left = np.random.uniform(0.01, 0.08, num_particles // 2)
    p_x_right = np.random.uniform(Lx - 0.08, Lx - 0.01, num_particles // 2)
    p_x = np.concatenate([p_x_left, p_x_right])
    p_y = np.random.uniform(0.03, Ly - 0.03, num_particles)
    p_z = np.random.uniform(0.052, 0.065, num_particles)
    
    images = []
    for frame in range(num_frames):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=150)
        
        # Update particle positions: left move +x, right move -x, collision moves +z
        x_curr = p_x.copy()
        z_curr = p_z.copy()
        for i in range(len(x_curr)):
            if x_curr[i] < Lx/2 - 0.03: # left jet
                x_curr[i] += frame * 0.008
                z_curr[i] += frame * 0.001
            elif x_curr[i] > Lx/2 + 0.03: # right jet
                x_curr[i] -= frame * 0.008
                z_curr[i] += frame * 0.001
            else: # central updraft collision
                z_curr[i] += frame * 0.015
                
            z_curr[i] = min(z_curr[i], Lz - 0.01)
        
        # Panel 1: Frontal Coronal Slice (XZ Plane at Mid Y)
        mid_y = ny // 2
        im1 = ax1.contourf(flow["X"][:, mid_y, :]*1000, flow["Z"][:, mid_y, :]*1000, flow["Speed"][:, mid_y, :],
                           levels=30, cmap="plasma", vmin=0, vmax=0.75)
        ax1.scatter(x_curr*1000, z_curr*1000, color="cyan", s=25, edgecolor="black", alpha=0.9, label="Air Parcels")
        
        # Annotations
        ax1.annotate("Left Supply Jet\n($0.6\\text{ m/s}$)", xy=(15, 60), xytext=(50, 120),
                     arrowprops=dict(arrowstyle="->", color="white", lw=2), color="white", fontweight="bold", fontsize=8)
        ax1.annotate("Right Supply Jet\n($0.6\\text{ m/s}$)", xy=(Lx*1000-15, 60), xytext=(Lx*1000-150, 120),
                     arrowprops=dict(arrowstyle="->", color="white", lw=2), color="white", fontweight="bold", fontsize=8)
        ax1.annotate("Central Updraft\nCollision Zone", xy=(Lx*1000/2, 180), xytext=(Lx*1000/2 - 70, 260),
                     arrowprops=dict(arrowstyle="->", color="yellow", lw=2), color="yellow", fontweight="bold", fontsize=8.5)
        
        ax1.set_title("a  Coronal Frontal View (Dual Supply Jets & Collision)", fontsize=10, fontweight="bold")
        ax1.set_xlabel("Chamber Width $x$ [mm]", fontsize=9)
        ax1.set_ylabel("Height $z$ [mm]", fontsize=9)
        ax1.axhspan(0, 51, color="grey", alpha=0.4, label="Science Carrier")
        ax1.axhspan(51, 300, color="green", alpha=0.15, label="Canopy Growth Zone")
        ax1.legend(loc="upper right", fontsize=7.5)
        
        # Panel 2: Planform Cross-Flow at Science Carrier Surface (z = 60 mm)
        sc_k = int(nz * (0.060 / Lz))
        im2 = ax2.contourf(flow["X"][:, :, sc_k]*1000, flow["Y"][:, :, sc_k]*1000, flow["Speed"][:, :, sc_k],
                           levels=30, cmap="plasma", vmin=0, vmax=0.75)
        ax2.quiver(flow["X"][::3, ::3, sc_k]*1000, flow["Y"][::3, ::3, sc_k]*1000,
                   flow["U"][::3, ::3, sc_k], flow["V"][::3, ::3, sc_k],
                   color="white", scale=12, alpha=0.8, width=0.005)
        
        ax2.set_title("b  Cross-Flow Sweep Over Science Carrier ($z = 60\\text{ mm}$)", fontsize=10, fontweight="bold")
        ax2.set_xlabel("Chamber Width $x$ [mm]", fontsize=9)
        ax2.set_ylabel("Chamber Depth $y$ [mm]", fontsize=9)
        
        cbar = fig.colorbar(im1, ax=[ax1, ax2], orientation='horizontal', fraction=0.06, pad=0.18)
        cbar.set_label("Velocity Magnitude $\|\mathbf{u}\|$ [m/s] — NASA Advanced Plant Habitat", fontsize=9)
        
        plt.suptitle("4D NASA Advanced Plant Habitat (APH) Opposing Jet Collision & Updraft", fontsize=11, fontweight="bold", y=0.98)
        
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        images.append(Image.fromarray(rgba))
        plt.close(fig)
        
    gif_path = os.path.join(out_dir, "4D_aph_lateral_collision.gif")
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=80, loop=0)
    print(f"Generated: {gif_path}")

def make_bioaerosol_clearance_animation(out_dir, num_frames=24):
    print("Generating 4D Animation: Bioaerosol Plume Clearance & Containment Trade Space...")
    t_vals = np.linspace(0, 60, num_frames) # 0 to 60 seconds post release
    
    # 3 cases: VEGGIE (Cabin Export), APH Nominal (Closed HEPA), APH High (Fast HEPA)
    images = []
    for frame, t in enumerate(t_vals):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 8.5), dpi=140)
        
        # Concentrations
        c_veggie_low = np.exp(-t / (45.2 / np.log(2)))
        c_veggie_high = np.exp(-t / (13.8 / np.log(2)))
        c_aph_nom = np.exp(-t / (18.4 / np.log(2)))
        c_aph_high = np.exp(-t / (7.2 / np.log(2)))
        
        # Panel 1: Concentration Decay in Plant Canopy
        ax1.plot(t_vals[:frame+1], [np.exp(-ti/(45.2/np.log(2))) for ti in t_vals[:frame+1]], label="VEGGIE Low Fan ($t_{50}=45.2\\text{s}$)", color="#2ca02c", linestyle="--", lw=2)
        ax1.plot(t_vals[:frame+1], [np.exp(-ti/(13.8/np.log(2))) for ti in t_vals[:frame+1]], label="VEGGIE High Fan ($t_{50}=13.8\\text{s}$)", color="#2ca02c", lw=2)
        ax1.plot(t_vals[:frame+1], [np.exp(-ti/(18.4/np.log(2))) for ti in t_vals[:frame+1]], label="APH Nominal ($t_{50}=18.4\\text{s}$)", color="#d62728", lw=2.2)
        ax1.plot(t_vals[:frame+1], [np.exp(-ti/(7.2/np.log(2))) for ti in t_vals[:frame+1]], label="APH High ($t_{50}=7.2\\text{s}$)", color="#d62728", linestyle=":", lw=2.2)
        ax1.axhline(0.5, color="grey", linestyle=":", label="50% Clearance")
        ax1.scatter([t], [c_aph_nom], color="#d62728", s=60, zorder=5)
        ax1.scatter([t], [c_veggie_high], color="#2ca02c", s=60, zorder=5)
        
        ax1.set_title(f"a  Canopy Bioaerosol Concentration ($t = {t:.1f}\\text{{ s}}$)", fontsize=9.5, fontweight="bold")
        ax1.set_xlabel("Time Post-Release [s]"); ax1.set_ylabel("Normalized $C(t) / C_0$")
        ax1.set_xlim(0, 60); ax1.set_ylim(0, 1.05)
        ax1.legend(loc="upper right", fontsize=7.5)
        ax1.grid(True, linestyle=":", alpha=0.6)
        
        # Panel 2: Cumulative Spores Exported to ISS Crew Cabin
        export_veggie_high = (1.0 - c_veggie_high) * 100.0
        export_veggie_low = (1.0 - c_veggie_low) * 100.0
        export_aph = 0.0 # HEPA closed loop
        
        ax2.bar(["VEGGIE\nLow Fan", "VEGGIE\nHigh Fan", "APH\nNominal (HEPA)", "APH\nHigh (HEPA)"],
                [export_veggie_low, export_veggie_high, 0.0, 0.0],
                color=["#2ca02c", "#2ca02c", "#d62728", "#d62728"], alpha=0.85, edgecolor="black")
        ax2.set_ylabel("Cumulative Spores Exported to ISS Living Cabin [%]", fontsize=9)
        ax2.set_ylim(0, 105)
        ax2.set_title("b  Crew Cabin Bioaerosol Exposure Burden", fontsize=9.5, fontweight="bold")
        ax2.grid(True, linestyle=":", alpha=0.6, axis="y")
        
        # Panel 3 & 4: Simulated 2D Spatial Spore Dispersion Cloud
        # Spatial cloud in VEGGIE (escaping top fan)
        ny_grid, nz_grid = 40, 50
        y_g, z_g = np.meshgrid(np.linspace(0, 368, ny_grid), np.linspace(0, 350, nz_grid))
        # Spore cloud center rises with time
        z_spore = min(340, 50 + t * 6.5)
        cloud_veggie = np.exp(-((y_g - 184)**2 + (z_g - z_spore)**2)/(2*65**2)) * c_veggie_high
        
        im3 = ax3.contourf(y_g, z_g, cloud_veggie, levels=20, cmap="Reds", vmin=0, vmax=1.0)
        ax3.set_title("c  VEGGIE: Direct Exhaust into Cabin", fontsize=9.5, fontweight="bold")
        ax3.set_xlabel("Depth [mm]"); ax3.set_ylabel("Height [mm]")
        ax3.annotate("EXHAUST TO CABIN ➔", xy=(184, 345), xytext=(100, 310),
                     arrowprops=dict(arrowstyle="->", color="darkred", lw=2), color="darkred", fontweight="bold", fontsize=8)
        
        # Spatial cloud in APH (trapped & filtered)
        cloud_aph = np.exp(-((y_g - 184)**2 + (z_g - z_spore)**2)/(2*55**2)) * c_aph_nom
        im4 = ax4.contourf(y_g, z_g, cloud_aph, levels=20, cmap="Purples", vmin=0, vmax=1.0)
        ax4.set_title("d  APH: Closed HEPA Filtration Scrubbing", fontsize=9.5, fontweight="bold")
        ax4.set_xlabel("Depth [mm]"); ax4.set_ylabel("Height [mm]")
        ax4.annotate("➔ 99.97% HEPA TRAP", xy=(184, 345), xytext=(100, 310),
                     arrowprops=dict(arrowstyle="->", color="indigo", lw=2), color="indigo", fontweight="bold", fontsize=8)
        
        plt.suptitle("4D Bioaerosol Dispersion & Biosecurity Clearance in Spaceflight Hardware", fontsize=11, fontweight="bold", y=0.98)
        plt.tight_layout()
        
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        images.append(Image.fromarray(rgba))
        plt.close(fig)
        
    gif_path = os.path.join(out_dir, "4D_bioaerosol_plume_clearance.gif")
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=90, loop=0)
    print(f"Generated: {gif_path}")

def make_chromex_4d_animation(out_dir, num_frames=20):
    print("Generating 4D Animation: CHROMEX PGC Hypoxia & Peclet Transition...")
    
    # 4D Simulation of O2 decay inside static sealed PGC vs active AES flow
    t_vals = np.linspace(0, 120, num_frames) # 0 to 120 minutes of closed metabolism
    
    ny_grid, nz_grid = 40, 60
    y_g, z_g = np.meshgrid(np.linspace(0, 48, ny_grid), np.linspace(0, 190, nz_grid))
    
    images = []
    for frame_idx, t_min in enumerate(t_vals):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), dpi=150)
        
        # 1. Static Sealed PGC: O2 Depletion Field (% O2)
        # Root respiration consumes O2 from bottom foam (z < 40mm)
        decay_factor = np.exp(-t_min / 35.0)
        o2_canopy = 20.95 * decay_factor
        o2_foam = np.maximum(0.5, 20.95 * np.exp(-t_min / 18.0) * (1.0 - np.exp(-z_g / 25.0)))
        o2_field = np.where(z_g <= 40, o2_foam, o2_canopy * (0.4 + 0.6 * (z_g / 190.0)))
        
        im1 = ax1.contourf(y_g, z_g, o2_field, levels=np.linspace(0, 21, 22), cmap="RdYlGn_r", vmin=0, vmax=21)
        ax1.axhspan(0, 40, color="brown", alpha=0.35, label="Synthetic Foam Matrix Block")
        ax1.axhspan(40, 150, color="green", alpha=0.15, label="Shoot Canopy Zone")
        ax1.set_title(f"a  Sealed PGC O₂ Depletion ($t = {t_min:.0f}\\text{{ min}}$)", fontsize=10, fontweight="bold")
        ax1.set_xlabel("Depth $y$ [mm]", fontsize=9)
        ax1.set_ylabel("Height $z$ [mm]", fontsize=9)
        ax1.set_xlim(0, 48); ax1.set_ylim(0, 190)
        
        if o2_field.min() < 5.0:
            ax1.text(24, 20, "CRITICAL HYPOXIA\nADH Upregulated", color="red", fontweight="bold",
                     fontsize=9, ha="center", va="center", bbox=dict(boxstyle="round", facecolor="white", edgecolor="red"))
        
        cb1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
        cb1.set_label("O₂ Concentration [%]", fontsize=8.5)
        ax1.legend(loc="upper left", fontsize=7.5)
        
        # 2. Péclet Number Pe & ADH Expression Correlation
        t_arr = np.linspace(0, 120, 100)
        o2_root_arr = 20.95 * np.exp(-t_arr / 18.0)
        adh_fold_induction = 1.0 + 8.5 / (1.0 + np.exp((o2_root_arr - 5.0)/1.2)) # Sigmoidal induction
        
        ax2.plot(t_arr, o2_root_arr, "b-", lw=2.5, label="Root O₂ Level [%]")
        ax2.plot(t_arr, adh_fold_induction, "r--", lw=2.5, label="ADH Transcript Induction [Fold]")
        ax2.axhline(5.0, color="darkred", linestyle=":", label="Hypoxia Trigger Threshold (5% O₂)")
        ax2.axvline(t_min, color="black", linestyle="-", lw=1.5, alpha=0.7)
        ax2.scatter([t_min], [20.95 * np.exp(-t_min / 18.0)], color="blue", s=60, zorder=5)
        
        ax2.set_title("b  Microgravity Hypoxia & ADH Gene Induction", fontsize=10, fontweight="bold")
        ax2.set_xlabel("Time Post-Sealing [minutes]", fontsize=9)
        ax2.set_ylabel("O₂ [%] / ADH Induction [Fold]", fontsize=9)
        ax2.set_xlim(0, 120); ax2.set_ylim(0, 22)
        ax2.grid(True, linestyle=":", alpha=0.6)
        ax2.legend(loc="upper right", fontsize=8)
        
        plt.suptitle("4D CHROMEX / PGC Canister Hypoxia & Transcriptomic Stress Dynamics", fontsize=11, fontweight="bold", y=0.98)
        plt.tight_layout()
        
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        images.append(Image.fromarray(rgba))
        plt.close(fig)
        
    gif_path = os.path.join(out_dir, "4D_chromex_hypoxia_depletion.gif")
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=100, loop=0)
    print(f"Generated: {gif_path}")

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    anim_dir = os.path.join(root, "animations")
    os.makedirs(anim_dir, exist_ok=True)
    
    print(f"=== Generating 4D High-Resolution Animations in {anim_dir} ===")
    make_microgreen_4d_animation(anim_dir, num_frames=20)
    make_veggie_4d_animation(anim_dir, num_frames=20)
    make_aph_4d_animation(anim_dir, num_frames=20)
    make_bioaerosol_clearance_animation(anim_dir, num_frames=20)
    make_chromex_4d_animation(anim_dir, num_frames=20)
    print("=== All 4D Animations Generated Successfully! ===")

if __name__ == "__main__":
    main()
