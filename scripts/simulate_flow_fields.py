#!/usr/bin/env python3
"""
3D and 4D Flow Field Synthesizer for Spaceflight Plant Growth Hardware.
Generates 3D spatial velocity grids, streamline seeds, Q-criterion vortex cores,
boundary layer distributions, and 4D time-resolved particle trajectories across
Microgreen, VEGGIE, and APH chambers under Nominal, High, Low, and Zero airflow regimes.
"""

import numpy as np
import os
import json

class ChamberFlowModel:
    def __init__(self, chamber_type="aph", regime="nominal", gravity=0.0):
        self.chamber_type = chamber_type.lower()
        self.regime = regime.lower()
        self.gravity = float(gravity) # 9.81 for Earth, 0.0 for microgravity

        # Define chamber physical bounding boxes [x_min, x_max, y_min, y_max, z_min, z_max] in meters
        if self.chamber_type == "microgreen":
            self.dims = (0.120, 0.1867, 0.1217) # 120 x 186.7 x 121.7 mm
            self.canopy_z = (0.025, 0.075)
            self.inlet_pos = np.array([0.060, 0.000, 0.0967])
            self.outlet_pos = np.array([0.060, 0.1867, 0.0967])
            self.speeds = {"nominal": 2.60, "high": 5.00, "low": 0.50, "zero": 0.00}
        elif self.chamber_type == "veggie":
            self.dims = (0.292, 0.368, 0.350) # 292 x 368 x 350 mm
            self.canopy_z = (0.040, 0.250)
            self.fan_pos = np.array([0.146, 0.184, 0.350])
            self.speeds = {"nominal": 0.15, "high": 0.28, "low": 0.065, "zero": 0.00}
        elif self.chamber_type == "aph":
            self.dims = (0.454, 0.408, 0.450) # 454 x 408 x 450 mm shoot zone
            self.canopy_z = (0.051, 0.300)
            self.left_inlet_pos = np.array([0.000, 0.204, 0.058])
            self.right_inlet_pos = np.array([0.454, 0.204, 0.058])
            self.speeds = {"nominal": 0.60, "high": 1.50, "low": 0.30, "zero": 0.00}
        elif self.chamber_type in ("chromex", "chromex_pgc"):
            self.dims = (0.095, 0.048, 0.190) # 95 x 48 x 190 mm PGC canister
            self.canopy_z = (0.040, 0.150)
            self.inlet_pos = np.array([0.0475, 0.024, 0.000])
            self.speeds = {"nominal": 0.0098, "high": 0.025, "low": 0.002, "zero": 0.000}
        else:
            raise ValueError(f"Unknown chamber type: {chamber_type}")

        self.u_ref = self.speeds.get(self.regime, 0.60)

    def get_grid(self, nx=40, ny=40, nz=40):
        x = np.linspace(0, self.dims[0], nx)
        y = np.linspace(0, self.dims[1], ny)
        z = np.linspace(0, self.dims[2], nz)
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        return X, Y, Z

    def compute_flow_field(self, nx=40, ny=40, nz=40, t=0.0):
        """Compute 3D velocity field (U, V, W), speed, and vorticity at time t."""
        X, Y, Z = self.get_grid(nx, ny, nz)
        Lx, Ly, Lz = self.dims

        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        W = np.zeros_like(Z)

        # -------------------------------------------------------------
        # ZERO AIRFLOW REGIME (Fan Failure / Stagnation)
        # -------------------------------------------------------------
        if self.regime == "zero":
            if self.gravity > 1.0: # Earth 1g: Weak natural thermal buoyancy plume from LED / canopy
                # Buoyancy driven central plume: warm ceiling / warm leaves -> slow upward drift in center, down along cold walls
                r_xy = np.sqrt((X - Lx/2)**2 + (Y - Ly/2)**2)
                r_max = np.sqrt((Lx/2)**2 + (Ly/2)**2)
                w_buoyant = 0.035 * (1.0 - (r_xy / r_max)**2) * np.sin(np.pi * Z / Lz)
                # Radial return flow
                u_return = -0.015 * (X - Lx/2) / (Lx/2) * np.cos(np.pi * Z / Lz)
                v_return = -0.015 * (Y - Ly/2) / (Ly/2) * np.cos(np.pi * Z / Lz)
                U = u_return
                V = v_return
                W = w_buoyant
            else: # Microgravity 0g: Complete stagnation, pure molecular diffusion, zero mechanical drift
                U = 0.0001 * np.sin(2*np.pi*X/Lx)
                V = 0.0001 * np.sin(2*np.pi*Y/Ly)
                W = np.zeros_like(Z)
            
            Speed = np.sqrt(U**2 + V**2 + W**2)
            TKE = np.full_like(Speed, 1e-6)
            Age = np.full_like(Speed, 120.0 + 50.0 * (1.0 - Z/Lz))
            return {"X": X, "Y": Y, "Z": Z, "U": U, "V": V, "W": W, "Speed": Speed, "TKE": TKE, "Age": Age}

        # -------------------------------------------------------------
        # MICROGREEN CHAMBER (Confined through-flow jet + unsteady flapping)
        # -------------------------------------------------------------
        if self.chamber_type == "microgreen":
            # Inlet jet enters at y=0, x=Lx/2, z=0.0967 discharging in +y direction
            # Jet centerline oscillates with time (flapping instability)
            flap_freq = 2.4 # Hz
            flap_amp = 0.015 * (Y / Ly) * np.sin(2 * np.pi * flap_freq * t)
            x_jet = Lx/2 + flap_amp
            z_jet = 0.0967 - 0.010 * (Y / Ly) # slight downward curve

            # Jet Gaussian core radius expanding with y
            b_jet = 0.020 + 0.040 * (Y / Ly)
            r_jet = np.sqrt((X - x_jet)**2 + (Z - z_jet)**2)
            
            # Forward jet velocity
            u_jet_peak = self.u_ref * (0.04 / (0.04 + Y))
            V_jet = u_jet_peak * np.exp(-(r_jet**2) / (2 * b_jet**2))

            # Recirculation / entrainment vortices in lower tray corners
            # Reverse flow along the tray floor (z < 0.04)
            v_recirc = -0.18 * self.u_ref * (1.0 - Y/Ly) * np.exp(-((Z - 0.035)/0.025)**2) * (1.0 - 4*(X - Lx/2)**2 / Lx**2)
            
            # Secondary lateral swirl
            U_swirl = 0.12 * self.u_ref * np.sin(2 * np.pi * X / Lx) * (Y / Ly) * np.sin(np.pi * Z / Lz)
            W_down = -0.15 * self.u_ref * (Y / Ly) * np.exp(-r_jet / b_jet) * (1.0 - Z/Lz)

            U = U_swirl
            V = V_jet + v_recirc
            W = W_down

            # Add wall boundary damping (no-slip)
            wall_damp = np.tanh(40 * X) * np.tanh(40 * (Lx - X)) * np.tanh(40 * Z) * np.tanh(40 * (Lz - Z))
            U *= wall_damp; V *= wall_damp; W *= wall_damp

            Speed = np.sqrt(U**2 + V**2 + W**2)
            TKE = 0.08 * (Speed**2) + 0.002 * (self.u_ref**2) * np.exp(-r_jet / b_jet)
            Age = 0.5 + 4.5 * (1.0 - V / (self.u_ref + 1e-4)) + 12.0 * np.exp(-Z / 0.03)

        # -------------------------------------------------------------
        # NASA VEGGIE (VPS) (Top suction fan + 4 passive base slots)
        # -------------------------------------------------------------
        elif self.chamber_type == "veggie":
            # Suction sink at top center: (Lx/2, Ly/2, Lz)
            x_c, y_c, z_c = Lx/2, Ly/2, Lz
            dx = x_c - X
            dy = y_c - Y
            dz = z_c - Z
            dist_fan = np.sqrt(dx**2 + dy**2 + dz**2) + 0.02
            
            # Potential flow suction toward top fan
            q_suction = self.u_ref * 0.008 # sink strength
            u_sink = -q_suction * (dx / (dist_fan**3))
            v_sink = -q_suction * (dy / (dist_fan**3))
            w_sink = q_suction * (dz / (dist_fan**3))

            # Base slot inflow: air drawn inward from all 4 perimeter base edges (z < 0.06)
            base_mask = np.exp(-Z / 0.04)
            u_base = 0.4 * self.u_ref * np.sign(Lx/2 - X) * np.exp(-((X - Lx/2)**2)/(2*0.08**2)) * base_mask
            v_base = 0.4 * self.u_ref * np.sign(Ly/2 - Y) * np.exp(-((Y - Ly/2)**2)/(2*0.08**2)) * base_mask

            # Vertical upward draft through pillow gaps
            # In microgravity, upward draft is purely suction; in 1g, LED buoyancy assists center
            buoyancy_boost = 0.08 if self.gravity > 1.0 else 0.0
            w_up = (self.u_ref * 0.85 + buoyancy_boost) * (1.0 - np.exp(-Z / 0.08)) * (1.0 - 0.5 * ((X - Lx/2)/(Lx/2))**2 - 0.5 * ((Y - Ly/2)/(Ly/2))**2)

            U = u_sink + u_base
            V = v_sink + v_base
            W = np.maximum(w_sink, w_up)

            # Pillow obstruction zone: 6 pillows in 2x3 grid dampen flow at z < 0.04
            pillow_damp = 1.0 - 0.65 * np.exp(-Z / 0.04) * (np.sin(2 * np.pi * X / (Lx/2))**2) * (np.sin(3 * np.pi * Y / (Ly/3))**2)
            U *= pillow_damp; V *= pillow_damp; W *= pillow_damp

            Speed = np.sqrt(U**2 + V**2 + W**2)
            TKE = 0.05 * (Speed**2) + 0.0015 * (self.u_ref**2)
            Age = 1.2 + 8.0 * (1.0 - Z/Lz) + 15.0 * (1.0 - Speed / (self.u_ref + 1e-4))

        # -------------------------------------------------------------
        # NASA ADVANCED PLANT HABITAT (APH) (Dual opposing cross-flow + sweep)
        # -------------------------------------------------------------
        elif self.chamber_type == "aph":
            # Left supply jet at x=0 (flows in +x)
            # Right supply jet at x=Lx (flows in -x)
            # Jets are at z=0.058, y spanning full depth
            z_jet = 0.058
            b_jet = 0.035
            jet_profile_z = np.exp(-((Z - z_jet)**2) / (2 * b_jet**2))

            # Left jet decelerates towards center
            u_left = self.u_ref * np.exp(-2.5 * X / Lx) * jet_profile_z
            # Right jet decelerates towards center
            u_right = -self.u_ref * np.exp(-2.5 * (Lx - X) / Lx) * jet_profile_z

            # Central collision updraft at X ~ Lx/2
            collision_mask = np.exp(-((X - Lx/2)**2) / (2 * 0.06**2)) * np.exp(-Z / 0.18)
            w_collision = 1.25 * self.u_ref * collision_mask

            # Upward displacement sweep through shoot canopy to ceiling exhaust
            w_sweep = 0.55 * self.u_ref * (1.0 - np.exp(-Z / 0.08)) * (1.0 + 0.2 * np.sin(np.pi * Y / Ly))

            # Exhaust suction strips at ceiling perimeter
            w_exhaust = 0.40 * self.u_ref * (Z / Lz)**2

            U = u_left + u_right
            V = 0.08 * self.u_ref * np.sin(2 * np.pi * Y / Ly) * (1.0 - Z/Lz)
            W = w_collision + w_sweep + w_exhaust

            # Wall damping
            wall_damp = np.tanh(30 * X) * np.tanh(30 * (Lx - X)) * np.tanh(30 * Y) * np.tanh(30 * (Ly - Y))
            U *= wall_damp; V *= wall_damp; W *= wall_damp

            Speed = np.sqrt(U**2 + V**2 + W**2)
            TKE = 0.09 * (Speed**2) + 0.003 * (self.u_ref**2) * collision_mask
            Age = 3.5 + 14.0 * (1.0 - Z/Lz)

        # -------------------------------------------------------------
        # NASA SPACE SHUTTLE CHROMEX / PGC (Creeping laminar / Darcy foam)
        # -------------------------------------------------------------
        elif self.chamber_type in ("chromex", "chromex_pgc"):
            # Lower manifold needle port at (Lx/2, Ly/2, 0)
            x_c, y_c = Lx / 2.0, Ly / 2.0
            r_needle = np.sqrt((X - x_c)**2 + (Y - y_c)**2) + 1e-4
            
            # Foam block Darcy resistance: z in [0, 0.040]
            in_foam = Z <= 0.040
            foam_attenuation = np.where(in_foam, 0.25, 1.0)
            
            # Needle jet spreading
            w_needle = self.u_ref * np.exp(-((r_needle)**2) / (2 * (0.008 + 0.05 * Z)**2)) * foam_attenuation
            
            # Creeping upward percolation toward top lid perimeter slots
            w_percolation = 0.45 * self.u_ref * (1.0 - np.exp(-Z / 0.03)) * (1.0 - 4*(X - Lx/2)**2 / Lx**2)
            
            # Slow lateral diffusion dispersion
            u_disp = 0.15 * self.u_ref * np.sign(X - x_c) * np.exp(-r_needle / 0.02)
            v_disp = 0.15 * self.u_ref * np.sign(Y - y_c) * np.exp(-r_needle / 0.02)
            
            U = u_disp
            V = v_disp
            W = w_needle + w_percolation

            # Wall damping
            wall_damp = np.tanh(40 * X) * np.tanh(40 * (Lx - X)) * np.tanh(40 * Y) * np.tanh(40 * (Ly - Y))
            U *= wall_damp; V *= wall_damp; W *= wall_damp

            Speed = np.sqrt(U**2 + V**2 + W**2)
            TKE = 0.01 * (Speed**2) + 1e-6 # Ultra-low turbulence, creeping laminar
            
            # Péclet number: Pe = u * d / D
            D_O2 = 2.0e-5
            d_leaf = 0.015
            Peclet = (Speed * d_leaf) / D_O2
            
            # Local O2 Mass Fraction / Hypoxia mapping
            # In sealed/zero mode: O2 decays rapidly in foam and boundary layers
            if self.regime == "zero":
                O2_conc = 0.02 + 0.04 * (Z / Lz) * np.exp(-r_needle / 0.03) # severe hypoxia < 5%
            else:
                O2_conc = 0.18 + 0.0295 * (1.0 - np.exp(-Z / 0.05)) # replenished by AES
                
            Age = 15.0 + 120.0 * (1.0 - Z/Lz)

        return {
            "X": X, "Y": Y, "Z": Z,
            "U": U, "V": V, "W": W,
            "Speed": Speed, "TKE": TKE, "Age": Age
        }

    def generate_streamline_seeds(self, num_seeds=60):
        """Generate 3D starting points for particle tracking and streamline ribbons."""
        Lx, Ly, Lz = self.dims
        if self.chamber_type == "microgreen":
            # Seeds near inlet port
            xs = np.random.uniform(Lx/2 - 0.015, Lx/2 + 0.015, num_seeds)
            ys = np.full(num_seeds, 0.005)
            zs = np.random.uniform(0.085, 0.105, num_seeds)
        elif self.chamber_type == "veggie":
            # Seeds at 4 perimeter base slots
            xs = np.random.uniform(0.02, Lx - 0.02, num_seeds)
            ys = np.random.choice([0.01, Ly - 0.01], num_seeds)
            zs = np.random.uniform(0.005, 0.025, num_seeds)
        elif self.chamber_type == "aph":
            # Seeds along left and right lower diffusers
            n_half = num_seeds // 2
            xs_left = np.full(n_half, 0.01)
            xs_right = np.full(num_seeds - n_half, Lx - 0.01)
            xs = np.concatenate([xs_left, xs_right])
            ys = np.random.uniform(0.02, Ly - 0.02, num_seeds)
            zs = np.random.uniform(0.052, 0.065, num_seeds)
        elif self.chamber_type in ("chromex", "chromex_pgc"):
            # Seeds near base needle manifold
            xs = np.random.uniform(Lx/2 - 0.008, Lx/2 + 0.008, num_seeds)
            ys = np.random.uniform(Ly/2 - 0.008, Ly/2 + 0.008, num_seeds)
            zs = np.random.uniform(0.002, 0.010, num_seeds)
            xs_left = np.full(n_half, 0.008)
            xs_right = np.full(num_seeds - n_half, Lx - 0.008)
            xs = np.concatenate([xs_left, xs_right])
            ys = np.random.uniform(0.02, Ly - 0.02, num_seeds)
            zs = np.random.uniform(0.052, 0.065, num_seeds)

        return np.column_stack([xs, ys, zs])

    def trace_streamlines(self, num_seeds=60, max_steps=180, dt=0.004):
        """Integrate 3D streamlines through the synthesized velocity field."""
        flow = self.compute_flow_field(nx=35, ny=35, nz=35)
        X, Y, Z = flow["X"], flow["Y"], flow["Z"]
        U, V, W = flow["U"], flow["V"], flow["W"]
        Speed = flow["Speed"]
        Lx, Ly, Lz = self.dims

        seeds = self.generate_streamline_seeds(num_seeds)
        lines = []

        from scipy.interpolate import RegularGridInterpolator
        x_pts = X[:, 0, 0]
        y_pts = Y[0, :, 0]
        z_pts = Z[0, 0, :]

        interp_u = RegularGridInterpolator((x_pts, y_pts, z_pts), U, bounds_error=False, fill_value=0.0)
        interp_v = RegularGridInterpolator((x_pts, y_pts, z_pts), V, bounds_error=False, fill_value=0.0)
        interp_w = RegularGridInterpolator((x_pts, y_pts, z_pts), W, bounds_error=False, fill_value=0.0)
        interp_s = RegularGridInterpolator((x_pts, y_pts, z_pts), Speed, bounds_error=False, fill_value=0.0)

        for seed in seeds:
            pos = seed.copy()
            traj = [pos.copy()]
            speeds = [float(interp_s(pos.reshape(1, 3))[0])]

            for _ in range(max_steps):
                if pos[0] < 0.002 or pos[0] > Lx - 0.002 or pos[1] < 0.002 or pos[1] > Ly - 0.002 or pos[2] < 0.002 or pos[2] > Lz - 0.002:
                    break
                
                pos_in = pos.reshape(1, 3)
                vel1 = np.array([float(interp_u(pos_in)[0]), float(interp_v(pos_in)[0]), float(interp_w(pos_in)[0])])
                speed1 = np.linalg.norm(vel1)
                if speed1 < 1e-4:
                    break
                
                # Adaptive dt
                step_dt = min(dt, 0.005 / (speed1 + 1e-3))
                mid_pos = pos + 0.5 * step_dt * vel1
                mid_in = mid_pos.reshape(1, 3)
                vel2 = np.array([float(interp_u(mid_in)[0]), float(interp_v(mid_in)[0]), float(interp_w(mid_in)[0])])
                pos += step_dt * vel2
                
                traj.append(pos.copy())
                speeds.append(float(interp_s(pos.reshape(1, 3))[0]))

            if len(traj) > 4:
                lines.append({"coords": np.array(traj), "speed": np.array(speeds)})

        return lines

def main():
    print("=== Testing 3D Flow Field Synthesizer ===")
    for ch in ["microgreen", "veggie", "aph"]:
        for reg in ["nominal", "high", "low", "zero"]:
            m = ChamberFlowModel(chamber_type=ch, regime=reg, gravity=0.0)
            res = m.compute_flow_field(nx=20, ny=20, nz=20)
            lines = m.trace_streamlines(num_seeds=15)
            print(f"Chamber: {ch:10s} | Regime: {reg:8s} | Max Speed: {res['Speed'].max():.3f} m/s | Streamlines Traced: {len(lines)}")
    print("=== All Chamber Flow Models Verified ===")

if __name__ == "__main__":
    main()
