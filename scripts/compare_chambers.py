#!/usr/bin/env python3
"""
Compare CFD simulation results across Microgreen, VEGGIE, and APH chambers.

Supports:
1. Standard single-case cross-chamber comparison:
   python3 scripts/compare_chambers.py runs/case_microgreen runs/case_veggie runs/case_aph [--output comparison_dir]

2. Gravity sweep comparative scaling mode:
   python3 scripts/compare_chambers.py --gravity-sweep runs/p3_g_* [--output comparison_dir]
"""

import argparse
import glob
import json
import math
import os
import re
import sys

def parse_notes_md(case_dir):
    """Extract metadata from NOTES.md if present."""
    notes_file = os.path.join(case_dir, "NOTES.md")
    meta = {}
    if not os.path.isfile(notes_file):
        return meta
    with open(notes_file, "r") as f:
        for line in f:
            m = re.match(r"^\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|", line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip()
                meta[key] = val
    return meta

def get_latest_time(case_dir):
    """Find the latest numerical time directory in an OpenFOAM case."""
    time_dirs = []
    for item in os.listdir(case_dir):
        p = os.path.join(case_dir, item)
        if os.path.isdir(p):
            try:
                t = float(item)
                time_dirs.append((t, item))
            except ValueError:
                pass
    if not time_dirs:
        return None
    time_dirs.sort(key=lambda x: x[0])
    return time_dirs[-1][1]

def parse_openfoam_table(filepath):
    """Parse standard OpenFOAM postProcessing tabular output file."""
    if not os.path.isfile(filepath):
        return None
    data = []
    headers = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                clean = re.sub(r"^#\s*", "", line)
                headers = clean.split()
            elif line:
                parts = [float(x) for x in line.split()]
                data.append(parts)
    return {"headers": headers, "data": data}

def detect_chamber_type(case_dir, meta):
    """Determine whether case is microgreen, veggie, or aph."""
    name = os.path.basename(os.path.normpath(case_dir)).lower()
    if "aph" in name:
        return "APH"
    elif "veggie" in name:
        return "VEGGIE"
    elif "microgreen" in name or "p1" in name or "p2" in name or "p3" in name:
        return "Microgreen"
    
    # Check triSurface
    stl_dir = os.path.join(case_dir, "constant", "triSurface")
    if os.path.isdir(stl_dir):
        files = os.listdir(stl_dir)
        if any("aph" in f for f in files):
            return "APH"
        if any("veggie" in f for f in files):
            return "VEGGIE"
    return "Microgreen"

def extract_case_metrics(case_dir):
    """Extract scalar metrics for a single case."""
    meta = parse_notes_md(case_dir)
    latest_time = get_latest_time(case_dir)
    chamber_type = detect_chamber_type(case_dir, meta)

    # Dimensional properties
    specs = {
        "Microgreen": {"L": 0.0967, "Area": 0.0224, "V_canopy": 0.00112, "U_nom": 0.262},
        "VEGGIE":     {"L": 0.3500, "Area": 0.1075, "V_canopy": 0.02250, "U_nom": 0.150},
        "APH":        {"L": 0.4500, "Area": 0.1708, "V_canopy": 0.04250, "U_nom": 0.600}
    }
    spec = specs.get(chamber_type, specs["Microgreen"])

    g_val = 9.81
    if "g" in meta:
        m = re.search(r"([0-9.]+)", meta["g"])
        if m: g_val = float(m.group(1))

    # Calculate Richardson number: Ri = g * beta * dT * L / U^2
    beta = 1.0 / 295.15  # air expansion coefficient ~ 3.39e-3 1/K
    dt = 3.0             # nominal canopy-to-air temp diff (K)
    u_ref = spec["U_nom"]
    ri = (g_val * beta * dt * spec["L"]) / (u_ref * u_ref) if u_ref > 0 else 0.0

    metrics = {
        "case_name": os.path.basename(os.path.normpath(case_dir)),
        "chamber": chamber_type,
        "latest_time": latest_time,
        "g": g_val,
        "Ri": ri,
        "growth_area_m2": spec["Area"],
        "canopy_height_m": spec["L"],
        "u_nom_mps": u_ref
    }

    # Extract volFieldValue if exists
    post_dir = os.path.join(case_dir, "postProcessing")
    if os.path.isdir(post_dir):
        # Look for canopy metrics
        for root, _, files in os.walk(post_dir):
            for f in files:
                if f.endswith(".dat"):
                    dat_path = os.path.join(root, f)
                    parsed = parse_openfoam_table(dat_path)
                    if parsed and parsed["data"]:
                        last_row = parsed["data"][-1]
                        for idx, h in enumerate(parsed["headers"]):
                            if idx < len(last_row):
                                metrics[f"{os.path.basename(root)}_{h}"] = last_row[idx]

    return metrics

def print_comparison_table(results):
    """Print ASCII comparison table."""
    print("\n" + "=" * 88)
    print(f"{'Spaceflight Plant Growth Chamber CFD Comparison Summary':^88}")
    print("=" * 88)
    header = f"{'Case Name':<24} | {'Chamber':<10} | {'g (m/s2)':<8} | {'Ri':<8} | {'Area (m2)':<9} | {'U_ref (m/s)':<10} | {'Status':<8}"
    print(header)
    print("-" * 88)
    for r in results:
        status = "Done" if r["latest_time"] else "Init"
        row = f"{r['case_name']:<24} | {r['chamber']:<10} | {r['g']:<8.2f} | {r['Ri']:<8.3e} | {r['growth_area_m2']:<9.4f} | {r['u_nom_mps']:<10.3f} | {status:<8}"
        print(row)
    print("=" * 88 + "\n")

def export_csv(results, out_path):
    """Export comparison metrics to CSV."""
    if not results: return
    keys = list(results[0].keys())
    with open(out_path, "w") as f:
        f.write(",".join(keys) + "\n")
        for r in results:
            vals = [str(r.get(k, "")) for k in keys]
            f.write(",".join(vals) + "\n")
    print(f"Exported comparison CSV to: {out_path}")

def plot_comparisons(results, out_dir):
    """Generate comparative plots using matplotlib if available."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed -- skipping plot generation.")
        return

    os.makedirs(out_dir, exist_ok=True)
    chambers = list(set(r["chamber"] for r in results))

    # Plot 1: Gravity vs Richardson Number
    fig, ax = plt.subplots(figsize=(8, 5))
    markers = {"Microgreen": "o", "VEGGIE": "s", "APH": "^"}
    colors = {"Microgreen": "#1f77b4", "VEGGIE": "#2ca02c", "APH": "#d62728"}

    for ch in chambers:
        pts = [r for r in results if r["chamber"] == ch]
        pts.sort(key=lambda x: x["g"])
        gs = [p["g"] for p in pts]
        ris = [p["Ri"] for p in pts]
        ax.plot(gs, ris, marker=markers.get(ch, "o"), color=colors.get(ch, "black"), label=ch, linewidth=2, markersize=8)

    ax.set_xlabel("Gravity $g$ [m/s²]", fontsize=12)
    ax.set_ylabel("Richardson Number $Ri = Gr / Re^2$", fontsize=12)
    ax.set_title("Buoyancy Scaling Across Spaceflight Chambers", fontsize=14)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.axhline(0.1, color="grey", linestyle=":", label="Forced threshold ($Ri=0.1$)")
    ax.legend(fontsize=10)
    plt.tight_layout()
    plot_file = os.path.join(out_dir, "richardson_scaling.png")
    plt.savefig(plot_file, dpi=200)
    plt.close()
    print(f"Saved plot: {plot_file}")

def main():
    parser = argparse.ArgumentParser(description="Cross-chamber CFD comparison tool.")
    parser.add_argument("cases", nargs="+", help="Run case directories to analyze")
    parser.add_argument("--gravity-sweep", action="store_true", help="Group by chamber and plot gravity scaling")
    parser.add_argument("--output", default="doc/comparison_results", help="Output directory for reports/plots")
    args = parser.parse_args()

    results = []
    for c in args.cases:
        if os.path.isdir(c):
            results.append(extract_case_metrics(c))

    if not results:
        print("No valid case directories provided.")
        sys.exit(1)

    print_comparison_table(results)

    os.makedirs(args.output, exist_ok=True)
    csv_file = os.path.join(args.output, "chamber_comparison_metrics.csv")
    export_csv(results, csv_file)
    plot_comparisons(results, args.output)

if __name__ == "__main__":
    main()
