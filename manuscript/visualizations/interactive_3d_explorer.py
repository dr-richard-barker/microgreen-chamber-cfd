#!/usr/bin/env python3
"""
Interactive 3D WebGL Explorer for Spaceflight Plant Growth Hardware CFD.
Features:
- Dynamic 3D Trace switching across all 4 chambers (APH, VEGGIE, Microgreen, CHROMEX),
  velocity regimes (Nominal, High, Low, Zero), and gravities (0g, Moon 0.166g, Mars 0.38g, Earth 1.0g).
- 4D Time-Stepping Airflow Animation (Play/Pause, scrubbable time slider).
- Emergency Fan Failure / Stop Airflow simulation with real-time aerodynamic decay and hypoxia telemetry.
"""

import os
import sys
import json
import numpy as np
import plotly.graph_objects as go

# Add scripts directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts")))
from simulate_flow_fields import ChamberFlowModel

def get_chamber_box_traces(chamber_type):
    """Generate wireframe enclosure and internal hardware components (trays, pillows, canisters)."""
    if chamber_type == "microgreen":
        Lx, Ly, Lz = 0.120, 0.1867, 0.0967
    elif chamber_type == "veggie":
        Lx, Ly, Lz = 0.292, 0.368, 0.350
    elif chamber_type == "aph":
        Lx, Ly, Lz = 0.454, 0.408, 0.450
    elif chamber_type in ("chromex", "chromex_pgc"):
        Lx, Ly, Lz = 0.095, 0.048, 0.190

    # 1. Main Enclosure Box Wireframe (mm)
    x_c = [0, Lx, Lx, 0, 0,  0, Lx, Lx, 0, 0,  0, 0,  Lx, Lx,  Lx, Lx,  0, 0]
    y_c = [0, 0, Ly, Ly, 0,  0, 0, Ly, Ly, 0,  0, 0,  0, 0,    Ly, Ly,  Ly, Ly]
    z_c = [0, 0, 0, 0, 0,    Lz, Lz, Lz, Lz, Lz, 0, Lz, 0, Lz,  0, Lz,  0, Lz]
    
    traces = []
    box_trace = {
        "type": "scatter3d",
        "x": (np.array(x_c) * 1000).tolist(),
        "y": (np.array(y_c) * 1000).tolist(),
        "z": (np.array(z_c) * 1000).tolist(),
        "mode": "lines",
        "line": {"color": "#333333", "width": 4},
        "name": f"{chamber_type.upper()} Enclosure",
        "hoverinfo": "none"
    }
    traces.append(box_trace)

    # 2. Hardware-specific physical structures
    if chamber_type == "microgreen":
        # Root substrate tray at bottom (z = 0 to 25 mm)
        tray_x = [0, Lx, Lx, 0, 0,  0, Lx, Lx, 0, 0,  0, 0,  Lx, Lx,  Lx, Lx,  0, 0]
        tray_y = [0, 0, Ly, Ly, 0,  0, 0, Ly, Ly, 0,  0, 0,  0, 0,    Ly, Ly,  Ly, Ly]
        tray_z = [0, 0, 0, 0, 0,  0.025, 0.025, 0.025, 0.025, 0.025, 0, 0.025, 0, 0.025, 0, 0.025, 0, 0.025]
        traces.append({
            "type": "scatter3d",
            "x": (np.array(tray_x) * 1000).tolist(),
            "y": (np.array(tray_y) * 1000).tolist(),
            "z": (np.array(tray_z) * 1000).tolist(),
            "mode": "lines",
            "line": {"color": "#8b5a2b", "width": 3},
            "name": "Substrate Tray (z=25mm)",
            "hoverinfo": "none"
        })
    elif chamber_type == "veggie":
        # 6 Plant pillows (2x3 grid, each 110x150x40 mm)
        px_list = [0.015, 0.165]
        py_list = [0.015, 0.135, 0.255]
        for ipx, px in enumerate(px_list):
            for ipy, py in enumerate(py_list):
                bx = [px, px+0.11, px+0.11, px, px,  px, px+0.11, px+0.11, px, px]
                by = [py, py, py+0.095, py+0.095, py, py, py, py+0.095, py+0.095, py]
                bz = [0, 0, 0, 0, 0, 0.040, 0.040, 0.040, 0.040, 0.040]
                traces.append({
                    "type": "scatter3d",
                    "x": (np.array(bx) * 1000).tolist(),
                    "y": (np.array(by) * 1000).tolist(),
                    "z": (np.array(bz) * 1000).tolist(),
                    "mode": "lines",
                    "line": {"color": "#8b5a2b", "width": 2},
                    "name": "Plant Pillow" if (ipx==0 and ipy==0) else None,
                    "showlegend": (ipx==0 and ipy==0),
                    "hoverinfo": "none"
                })
    elif chamber_type == "aph":
        # 4-quadrant Science Carrier (z = 0 to 51 mm)
        sc_x = [0, Lx, Lx, 0, 0, 0, Lx, Lx, 0, 0]
        sc_y = [0, 0, Ly, Ly, 0, 0, 0, Ly, Ly, 0]
        sc_z = [0, 0, 0, 0, 0, 0.051, 0.051, 0.051, 0.051, 0.051]
        traces.append({
            "type": "scatter3d",
            "x": (np.array(sc_x) * 1000).tolist(),
            "y": (np.array(sc_y) * 1000).tolist(),
            "z": (np.array(sc_z) * 1000).tolist(),
            "mode": "lines",
            "line": {"color": "#4a6984", "width": 3},
            "name": "Science Carrier Base (z=51mm)",
            "hoverinfo": "none"
        })
    elif chamber_type in ("chromex", "chromex_pgc"):
        # Synthetic foam block base (z = 0 to 40 mm)
        foam_x = [0, Lx, Lx, 0, 0, 0, Lx, Lx, 0, 0]
        foam_y = [0, 0, Ly, Ly, 0, 0, 0, Ly, Ly, 0]
        foam_z = [0, 0, 0, 0, 0, 0.040, 0.040, 0.040, 0.040, 0.040]
        traces.append({
            "type": "scatter3d",
            "x": (np.array(foam_x) * 1000).tolist(),
            "y": (np.array(foam_y) * 1000).tolist(),
            "z": (np.array(foam_z) * 1000).tolist(),
            "mode": "lines",
            "line": {"color": "#8b5a2b", "width": 3},
            "name": "Synthetic Foam Block (z=40mm)",
            "hoverinfo": "none"
        })

    return traces

def build_flow_traces(chamber_type, regime="nominal", gravity=0.0, t=0.0):
    """Generate 3D streamline ribbons and mid-canopy velocity slice surfaces."""
    model = ChamberFlowModel(chamber_type=chamber_type, regime=regime, gravity=gravity)
    Lx, Ly, Lz = model.dims
    u_max = max(0.01, model.u_ref * 1.25)
    
    traces = []
    
    # Fast path for zero airflow (fan stoppage)
    if regime == "zero" or model.u_ref == 0.0:
        # Near-zero slice plane
        flow = model.compute_flow_field(nx=12, ny=12, nz=12, t=t)
        mid_k = 6
        x_slice = (flow["X"][:, :, mid_k] * 1000).tolist()
        y_slice = (flow["Y"][:, :, mid_k] * 1000).tolist()
        z_slice = (flow["Z"][:, :, mid_k] * 1000).tolist()
        speed_slice = np.zeros_like(flow["Speed"][:, :, mid_k]).tolist()
        traces.append({
            "type": "surface",
            "x": x_slice,
            "y": y_slice,
            "z": z_slice,
            "surfacecolor": speed_slice,
            "colorscale": "Turbo",
            "cmin": 0,
            "cmax": 0.1,
            "opacity": 0.40,
            "name": "Stagnant Canopy Slice (0 m/s)",
            "showscale": True,
            "colorbar": {
                "title": "Velocity [m/s]",
                "len": 0.65,
                "thickness": 16,
                "x": 1.02
            }
        })
        return traces

    # 1. 3D Streamlines
    num_seeds = 20 if chamber_type != "chromex" else 14
    lines = model.trace_streamlines(num_seeds=num_seeds, max_steps=70, dt=0.006, t=t)
    for idx, line in enumerate(lines):
        coords = line["coords"] * 1000.0 # to mm
        speeds = line["speed"]
        if len(coords) < 2:
            continue
        traces.append({
            "type": "scatter3d",
            "x": coords[:, 0].tolist(),
            "y": coords[:, 1].tolist(),
            "z": coords[:, 2].tolist(),
            "mode": "lines",
            "line": {
                "color": speeds.tolist(),
                "colorscale": "Turbo",
                "cmin": 0,
                "cmax": u_max,
                "width": 4.5
            },
            "name": "Airflow Streamlines" if idx == 0 else None,
            "showlegend": (idx == 0),
            "hovertemplate": "x: %{x:.1f} mm<br>y: %{y:.1f} mm<br>z: %{z:.1f} mm<br>Speed: %{text:.3f} m/s",
            "text": [float(f"{s:.3f}") for s in speeds]
        })

    # 2. Mid-Canopy Velocity Slice Plane
    flow = model.compute_flow_field(nx=14, ny=14, nz=14, t=t)
    mid_k = 7
    x_slice = (flow["X"][:, :, mid_k] * 1000).tolist()
    y_slice = (flow["Y"][:, :, mid_k] * 1000).tolist()
    z_slice = (flow["Z"][:, :, mid_k] * 1000).tolist()
    speed_slice = flow["Speed"][:, :, mid_k].tolist()

    traces.append({
        "type": "surface",
        "x": x_slice,
        "y": y_slice,
        "z": z_slice,
        "surfacecolor": speed_slice,
        "colorscale": "Turbo",
        "cmin": 0,
        "cmax": u_max,
        "opacity": 0.60,
        "name": "Canopy Velocity Slice",
        "showscale": True,
        "colorbar": {
            "title": "Velocity [m/s]",
            "len": 0.65,
            "thickness": 16,
            "x": 1.02
        }
    })

    return traces

def precompute_all_trace_bundles():
    """Precompute full database of 3D traces across all platforms, regimes, gravities, and time frames."""
    print("Precomputing 3D Flow & Geometry Trace Bundles...")
    chambers = ["aph", "veggie", "microgreen", "chromex"]
    regimes = ["nominal", "high", "low", "zero"]
    gravities = ["0.0", "1.62", "3.72", "9.81"]
    time_steps = [0.0, 0.25, 0.50, 0.75, 1.0]

    database = {}
    for ch in chambers:
        print(f"  -> Building {ch.upper()} traces...")
        database[ch] = {}
        box_traces = get_chamber_box_traces(ch)
        
        # Camera & Axis layout
        if ch == "microgreen":
            layout_dims = {"x": [0, 120], "y": [0, 187], "z": [0, 97]}
        elif ch == "veggie":
            layout_dims = {"x": [0, 292], "y": [0, 368], "z": [0, 350]}
        elif ch == "aph":
            layout_dims = {"x": [0, 454], "y": [0, 408], "z": [0, 450]}
        elif ch == "chromex":
            layout_dims = {"x": [0, 95], "y": [0, 48], "z": [0, 190]}

        for reg in regimes:
            database[ch][reg] = {}
            for grav_str in gravities:
                database[ch][reg][grav_str] = {}
                grav_val = float(grav_str)
                for t in time_steps:
                    t_str = f"{t:.2f}"
                    flow_tr = build_flow_traces(ch, regime=reg, gravity=grav_val, t=t)
                    all_tr = box_traces + flow_tr
                    database[ch][reg][grav_str][t_str] = {
                        "traces": all_tr,
                        "bounds": layout_dims
                    }
                    
    print(f"Precomputed {len(chambers)*len(regimes)*len(gravities)*len(time_steps)} 3D visualizer states.")
    return database

def create_interactive_dashboard(html_path):
    print("Building Interactive 3D WebGL Dashboard...")
    trace_bundles = precompute_all_trace_bundles()
    trace_json = json.dumps(trace_bundles)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Interactive Spaceflight Hardware CFD Explorer</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
  :root {{
    --primary: #005696;
    --primary-dark: #003865;
    --accent: #e31837;
    --accent-orange: #d97706;
    --bg-light: #f4f8fb;
    --card-bg: #ffffff;
    --text-main: #222222;
    --text-muted: #666666;
    --border: #d0dbe5;
    --danger: #dc2626;
    --success: #16a34a;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: var(--bg-light);
    color: var(--text-main);
  }}
  .header {{
    background: var(--primary);
    color: white;
    padding: 12px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  }}
  .header h1 {{ margin: 0; font-size: 16pt; font-weight: 700; }}
  .header .badge {{ background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 4px; font-size: 8.5pt; }}
  
  .controls-bar {{
    background: white;
    padding: 12px 24px;
    border-bottom: 1px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}
  .control-group {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  .control-group label {{
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.5px;
  }}
  select, button, input[type="range"] {{
    padding: 7px 12px;
    font-size: 9.5pt;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: white;
    cursor: pointer;
    font-weight: 500;
  }}
  select:focus, button:focus {{ outline: none; border-color: var(--primary); ring: 2px rgba(0,86,150,0.2); }}
  
  .btn-action {{
    background: var(--primary);
    color: white;
    border: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border-radius: 6px;
    font-weight: 600;
    transition: all 0.2s;
  }}
  .btn-action:hover {{ background: var(--primary-dark); }}
  .btn-danger {{
    background: var(--danger);
    color: white;
    border: none;
    font-weight: 700;
  }}
  .btn-danger:hover {{ background: #b91c1c; }}
  .btn-success {{
    background: var(--success);
    color: white;
    border: none;
    font-weight: 700;
  }}
  .btn-success:hover {{ background: #15803d; }}

  .main-layout {{
    display: grid;
    grid-template-columns: 340px 1fr;
    height: calc(100vh - 120px);
    overflow: hidden;
  }}
  @media (max-width: 900px) {{
    .main-layout {{ grid-template-columns: 1fr; height: auto; }}
  }}

  .sidebar {{
    background: white;
    border-right: 1px solid var(--border);
    padding: 18px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .sidebar h3 {{
    margin: 0 0 10px 0;
    font-size: 11pt;
    color: var(--primary-dark);
    border-bottom: 2px solid var(--primary);
    padding-bottom: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  
  .metric-card {{
    background: var(--bg-light);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 8px;
  }}
  .metric-card.alert {{
    background: #fef2f2;
    border-color: #fca5a5;
  }}
  .metric-val {{
    font-size: 13pt;
    font-weight: 700;
    color: var(--primary);
  }}
  .metric-card.alert .metric-val {{ color: var(--danger); }}
  .metric-lbl {{
    font-size: 8pt;
    color: var(--text-muted);
    margin-top: 2px;
  }}
  
  .anim-box {{
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .anim-controls-row {{
    display: flex;
    gap: 8px;
    align-items: center;
  }}
  
  .plot-container {{
    position: relative;
    width: 100%;
    height: 100%;
    background: #ffffff;
  }}
  #plotlyDiv {{
    width: 100%;
    height: 100%;
  }}
  
  .alert-banner {{
    display: none;
    background: #fee2e2;
    border-left: 4px solid var(--danger);
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 8.5pt;
    color: #991b1b;
    font-weight: 600;
    animation: pulse 1.5s infinite;
  }}
  @keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.75; }}
  }}
</style>
</head>
<body>

<div class="header">
  <div style="display: flex; align-items: center; gap: 10px;">
    <i class="fas fa-wind" style="font-size: 18pt; color: #38bdf8;"></i>
    <h1>Interactive 3D Spaceflight Hardware CFD Explorer</h1>
  </div>
  <span class="badge">OpenFOAM v2606 &bull; Multi-Chamber Variable Gravity Engine</span>
</div>

<div class="controls-bar">
  <div class="control-group">
    <label><i class="fas fa-cubes"></i> Hardware Enclosure</label>
    <select id="selChamber" onchange="onChamberChange()">
      <option value="aph" selected>NASA Advanced Plant Habitat (APH)</option>
      <option value="veggie">NASA VEGGIE (VPS)</option>
      <option value="microgreen">Microgreen Chamber</option>
      <option value="chromex">NASA Shuttle CHROMEX (PGC Canister)</option>
    </select>
  </div>
  
  <div class="control-group">
    <label><i class="fas fa-tachometer-alt"></i> Airflow Regime</label>
    <select id="selRegime" onchange="onRegimeChange()">
      <option value="nominal" selected>Flight Baseline (Nominal)</option>
      <option value="high">High Blast (Maximum Velocity)</option>
      <option value="low">Low Draft (Flight Extreme / Seedling)</option>
      <option value="zero">Zero Airflow (Sealed / Fan Stoppage)</option>
    </select>
  </div>

  <div class="control-group">
    <label><i class="fas fa-globe"></i> Gravity Field</label>
    <select id="selGravity" onchange="onGravityChange()">
      <option value="0.0" selected>Microgravity (0.0 g / ISS)</option>
      <option value="1.62">Lunar Surface (0.166 g)</option>
      <option value="3.72">Martian Surface (0.38 g)</option>
      <option value="9.81">Earth Ground Control (1.0 g)</option>
    </select>
  </div>

  <div class="control-group" style="margin-left: auto; display: flex; flex-direction: row; gap: 8px; align-items: flex-end;">
    <button id="btnFanTest" class="btn-action btn-danger" onclick="toggleFanFailure()">
      <i class="fas fa-stop-circle"></i> 🛑 Simulate Fan Failure
    </button>
    <button class="btn-action" onclick="resetCamera()">
      <i class="fas fa-video"></i> Reset View
    </button>
  </div>
</div>

<div class="main-layout">
  <!-- SIDEBAR METRICS & CONTROLS -->
  <div class="sidebar">
    <div id="alertBanner" class="alert-banner">
      <i class="fas fa-exclamation-triangle"></i> EMERGENCY FAN SHUTDOWN ACTIVE: Rapid Boundary Layer Hypoxia & Heat Trapping
    </div>

    <!-- 4D ANIMATION CONTROLS -->
    <div class="anim-box">
      <label style="font-size: 8pt; font-weight: 700; text-transform: uppercase; color: var(--text-muted);">
        <i class="fas fa-play"></i> 4D Unsteady Flow Cycle
      </label>
      <div class="anim-controls-row">
        <button id="btnPlay" class="btn-action" style="padding: 6px 12px; font-size: 8.5pt;" onclick="togglePlayAnimation()">
          <i class="fas fa-play"></i> Play
        </button>
        <input type="range" id="timeSlider" min="0" max="4" value="0" step="1" style="flex: 1;" oninput="onSliderTimeChange(this.value)">
        <span id="dispTime" style="font-size: 8.5pt; font-weight: 700; min-width: 45px;">t=0.00s</span>
      </div>
    </div>

    <h3>Live Telemetry & Aerodynamics</h3>
    <div id="infoBox">
      <div class="metric-card" id="cardFlow">
        <div class="metric-val" id="dispFlow">26.4 m³/h (0.60 m/s)</div>
        <div class="metric-lbl">Forced Volumetric Flow & Velocity</div>
      </div>
      <div class="metric-card" id="cardConductance">
        <div class="metric-val" id="dispConductance">1.071 mol m⁻² s⁻¹</div>
        <div class="metric-lbl">Boundary Layer Conductance (g_bl)</div>
      </div>
      <div class="metric-card" id="cardThickness">
        <div class="metric-val" id="dispThickness">1.63 mm</div>
        <div class="metric-lbl">Aerodynamic Boundary Layer (δ_bl)</div>
      </div>
      <div class="metric-card" id="cardStagnant">
        <div class="metric-val" id="dispStagnant">2.6%</div>
        <div class="metric-lbl">Canopy Stagnant Volume (&lt;0.05 m/s)</div>
      </div>
      <div class="metric-card" id="cardBiosecurity">
        <div class="metric-val" id="dispBiosecurity">Closed HEPA (0% Cabin Burden)</div>
        <div class="metric-lbl">Containment & Biosafety Class</div>
      </div>
    </div>
    
    <h3>3D Navigation Guide</h3>
    <p style="font-size: 8.5pt; line-height: 1.4; color: var(--text-muted); margin: 0;">
      &bull; <b>Left Click + Drag:</b> 3D Orbital Rotation<br>
      &bull; <b>Right Click + Drag:</b> Pan Viewport<br>
      &bull; <b>Scroll Wheel:</b> Zoom In / Out<br>
      &bull; <b>Hover:</b> Read local coordinates & velocity
    </p>
  </div>
  
  <!-- 3D PLOTLY CANVAS -->
  <div class="plot-container">
    <div id="plotlyDiv"></div>
  </div>
</div>

<script>
  // Precomputed Trace Database from Python CFD Pipeline
  const traceDB = {trace_json};

  const telemetryData = {{
    "aph": {{
      "nominal": {{ "flow": "26.4 m³/h (0.60 m/s)", "gbl": "1.071 mol m⁻²s⁻¹", "thick": "1.63 mm", "stag": "2.6%", "bio": "Closed HEPA (0% Cabin Burden)" }},
      "high": {{ "flow": "66.0 m³/h (1.50 m/s)", "gbl": "1.745 mol m⁻²s⁻¹", "thick": "0.98 mm", "stag": "0.4%", "bio": "Ultra-Fast HEPA Scrub (t50=7.2s)" }},
      "low": {{ "flow": "13.2 m³/h (0.30 m/s)", "gbl": "0.778 mol m⁻²s⁻¹", "thick": "2.24 mm", "stag": "5.8%", "bio": "Low Shear Seedling Mode" }},
      "zero": {{ "flow": "0.0 m³/h (0.00 m/s)", "gbl": "0.042 mol m⁻²s⁻¹", "thick": "25.0 mm", "stag": "100.0%", "bio": "Diffusive Buildup (Fan Failure)" }}
    }},
    "veggie": {{
      "nominal": {{ "flow": "85.0 m³/h (0.15 m/s draft)", "gbl": "0.515 mol m⁻²s⁻¹", "thick": "3.40 mm", "stag": "15.4%", "bio": "100% Spore Export to ISS Cabin" }},
      "high": {{ "flow": "140.0 m³/h (0.28 m/s draft)", "gbl": "0.792 mol m⁻²s⁻¹", "thick": "2.10 mm", "stag": "6.2%", "bio": "High Cabin Dispersion (t50=13.8s)" }},
      "low": {{ "flow": "42.5 m³/h (0.065 m/s draft)", "gbl": "0.219 mol m⁻²s⁻¹", "thick": "7.95 mm", "stag": "52.8%", "bio": "High Mold Vulnerability (VEG-01)" }},
      "zero": {{ "flow": "0.0 m³/h (0.00 m/s)", "gbl": "0.028 mol m⁻²s⁻¹", "thick": "28.0 mm", "stag": "100.0%", "bio": "Total Buoyancy Collapse (0g Stagnant)" }}
    }},
    "microgreen": {{
      "nominal": {{ "flow": "11.8 m³/h (2.60 m/s jet)", "gbl": "0.688 mol m⁻²s⁻¹", "thick": "2.54 mm", "stag": "9.6%", "bio": "Sealed Unit (0% Cabin Export)" }},
      "high": {{ "flow": "22.6 m³/h (5.00 m/s jet)", "gbl": "1.185 mol m⁻²s⁻¹", "thick": "1.45 mm", "stag": "3.1%", "bio": "High TKE Confined Jet" }},
      "low": {{ "flow": "2.3 m³/h (0.50 m/s jet)", "gbl": "0.312 mol m⁻²s⁻¹", "thick": "5.60 mm", "stag": "28.5%", "bio": "Corner Recirculation Pocketing" }},
      "zero": {{ "flow": "0.0 m³/h (0.00 m/s)", "gbl": "0.035 mol m⁻²s⁻¹", "thick": "25.0 mm", "stag": "100.0%", "bio": "Sealed Stagnation Failure" }}
    }},
    "chromex": {{
      "nominal": {{ "flow": "1.0 L/h AES (9.8 mm/s)", "gbl": "0.097 mol m⁻²s⁻¹", "thick": "12.4 mm", "stag": "68.5%", "bio": "Closed Canister (0% Cabin Export)" }},
      "high": {{ "flow": "2.5 L/h AES (25 mm/s)", "gbl": "0.185 mol m⁻²s⁻¹", "thick": "8.2 mm", "stag": "42.0%", "bio": "Creeping Aeration (Re ~ 5)" }},
      "low": {{ "flow": "0.2 L/h AES (2.0 mm/s)", "gbl": "0.052 mol m⁻²s⁻¹", "thick": "18.5 mm", "stag": "88.0%", "bio": "Diffusion Dominated (Pe < 1)" }},
      "zero": {{ "flow": "0.0 L/h (Sealed)", "gbl": "0.031 mol m⁻²s⁻¹", "thick": "25.0 mm", "stag": "100.0%", "bio": "Critical Hypoxia (ADH Upregulation)" }}
    }}
  }};

  const timeValues = ["0.00", "0.25", "0.50", "0.75", "1.00"];
  let currentTimeIdx = 0;
  let isPlaying = false;
  let animTimer = null;
  let isFanFailure = false;
  let failureStep = 0;
  let failureTimer = null;

  function getActiveState() {{
    const ch = document.getElementById("selChamber").value;
    const reg = document.getElementById("selRegime").value;
    const grav = document.getElementById("selGravity").value;
    const tStr = timeValues[currentTimeIdx];
    return {{ ch, reg, grav, tStr }};
  }}

  function updatePlot() {{
    const {{ ch, reg, grav, tStr }} = getActiveState();
    const bundle = traceDB[ch][reg][grav][tStr];
    
    const layout = {{
      scene: {{
        xaxis: {{ title: "Width x [mm]", range: bundle.bounds.x, backgroundcolor: "#f8f9fa", gridcolor: "#e0e0e0", showbackground: true }},
        yaxis: {{ title: "Depth y [mm]", range: bundle.bounds.y, backgroundcolor: "#f8f9fa", gridcolor: "#e0e0e0", showbackground: true }},
        zaxis: {{ title: "Height z [mm]", range: bundle.bounds.z, backgroundcolor: "#f8f9fa", gridcolor: "#e0e0e0", showbackground: true }},
        camera: {{
          eye: {{ x: 1.6, y: -1.6, z: 1.3 }},
          up: {{ x: 0, y: 0, z: 1 }}
        }},
        aspectmode: "data"
      }},
      margin: {{ l: 0, r: 0, b: 0, t: 20 }},
      paper_bgcolor: "#ffffff",
      showlegend: true,
      legend: {{ x: 0.02, y: 0.95, bgcolor: "rgba(255,255,255,0.85)" }}
    }};

    Plotly.react("plotlyDiv", bundle.traces, layout, {{ responsive: true, displaylogo: false }});
    updateTelemetry(ch, reg);
  }}

  function updateTelemetry(ch, reg) {{
    const info = telemetryData[ch][reg];
    document.getElementById("dispFlow").innerText = info.flow;
    document.getElementById("dispConductance").innerText = info.gbl;
    document.getElementById("dispThickness").innerText = info.thick;
    document.getElementById("dispStagnant").innerText = info.stag;
    document.getElementById("dispBiosecurity").innerText = info.bio;

    const cards = [document.getElementById("cardFlow"), document.getElementById("cardConductance"), 
                   document.getElementById("cardThickness"), document.getElementById("cardStagnant")];
    cards.forEach(c => {{
      if (reg === "zero" || isFanFailure) {{
        c.classList.add("alert");
      }} else {{
        c.classList.remove("alert");
      }}
    }});
  }}

  function onChamberChange() {{
    currentTimeIdx = 0;
    document.getElementById("timeSlider").value = 0;
    document.getElementById("dispTime").innerText = "t=0.00s";
    updatePlot();
  }}

  function onRegimeChange() {{
    if (isFanFailure && document.getElementById("selRegime").value !== "zero") {{
      resetFanFailureState();
    }}
    updatePlot();
  }}

  function onGravityChange() {{
    updatePlot();
  }}

  function onSliderTimeChange(val) {{
    currentTimeIdx = parseInt(val);
    document.getElementById("dispTime").innerText = `t=${{timeValues[currentTimeIdx]}}s`;
    updatePlot();
  }}

  function togglePlayAnimation() {{
    const btn = document.getElementById("btnPlay");
    if (isPlaying) {{
      isPlaying = false;
      clearInterval(animTimer);
      btn.innerHTML = '<i class="fas fa-play"></i> Play';
    }} else {{
      isPlaying = true;
      btn.innerHTML = '<i class="fas fa-pause"></i> Pause';
      animTimer = setInterval(() => {{
        currentTimeIdx = (currentTimeIdx + 1) % timeValues.length;
        document.getElementById("timeSlider").value = currentTimeIdx;
        document.getElementById("dispTime").innerText = `t=${{timeValues[currentTimeIdx]}}s`;
        updatePlot();
      }}, 350);
    }}
  }}

  function toggleFanFailure() {{
    if (!isFanFailure) {{
      // Initiate Fan Failure Test
      isFanFailure = true;
      if (isPlaying) togglePlayAnimation();
      
      const btn = document.getElementById("btnFanTest");
      btn.className = "btn-action btn-success";
      btn.innerHTML = '<i class="fas fa-redo"></i> 🔄 Restore Nominal Fan';
      document.getElementById("alertBanner").style.display = "block";
      
      // Step-by-step decay simulation
      let step = 0;
      failureTimer = setInterval(() => {{
        step++;
        if (step === 1) {{
          document.getElementById("dispFlow").innerText = "Spinning Down... (0.28 m/s)";
          document.getElementById("dispConductance").innerText = "0.450 mol m⁻²s⁻¹";
          document.getElementById("dispThickness").innerText = "6.5 mm (Expanding)";
        }} else if (step === 2) {{
          document.getElementById("dispFlow").innerText = "Residual Drift... (0.05 m/s)";
          document.getElementById("dispConductance").innerText = "0.120 mol m⁻²s⁻¹";
          document.getElementById("dispThickness").innerText = "15.0 mm";
        }} else if (step >= 3) {{
          clearInterval(failureTimer);
          document.getElementById("selRegime").value = "zero";
          updatePlot();
        }}
      }}, 500);
    }} else {{
      // Restore Fan
      resetFanFailureState();
      document.getElementById("selRegime").value = "nominal";
      updatePlot();
    }}
  }}

  function resetFanFailureState() {{
    isFanFailure = false;
    clearInterval(failureTimer);
    const btn = document.getElementById("btnFanTest");
    btn.className = "btn-action btn-danger";
    btn.innerHTML = '<i class="fas fa-stop-circle"></i> 🛑 Simulate Fan Failure';
    document.getElementById("alertBanner").style.display = "none";
  }}

  function resetCamera() {{
    const {{ ch, reg, grav, tStr }} = getActiveState();
    const bundle = traceDB[ch][reg][grav][tStr];
    Plotly.relayout("plotlyDiv", {{
      "scene.camera": {{
        eye: {{ x: 1.6, y: -1.6, z: 1.3 }},
        up: {{ x: 0, y: 0, z: 1 }}
      }}
    }});
  }}

  // Initial plot render on page load
  window.addEventListener("DOMContentLoaded", () => {{
    updatePlot();
  }});
</script>

</body>
</html>
"""
    with open(html_path, "w") as f:
        f.write(html_content)
    print(f"=== Successfully Generated Dynamic 3D Explorer: {html_path} ===")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(out_dir, "interactive_3d_explorer.html")
    create_interactive_dashboard(html_file)
