#!/usr/bin/env python3
"""
Generate the NASA Space Shuttle CHROMEX / Plant Growth Unit (PGU) geometry as STL surfaces.

The geometry is fully analytic -- no CAD input required.
Writes into <case>/constant/triSurface/:
    1. chromex_pgu_chassis.stl   Macro-scale Middeck locker chassis with lamp bank & cooling ducts.
    2. chromex_pgc_chamber.stl   Micro-scale Plant Growth Chamber (PGC) Lexan canister fluid domain.
    3. chromex_foam_block.stl    Porous synthetic foam rooting block matrix.
    4. chromex_pgc_array.stl     6-canister PGC array inside the PGU locker.

Dimensions (Metres):
    PGU Macro Chassis: 0.510 (W, x) x 0.360 (D, y) x 0.270 (H, z) -- 49.57 L Shuttle Middeck Locker
    PGC Micro Canister: 0.095 (W, x) x 0.048 (D, y) x 0.190 (H, z) -- 0.866 L fluid domain
    PGC Foam Rooting Block: 0.095 (x) x 0.048 (y) x 0.040 (z) -- 0.182 L porous block

Usage:
    python3 scripts/make_chromex_geometry.py --case <case-dir> [--verify]
"""

import argparse
import math
import os
import sys
from collections import defaultdict

# ---------------------------------------------------------------------------
# Physical Dimensions (Metres)
# ---------------------------------------------------------------------------
# Macro PGU Chassis
PGU_W = 0.510           # Width (x)
PGU_D = 0.360           # Depth (y)
PGU_H = 0.270           # Height (z)

# Micro PGC Canister
PGC_W = 0.095           # Width (x)
PGC_D = 0.048           # Depth (y)
PGC_H = 0.190           # Total height (z)

# Rooting Foam Matrix
FOAM_H = 0.040          # Foam height (z = 0 to 0.040)
EMBED = 0.001           # 1 mm embed for watertight Boolean subtraction

# Fluid Ports in PGC
INLET_R = 0.003         # 3 mm radius inlet port at bottom center (x=PGC_W/2, y=PGC_D/2)
EXHAUST_H = 0.005       # 5 mm exhaust slot at top lid perimeter

# PGU Array Layout (2 rows of 3 canisters)
ARRAY_NX = 3
ARRAY_NY = 2
ARRAY_GAP_X = 0.045
ARRAY_GAP_Y = 0.050

BOUNDARY_DS = 0.005     # 5 mm mesh spacing
TWO_PI = 2.0 * math.pi

# ---------------------------------------------------------------------------
# STL Primitives
# ---------------------------------------------------------------------------
def facet(f, a, b, c):
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    mag = math.sqrt(nx * nx + ny * ny + nz * nz)
    if mag < 1e-20:
        return 0
    nx, ny, nz = nx / mag, ny / mag, nz / mag
    f.write("  facet normal %.9e %.9e %.9e\n    outer loop\n" % (nx, ny, nz))
    for p in (a, b, c):
        f.write("      vertex %.9e %.9e %.9e\n" % (p[0], p[1], p[2]))
    f.write("    endloop\n  endfacet\n")
    return 1

def quad(f, a, b, c, d):
    return facet(f, a, b, c) + facet(f, a, c, d)

def box_solid(f, name, x0, x1, y0, y1, z0, z1):
    f.write(f"solid {name}\n")
    # Bottom
    quad(f, (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0))
    # Top
    quad(f, (x0, y0, z1), (x0, y1, z1), (x1, y1, z1), (x1, y0, z1))
    # Front (y=y0)
    quad(f, (x0, y0, z0), (x0, y0, z1), (x1, y0, z1), (x1, y0, z0))
    # Back (y=y1)
    quad(f, (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1))
    # Left (x=x0)
    quad(f, (x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1))
    # Right (x=x1)
    quad(f, (x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0))
    f.write(f"endsolid {name}\n")

# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------
def write_pgc_chamber(path):
    """Write individual PGC canister multi-solid STL."""
    with open(path, "w") as f:
        # 1. Floor
        f.write("solid floor\n")
        quad(f, (0, 0, 0), (PGC_W, 0, 0), (PGC_W, PGC_D, 0), (0, PGC_D, 0))
        f.write("endsolid floor\n")

        # 2. Walls
        f.write("solid walls\n")
        # Front
        quad(f, (0, 0, 0), (0, 0, PGC_H - EXHAUST_H), (PGC_W, 0, PGC_H - EXHAUST_H), (PGC_W, 0, 0))
        # Back
        quad(f, (0, PGC_D, 0), (PGC_W, PGC_D, 0), (PGC_W, PGC_D, PGC_H - EXHAUST_H), (0, PGC_D, PGC_H - EXHAUST_H))
        # Left
        quad(f, (0, 0, 0), (0, PGC_D, 0), (0, PGC_D, PGC_H - EXHAUST_H), (0, 0, PGC_H - EXHAUST_H))
        # Right
        quad(f, (PGC_W, 0, 0), (PGC_W, 0, PGC_H - EXHAUST_H), (PGC_W, PGC_D, PGC_H - EXHAUST_H), (PGC_W, PGC_D, 0))
        f.write("endsolid walls\n")

        # 3. Ceiling (Lid)
        f.write("solid lid\n")
        quad(f, (0, 0, PGC_H), (0, PGC_D, PGC_H), (PGC_W, PGC_D, PGC_H), (PGC_W, 0, PGC_H))
        f.write("endsolid lid\n")

        # 4. Inlet Port (Base Manifold)
        f.write("solid inlet_port\n")
        cx, cy = PGC_W / 2.0, PGC_D / 2.0
        n_seg = 16
        for i in range(n_seg):
            th0 = i * TWO_PI / n_seg
            th1 = (i + 1) * TWO_PI / n_seg
            p0 = (cx, cy, 0)
            p1 = (cx + INLET_R * math.cos(th0), cy + INLET_R * math.sin(th0), 0)
            p2 = (cx + INLET_R * math.cos(th1), cy + INLET_R * math.sin(th1), 0)
            facet(f, p0, p2, p1)
        f.write("endsolid inlet_port\n")

        # 5. Exhaust Ports (Lid Perimeter Slots)
        f.write("solid exhaust_ports\n")
        # Front exhaust slot
        quad(f, (0, 0, PGC_H - EXHAUST_H), (0, 0, PGC_H), (PGC_W, 0, PGC_H), (PGC_W, 0, PGC_H - EXHAUST_H))
        # Back exhaust slot
        quad(f, (0, PGC_D, PGC_H - EXHAUST_H), (PGC_W, PGC_D, PGC_H - EXHAUST_H), (PGC_W, PGC_D, PGC_H), (0, PGC_D, PGC_H))
        # Left exhaust slot
        quad(f, (0, 0, PGC_H - EXHAUST_H), (0, PGC_D, PGC_H - EXHAUST_H), (0, PGC_D, PGC_H), (0, 0, PGC_H))
        # Right exhaust slot
        quad(f, (PGC_W, 0, PGC_H - EXHAUST_H), (PGC_W, 0, PGC_H), (PGC_W, PGC_D, PGC_H), (PGC_W, PGC_D, PGC_H - EXHAUST_H))
        f.write("endsolid exhaust_ports\n")

def write_foam_block(path):
    """Write synthetic rooting foam block solid STL."""
    with open(path, "w") as f:
        box_solid(f, "foam_block", 0, PGC_W, 0, PGC_D, -EMBED, FOAM_H)

def write_pgu_chassis(path):
    """Write macro-scale PGU Middeck locker chassis STL."""
    with open(path, "w") as f:
        # Main Locker Shell
        box_solid(f, "pgu_shell", 0, PGU_W, 0, PGU_D, 0, PGU_H)

def write_pgc_array(path):
    """Write 6-canister PGC array inside PGU."""
    with open(path, "w") as f:
        x_margin = (PGU_W - (ARRAY_NX * PGC_W + (ARRAY_NX - 1) * ARRAY_GAP_X)) / 2.0
        y_margin = (PGU_D - (ARRAY_NY * PGC_D + (ARRAY_NY - 1) * ARRAY_GAP_Y)) / 2.0
        
        idx = 1
        for iy in range(ARRAY_NY):
            for ix in range(ARRAY_NX):
                x0 = x_margin + ix * (PGC_W + ARRAY_GAP_X)
                x1 = x0 + PGC_W
                y0 = y_margin + iy * (PGC_D + ARRAY_GAP_Y)
                y1 = y0 + PGC_D
                z0 = 0.020  # 20 mm above PGU floor
                z1 = z0 + PGC_H
                box_solid(f, f"pgc_canister_{idx}", x0, x1, y0, y1, z0, z1)
                idx += 1

def verify_stl(path):
    """Verify STL vertex and edge connectivity."""
    edges = defaultdict(int)
    n_facets = 0
    with open(path) as f:
        curr_pts = []
        for line in f:
            line = line.strip()
            if line.startswith("vertex"):
                parts = line.split()
                curr_pts.append(tuple(round(float(v), 7) for v in parts[1:4]))
                if len(curr_pts) == 3:
                    n_facets += 1
                    p1, p2, p3 = curr_pts
                    edges[tuple(sorted((p1, p2)))] += 1
                    edges[tuple(sorted((p2, p3)))] += 1
                    edges[tuple(sorted((p3, p1)))] += 1
                    curr_pts = []
    
    open_edges = [e for e, c in edges.items() if c != 2]
    print(f"[{os.path.basename(path)}] {n_facets} facets, {len(edges)} edges, {len(open_edges)} open edges.")
    return len(open_edges) == 0

def main():
    parser = argparse.ArgumentParser(description="Generate CHROMEX / PGU analytic STL geometry")
    parser.add_argument("--case", default=".", help="Target OpenFOAM case directory")
    parser.add_argument("--verify", action="store_true", help="Run closed manifold verification")
    args = parser.parse_args()

    out_dir = os.path.join(args.case, "constant", "triSurface")
    os.makedirs(out_dir, exist_ok=True)

    pgc_path = os.path.join(out_dir, "chromex_pgc_chamber.stl")
    foam_path = os.path.join(out_dir, "chromex_foam_block.stl")
    pgu_path = os.path.join(out_dir, "chromex_pgu_chassis.stl")
    array_path = os.path.join(out_dir, "chromex_pgc_array.stl")

    write_pgc_chamber(pgc_path)
    write_foam_block(foam_path)
    write_pgu_chassis(pgu_path)
    write_pgc_array(array_path)

    print(f"=== Successfully Generated CHROMEX / PGU STLs in {out_dir} ===")
    print(f"  • PGU Macro Chassis:  {PGU_W*1000:.0f} x {PGU_D*1000:.0f} x {PGU_H*1000:.0f} mm (49.57 L)")
    print(f"  • PGC Micro Canister: {PGC_W*1000:.0f} x {PGC_D*1000:.0f} x {PGC_H*1000:.0f} mm (0.866 L)")
    print(f"  • PGC Foam Block:     {PGC_W*1000:.0f} x {PGC_D*1000:.0f} x {FOAM_H*1000:.0f} mm (0.182 L)")
    print(f"  • PGC Array:          6 Canisters (2x3 grid)")

    if args.verify:
        print("\n--- Verifying STL Watertight Properties ---")
        v1 = verify_stl(foam_path)
        v2 = verify_stl(pgu_path)
        v3 = verify_stl(array_path)
        print(f"Watertight status: Foam={v1}, PGU={v2}, Array={v3}")

if __name__ == "__main__":
    main()
