#!/usr/bin/env python3
"""
Generate the VEGGIE chamber internal geometry as STL surfaces.

The chamber is fully analytic -- there is no CAD input.
Writes into <case>/constant/triSurface/:
    veggie_chamber.stl   closed shell of the fluid domain, multi-solid.
    veggie_pillows.stl   closed boxes for the 6 plant pillows.

Coordinate system (metres, origin at the internal floor, front-left corner):
    x  0 -> 0.292   chamber width
    y  0 -> 0.368   chamber depth
    z  0 -> up      height (floor to light cap)

Usage:
    python3 make_veggie_geometry.py --case <case-dir> [--bellows-h 350] [--verify]
"""

import argparse
import math
import os
from collections import defaultdict

# ---------------------------------------------------------------------------
# VEGGIE Chamber parameters. Metres.
# ---------------------------------------------------------------------------
WIDTH = 0.292           # internal, x
DEPTH = 0.368           # internal, y
INLET_H = 0.010         # base inlet slot height
BELLOWS_H_DEF = 0.350   # default bellows height

PORT_R = 0.025          # fan exhaust radius (50 mm diameter)
PORT_X = WIDTH / 2.0
PORT_Y = DEPTH / 2.0

# 6 pillows in 2x3 grid
PILLOW_X = 0.110
PILLOW_Y = 0.150
PILLOW_Z = 0.040
PILLOW_GAP = 0.016
NX = 2
NY = 3

EMBED = 0.001           # embed pillows 1mm into the floor

BOUNDARY_DS = 0.005     # vertex spacing
TWO_PI = 2.0 * math.pi

# ---------------------------------------------------------------------------
# STL primitives
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

def samples(a, b, ds):
    n = max(1, int(math.ceil(abs(b - a) / ds)))
    return [a + (b - a) * i / n for i in range(n + 1)]

def make_ring(z):
    n = max(64, int(TWO_PI * PORT_R / BOUNDARY_DS))
    return [(PORT_X + PORT_R * math.cos(TWO_PI * i / n),
             PORT_Y + PORT_R * math.sin(TWO_PI * i / n), z) for i in range(n)]

def _unwrap_z(p, cx, cy, a0):
    return (math.atan2(p[1] - cy, p[0] - cx) - a0) % TWO_PI

def write_pierced_ceiling(f, z, poly, ring):
    cx, cy = PORT_X, PORT_Y
    a0 = math.atan2(poly[0][1] - cy, poly[0][0] - cx)
    uo = [_unwrap_z(p, cx, cy, a0) for p in poly]
    uo[0] = 0.0

    ur = [_unwrap_z(p, cx, cy, a0) for p in ring]
    k = min(range(len(ring)), key=lambda i: ur[i])
    ring = ring[k:] + ring[:k]
    ur = ur[k:] + ur[:k]

    N, M = len(poly), len(ring)
    written = 0
    i = j = 0
    while i < N or j < M:
        nxt_o = uo[i + 1] if i + 1 < N else TWO_PI
        nxt_r = ur[j + 1] if j + 1 < M else TWO_PI
        if j >= M or (i < N and nxt_o <= nxt_r):
            written += facet(f, poly[i], poly[(i + 1) % N], ring[j % M])
            i += 1
        else:
            written += facet(f, poly[i % N], ring[(j + 1) % M], ring[j % M])
            j += 1
    return written

def write_chamber(path, bellows_h):
    xs = samples(0.0, WIDTH, BOUNDARY_DS)
    ys = samples(0.0, DEPTH, BOUNDARY_DS)
    ring = make_ring(bellows_h)

    poly = []
    poly.extend([(x, 0.0, bellows_h) for x in xs[:-1]])
    poly.extend([(WIDTH, y, bellows_h) for y in ys[:-1]])
    poly.extend([(x, DEPTH, bellows_h) for x in reversed(xs[1:])])
    poly.extend([(0.0, y, bellows_h) for y in reversed(ys[1:])])

    nf = 0
    with open(path, "w") as f:
        # Baseplate: FULL floor at z=0 (normals point -Z)
        f.write("solid baseplate\n")
        # To get normal -Z, we need b-a and c-a to cross to -Z.
        # quad(f, (x0, y1, 0), (x0, y0, 0), (x1, y0, 0), (x1, y1, 0))
        # a=(x0, y1), b=(x0, y0) -> (0, -dy), c=(x1, y0) -> (dx, -dy)
        # cross((0, -dy), (dx, -dy)) = 0*-dy - (-dy)*dx = dx*dy = +Z! WRONG!
        # Let's try: a=(x0, y0, 0), b=(x0, y1, 0), c=(x1, y1, 0), d=(x1, y0, 0)
        # b-a=(0, dy, 0), c-a=(dx, dy, 0). cross=(0*dy - dy*dx) = -Z! CORRECT!
        for i in range(len(xs) - 1):
            for j in range(len(ys) - 1):
                nf += quad(f, (xs[i], ys[j], 0), (xs[i], ys[j+1], 0),
                           (xs[i+1], ys[j+1], 0), (xs[i+1], ys[j], 0))
        f.write("endsolid baseplate\n")

        # The side walls (inlets + bellows) follow the exact same CCW boundary loop
        # as the lightcap pierced ceiling outer loop.
        # Loop edges: p0 -> p1.
        # If we trace CCW on the floor:
        # a=(p0.x, p0.y), b=(p1.x, p1.y). 
        # quad(f, a_lower, b_lower, b_upper, a_upper)
        # b-a is along the loop. c-a is along the loop + up Z.
        # cross(b-a, c-a) = (dx, dy, 0) x (dx, dy, dz) = (dy*dz, -dx*dz, 0)
        # For front edge: dx>0, dy=0 -> (0, -dx*dz, 0) -> -Y. CORRECT!
        
        # We must split the loop into the 4 named faces for the inlets.
        front_loop = [(x, 0.0) for x in xs]
        right_loop = [(WIDTH, y) for y in ys]
        back_loop = [(x, DEPTH) for x in reversed(xs)]
        left_loop = [(0.0, y) for y in reversed(ys)]
        
        loops = [
            ("front", front_loop),
            ("right", right_loop),
            ("back", back_loop),
            ("left", left_loop)
        ]
        
        for name, loop_pts in loops:
            f.write(f"solid base_inlet_{name}\n")
            for k in range(len(loop_pts) - 1):
                p0, p1 = loop_pts[k], loop_pts[k+1]
                nf += quad(f, (p0[0], p0[1], 0), (p1[0], p1[1], 0), 
                           (p1[0], p1[1], INLET_H), (p0[0], p0[1], INLET_H))
            f.write(f"endsolid base_inlet_{name}\n")

        # Bellows: z=INLET_H to bellows_h
        f.write("solid bellows\n")
        # We can just iterate the full CCW poly loop
        # Wait, poly loop has the last point = first point? 
        # poly: front (xs[:-1]), right (ys[:-1]), back (xs[1:] reversed), left (ys[1:] reversed)
        # so it's a closed loop without duplication.
        for k in range(len(poly)):
            p0 = poly[k]
            p1 = poly[(k+1) % len(poly)]
            nf += quad(f, (p0[0], p0[1], INLET_H), (p1[0], p1[1], INLET_H),
                       (p1[0], p1[1], bellows_h), (p0[0], p0[1], bellows_h))
        f.write("endsolid bellows\n")

        # Lightcap: horizontal ceiling z=bellows_h (normal +Z)
        f.write("solid lightcap\n")
        nf += write_pierced_ceiling(f, bellows_h, poly, ring)
        f.write("endsolid lightcap\n")

        # Fan exhaust: circular disc (normal +Z)
        f.write("solid fan_exhaust\n")
        c = (PORT_X, PORT_Y, bellows_h)
        for i in range(len(ring)):
            nf += facet(f, c, ring[i], ring[(i+1)%len(ring)])
        f.write("endsolid fan_exhaust\n")

    return nf

def write_pillows(path):
    total_w = NX * PILLOW_X + (NX - 1) * PILLOW_GAP
    total_d = NY * PILLOW_Y + (NY - 1) * PILLOW_GAP
    x0 = (WIDTH - total_w) / 2.0
    y0 = (DEPTH - total_d) / 2.0

    nf = 0
    with open(path, "w") as f:
        idx = 0
        for iy in range(NY):
            for ix in range(NX):
                name = "pillow_" + chr(ord('A') + idx)
                idx += 1

                px0 = x0 + ix * (PILLOW_X + PILLOW_GAP)
                px1 = px0 + PILLOW_X
                py0 = y0 + iy * (PILLOW_Y + PILLOW_GAP)
                py1 = py0 + PILLOW_Y

                # Clip and embed
                px0 = max(-EMBED, px0)
                px1 = min(WIDTH + EMBED, px1)
                py0 = max(-EMBED, py0)
                py1 = min(DEPTH + EMBED, py1)

                z0 = -EMBED
                z1 = PILLOW_Z

                f.write(f"solid {name}\n")
                nf += quad(f, (px0, py0, z1), (px1, py0, z1), (px1, py1, z1), (px0, py1, z1)) # Top
                nf += quad(f, (px0, py1, z0), (px1, py1, z0), (px1, py0, z0), (px0, py0, z0)) # Bottom
                nf += quad(f, (px0, py0, z0), (px1, py0, z0), (px1, py0, z1), (px0, py0, z1)) # Front
                nf += quad(f, (px1, py1, z0), (px0, py1, z0), (px0, py1, z1), (px1, py1, z1)) # Back
                nf += quad(f, (px0, py1, z0), (px0, py0, z0), (px0, py0, z1), (px0, py1, z1)) # Left
                nf += quad(f, (px1, py0, z0), (px1, py1, z0), (px1, py1, z1), (px1, py0, z1)) # Right
                f.write(f"endsolid {name}\n")
    return nf

def verify_closed(path):
    half = defaultdict(int)
    verts, nf, vol = [], 0, 0.0
    with open(path) as f:
        for line in f:
            s = line.split()
            if s and s[0] == "vertex":
                verts.append(tuple(round(float(v), 9) for v in s[1:4]))
                if len(verts) == 3:
                    nf += 1
                    a, b, c = verts
                    vol += (a[0] * (b[1] * c[2] - b[2] * c[1])
                            - a[1] * (b[0] * c[2] - b[2] * c[0])
                            + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
                    for i in range(3):
                        half[(verts[i], verts[(i + 1) % 3])] += 1
                    verts = []

    unmatched = [e for e in half if half.get((e[1], e[0]), 0) != half[e]]
    dup = [e for e, n in half.items() if n != 1]
    closed = not unmatched and not dup

    msgs = []
    msgs.append("CLOSED+ORIENTED" if closed else f"BAD ({len(unmatched)} unmatched, {len(dup)} dup)")
    msgs.append(f"vol {vol * 1e3:+8.4f} L")
    if vol <= 0:
        msgs.append("<- NEGATIVE: normals point INTO the solid")

    print(f"  {os.path.basename(path):<18} {nf:6d} facets  {'  '.join(msgs)}")
    return closed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--bellows-h", type=float, default=BELLOWS_H_DEF*1000, help="in mm")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    h = args.bellows_h / 1000.0

    out = os.path.join(args.case, "constant", "triSurface")
    os.makedirs(out, exist_ok=True)

    chamber = os.path.join(out, "veggie_chamber.stl")
    pillows = os.path.join(out, "veggie_pillows.stl")
    info = os.path.join(out, "geometry.info")

    write_chamber(chamber, h)
    write_pillows(pillows)

    v_total = WIDTH * DEPTH * h
    v_pillows = 6.0 * PILLOW_X * PILLOW_Y * PILLOW_Z
    v_air = v_total - v_pillows
    a_fan = math.pi * PORT_R * PORT_R
    a_inlets = 2.0 * (WIDTH + DEPTH) * INLET_H

    with open(info, "w") as f:
        f.write("CHAMBER VEGGIE\n")
        f.write(f"WIDTH {WIDTH:.6f}\n")
        f.write(f"DEPTH {DEPTH:.6f}\n")
        f.write(f"HEIGHT {h:.6f}\n")
        f.write(f"V_AIR {v_air:.6e}\n")
        f.write(f"PORT_AREA {a_fan:.6e}\n")
        f.write(f"INLET_AREA {a_inlets:.6e}\n")

    print(f"Wrote VEGGIE STLs to {out}")
    print(f"  Bellows height : {h*1000:.1f} mm")
    print(f"  Chamber volume : {v_total * 1000:.2f} L (Air volume: {v_air * 1000:.2f} L)")

    if args.verify:
        ok = verify_closed(chamber) & verify_closed(pillows)
        if not ok:
            raise SystemExit("Surface failed verification!")

if __name__ == "__main__":
    main()
