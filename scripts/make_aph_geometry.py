#!/usr/bin/env python3
"""
Generate the APH (Advanced Plant Habitat) chamber internal geometry as STL surfaces.

The chamber is fully analytic -- there is no CAD input.
Writes into <case>/constant/triSurface/:
    aph_chamber.stl          closed shell of the fluid domain, multi-solid.
    aph_science_carrier.stl  closed box for the Science Carrier root module.
    aph_diffuser_left.stl    thin box for left inlet diffuser baffle.
    aph_diffuser_right.stl   thin box for right inlet diffuser baffle.

Coordinate system (metres, origin at the internal floor, front-left corner):
    x  0 -> 0.454   chamber width
    y  0 -> 0.408   chamber depth
    z  0 -> 0.501   height (floor to GLA ceiling)

Usage:
    python3 make_aph_geometry.py --case <case-dir> [--air-vel 0.6] [--verify]
"""

import argparse
import math
import os
from collections import defaultdict

# ---------------------------------------------------------------------------
# APH Chamber parameters -- Morrow et al. 2016 ICES-2016-320. Metres.
# ---------------------------------------------------------------------------
WIDTH = 0.454            # internal width, x (454 mm)
DEPTH = 0.408            # internal depth, y (408 mm)
HEIGHT = 0.501           # total height, z (501 mm)

ROOT_Z = 0.051           # science carrier top (51 mm)
SHOOT_H = 0.450          # shoot zone height (450 mm clear)

INLET_Z_MIN = 0.051      # inlet slot lower edge (just above SC)
INLET_Z_MAX = 0.066      # inlet slot upper edge (15 mm tall)
INLET_H = INLET_Z_MAX - INLET_Z_MIN

EXHAUST_W = 0.020        # ceiling perimeter exhaust strip width (20 mm)

DIFFUSER_THICK = 0.002   # 2 mm baffle thickness
DIFFUSER_OFFSET = 0.005  # 5 mm inward from inlet face

EMBED = 0.001            # 1 mm embedding into solids for watertightness

# ---------------------------------------------------------------------------
# STL primitives. Normals point OUT of the fluid domain for chamber shell,
# and OUT of the solid (into fluid) for obstacles like SC / diffusers.
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
    # CCW order: (a, b, c) and (a, c, d)
    return facet(f, a, b, c) + facet(f, a, c, d)

def write_box(f, x0, x1, y0, y1, z0, z1, name="solid"):
    """Write an axis-aligned box with outward normals."""
    f.write("solid %s\n" % name)
    # top (+z)
    quad(f, (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1))
    # bottom (-z)
    quad(f, (x0, y1, z0), (x1, y1, z0), (x1, y0, z0), (x0, y0, z0))
    # front (-y)
    quad(f, (x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1))
    # back (+y)
    quad(f, (x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1))
    # left (-x)
    quad(f, (x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1))
    # right (+x)
    quad(f, (x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1))
    f.write("endsolid %s\n" % name)

# ---------------------------------------------------------------------------
# APH Chamber Shell - Grid Based to Guarantee Watertight Matching
# ---------------------------------------------------------------------------
def write_aph_chamber(path):
    """Write the closed APH fluid shell as a multi-solid ASCII STL.
    Normals point OUT of the fluid domain."""
    xs = [0.0, EXHAUST_W, WIDTH - EXHAUST_W, WIDTH]
    ys = [0.0, EXHAUST_W, DEPTH - EXHAUST_W, DEPTH]
    zs = [0.0, INLET_Z_MIN, INLET_Z_MAX, HEIGHT]

    # Collect quads per solid name
    solids = defaultdict(list)

    # 1. Floor at z=0 (normal -z)
    for i in range(3):
        for j in range(3):
            solids["floor"].append(((xs[i], ys[j+1], 0), (xs[i+1], ys[j+1], 0), (xs[i+1], ys[j], 0), (xs[i], ys[j], 0)))

    # 2. Ceiling at z=HEIGHT (normal +z)
    for i in range(3):
        for j in range(3):
            q = ((xs[i], ys[j], HEIGHT), (xs[i+1], ys[j], HEIGHT), (xs[i+1], ys[j+1], HEIGHT), (xs[i], ys[j+1], HEIGHT))
            if i == 1 and j == 1:
                solids["ceiling"].append(q)
            elif j == 0:
                solids["exhaust_north"].append(q)
            elif j == 2:
                solids["exhaust_south"].append(q)
            elif i == 0 and j == 1:
                solids["exhaust_west"].append(q)
            elif i == 2 and j == 1:
                solids["exhaust_east"].append(q)

    # 3. Front wall at y=0 (normal -y)
    for i in range(3):
        for k in range(3):
            solids["walls"].append(((xs[i], 0, zs[k]), (xs[i+1], 0, zs[k]), (xs[i+1], 0, zs[k+1]), (xs[i], 0, zs[k+1])))

    # 4. Back wall at y=DEPTH (normal +y)
    for i in range(3):
        for k in range(3):
            solids["walls"].append(((xs[i+1], DEPTH, zs[k]), (xs[i], DEPTH, zs[k]), (xs[i], DEPTH, zs[k+1]), (xs[i+1], DEPTH, zs[k+1])))

    # 5. Left wall at x=0 (normal -x)
    for j in range(3):
        for k in range(3):
            q = ((0, ys[j+1], zs[k]), (0, ys[j], zs[k]), (0, ys[j], zs[k+1]), (0, ys[j+1], zs[k+1]))
            if k == 1:
                solids["left_inlet"].append(q)
            else:
                solids["walls"].append(q)

    # 6. Right wall at x=WIDTH (normal +x)
    for j in range(3):
        for k in range(3):
            q = ((WIDTH, ys[j], zs[k]), (WIDTH, ys[j+1], zs[k]), (WIDTH, ys[j+1], zs[k+1]), (WIDTH, ys[j], zs[k+1]))
            if k == 1:
                solids["right_inlet"].append(q)
            else:
                solids["walls"].append(q)

    # Write all solids
    nf = 0
    with open(path, "w") as f:
        for name, quads in solids.items():
            f.write(f"solid {name}\n")
            for a, b, c, d in quads:
                nf += quad(f, a, b, c, d)
            f.write(f"endsolid {name}\n")
    return nf

def write_aph_science_carrier(path):
    """Write the Science Carrier box (embedded in floor/walls)."""
    with open(path, "w") as f:
        write_box(f, -EMBED, WIDTH + EMBED, -EMBED, DEPTH + EMBED, -EMBED, ROOT_Z, name="carrier_tray")

def write_aph_diffuser(path, x_pos, name="diffuser"):
    """Write thin porous baffle box for the inlet diffuser."""
    with open(path, "w") as f:
        write_box(f, x_pos - DIFFUSER_THICK/2.0, x_pos + DIFFUSER_THICK/2.0,
                  0.0, DEPTH, INLET_Z_MIN, INLET_Z_MAX, name=name)

# ---------------------------------------------------------------------------
# Verification helper (watertight & manifold check)
# ---------------------------------------------------------------------------
def verify_closed(path):
    half = defaultdict(int)
    nf = 0
    vol = 0.0
    with open(path, "r") as f:
        curr_v = []
        for line in f:
            line = line.strip()
            if line.startswith("vertex"):
                parts = line.split()
                curr_v.append((round(float(parts[1]), 9),
                               round(float(parts[2]), 9),
                               round(float(parts[3]), 9)))
            elif line.startswith("endfacet"):
                if len(curr_v) == 3:
                    a, b, c = curr_v
                    vol += (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])) / 6.0
                    for e in [(a, b), (b, c), (c, a)]:
                        half[e] += 1
                    nf += 1
                curr_v = []

    unmatched = [e for e in half if half.get((e[1], e[0]), 0) != half[e]]
    dup = [e for e, n in half.items() if n != 1]
    closed = not unmatched and not dup
    msgs = []
    msgs.append("CLOSED+ORIENTED" if closed else f"BAD ({len(unmatched)} unmatched, {len(dup)} dup)")
    msgs.append(f"vol {vol*1e3:+8.4f} L")
    print(f"  {os.path.basename(path):<24} {nf:6d} facets  {'  '.join(msgs)}")
    return closed and vol > 0

def main():
    ap = argparse.ArgumentParser(description="Generate APH chamber STL geometry.")
    ap.add_argument("--case", required=True, help="OpenFOAM case directory")
    ap.add_argument("--air-vel", type=float, default=0.6, help="Supply velocity m/s (default: 0.6)")
    ap.add_argument("--verify", action="store_true", help="Verify STL closure")
    args = ap.parse_args()

    out = os.path.join(args.case, "constant", "triSurface")
    os.makedirs(out, exist_ok=True)

    c_path = os.path.join(out, "aph_chamber.stl")
    sc_path = os.path.join(out, "aph_science_carrier.stl")
    dl_path = os.path.join(out, "aph_diffuser_left.stl")
    dr_path = os.path.join(out, "aph_diffuser_right.stl")
    info_path = os.path.join(out, "geometry.info")

    write_aph_chamber(c_path)
    write_aph_science_carrier(sc_path)
    write_aph_diffuser(dl_path, DIFFUSER_OFFSET, "diffuser_left")
    write_aph_diffuser(dr_path, WIDTH - DIFFUSER_OFFSET, "diffuser_right")

    # Metrics
    v_total = WIDTH * DEPTH * HEIGHT
    v_root = WIDTH * DEPTH * ROOT_Z
    v_shoot = WIDTH * DEPTH * SHOOT_H
    a_inlet_single = DEPTH * INLET_H
    q_single = args.air_vel * a_inlet_single
    q_total = 2.0 * q_single

    with open(info_path, "w") as f:
        f.write(f"CHAMBER APH\n")
        f.write(f"WIDTH {WIDTH:.6f}\n")
        f.write(f"DEPTH {DEPTH:.6f}\n")
        f.write(f"HEIGHT {HEIGHT:.6f}\n")
        f.write(f"V_AIR {v_shoot:.6e}\n")
        f.write(f"INLET_AREA {a_inlet_single:.6e}\n")
        f.write(f"INLET_VEL {args.air_vel:.4f}\n")
        f.write(f"Q_M3S {q_total:.6e}\n")

    print("APH Geometry Parameters:")
    print(f"  Chamber outer dims:  {WIDTH*1000:.1f} x {DEPTH*1000:.1f} x {HEIGHT*1000:.1f} mm ({v_total*1e3:.1f} L)")
    print(f"  Shoot volume:        {v_shoot*1e3:.1f} L (clear height {SHOOT_H*1000:.1f} mm)")
    print(f"  Root carrier volume: {v_root*1e3:.1f} L (depth {ROOT_Z*1000:.1f} mm)")
    print(f"  Inlet slots (2x):    {DEPTH*1000:.1f} x {INLET_H*1000:.1f} mm at z={INLET_Z_MIN*1000:.1f}..{INLET_Z_MAX*1000:.1f} mm")
    print(f"  Inlet velocity:      {args.air_vel:.3f} m/s -> Q = {q_single*3600:.1f} m3/h each ({q_total*3600:.1f} m3/h total)")

    if args.verify:
        ok = True
        ok &= verify_closed(c_path)
        ok &= verify_closed(sc_path)
        ok &= verify_closed(dl_path)
        ok &= verify_closed(dr_path)
        if not ok:
            print("Warning: some surfaces failed verification.")
        else:
            print("All APH STLs verified: closed and correctly oriented.")

if __name__ == "__main__":
    main()
