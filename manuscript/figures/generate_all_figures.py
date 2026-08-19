#!/usr/bin/env python3
"""
Master figure generator script for the npj Microgravity manuscript.
Runs Figures 1 to 5 and outputs vector PDFs and 300-DPI PNGs.
"""

import os
import sys

from fig1_hardware_domains import create_fig1
from fig2_gravity_richardson import create_fig2
from fig3_canopy_aerodynamics import create_fig3
from fig4_scalar_ventilation import create_fig4
from fig5_biosecurity_trades import create_fig5
from fig6_3d_flow_topologies import create_fig6
from fig7_airflow_extremes import create_fig7

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(root, "output")
    os.makedirs(out, exist_ok=True)

    print(f"=== Generating All Publication Figures for npj Microgravity in {out} ===")
    create_fig1(out)
    create_fig2(out)
    create_fig3(out)
    create_fig4(out)
    create_fig5(out)
    create_fig6(out)
    create_fig7(out)
    print("=== All 7 Figures Generated Successfully! ===")

if __name__ == "__main__":
    main()
