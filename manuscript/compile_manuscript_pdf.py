#!/usr/bin/env python3
"""
Compile authentic publication-grade npj Microgravity manuscript PDF using Typst.
Produces genuine Nature Portfolio / npj Microgravity journal layout:
- Nature header & DOI banner
- 2-column justified layout with clean typography
- Formatted tables with booktabs styling
- Embedded high-resolution publication figures (Figures 1–9)
- Formatted mathematical equations and bibliography
"""

import os
import sys
import typst

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    typ_path = os.path.join(root, "manuscript.typ")
    pdf_path = os.path.join(root, "npj_manuscript.pdf")
    
    print(f"=== Compiling npj Microgravity Manuscript via Typst: {typ_path} ===")
    typst.compile(typ_path, output=pdf_path)
    print(f"=== Successfully Compiled Publication PDF: {pdf_path} ===")

if __name__ == "__main__":
    main()
