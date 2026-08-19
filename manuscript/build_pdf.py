#!/usr/bin/env python3
"""
Compile the npj Microgravity manuscript into a publication-grade PDF using
Nature Journal CSS styling, MathJax mathematical rendering, and headless Chromium.
"""

import os
import subprocess
import sys

def build_html_manuscript(html_path):
    fig_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "figures", "output"))
    fig1 = os.path.join(fig_dir, "Fig1_hardware_domains.png")
    fig2 = os.path.join(fig_dir, "Fig2_gravity_richardson.png")
    fig3 = os.path.join(fig_dir, "Fig3_canopy_aerodynamics.png")
    fig4 = os.path.join(fig_dir, "Fig4_scalar_ventilation.png")
    fig5 = os.path.join(fig_dir, "Fig5_biosecurity_trades.png")

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Aerodynamic Boundary-Layer Scaling and Enclosure Regimes Across Spaceflight Plant Growth Hardware</title>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
  @page {
    size: A4;
    margin: 20mm 18mm 22mm 18mm;
    @bottom-right {
      content: counter(page);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 9pt;
      color: #666;
    }
  }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #222;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }

  .journal-header {
    border-bottom: 3px solid #005696;
    padding-bottom: 8px;
    margin-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .journal-logo {
    font-size: 18pt;
    font-weight: 800;
    color: #005696;
    letter-spacing: -0.5px;
  }
  .journal-logo span {
    color: #e31837;
    font-style: italic;
  }
  .article-type {
    font-size: 10pt;
    font-weight: 700;
    text-transform: uppercase;
    color: #555;
    letter-spacing: 1px;
  }
  
  h1.title {
    font-size: 18pt;
    font-weight: 800;
    line-height: 1.25;
    color: #111;
    margin: 0 0 15px 0;
  }
  
  .authors {
    font-size: 11pt;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
  }
  .affiliations {
    font-size: 8.5pt;
    color: #555;
    margin-bottom: 20px;
    line-height: 1.4;
  }
  .affiliations sup {
    color: #005696;
    font-weight: bold;
  }
  
  .abstract-box {
    background-color: #f4f8fb;
    border-left: 4px solid #005696;
    padding: 14px 18px;
    margin-bottom: 25px;
    border-radius: 0 4px 4px 0;
  }
  .abstract-box h2 {
    font-size: 10pt;
    text-transform: uppercase;
    font-weight: 800;
    color: #005696;
    margin: 0 0 8px 0;
    letter-spacing: 0.5px;
  }
  .abstract-box p {
    font-size: 9.5pt;
    margin: 0;
    line-height: 1.5;
    color: #222;
    text-align: justify;
  }

  h2.section-title {
    font-size: 13pt;
    font-weight: 800;
    color: #005696;
    border-bottom: 1px solid #dde5ed;
    padding-bottom: 4px;
    margin-top: 25px;
    margin-bottom: 12px;
  }
  h3.subsection-title {
    font-size: 11pt;
    font-weight: 700;
    color: #222;
    margin-top: 18px;
    margin-bottom: 8px;
  }

  p {
    text-align: justify;
    margin-bottom: 12px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }
  th {
    background-color: #f8f9fa;
    color: #111;
    font-weight: 700;
    text-align: left;
    padding: 7px 8px;
    border-top: 2px solid #333;
    border-bottom: 1px solid #333;
  }
  td {
    padding: 6px 8px;
    border-bottom: 1px solid #e9ecef;
    vertical-align: top;
  }
  tr:last-child td {
    border-bottom: 2px solid #333;
  }
  .table-caption {
    font-size: 8.5pt;
    font-weight: 600;
    margin-bottom: 6px;
    color: #333;
  }
  .table-caption span.tab-num {
    font-weight: 800;
    color: #005696;
  }

  .figure-box {
    margin: 22px 0;
    text-align: center;
    page-break-inside: avoid;
  }
  .figure-box img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  .figure-caption {
    font-size: 8.5pt;
    text-align: justify;
    margin-top: 8px;
    color: #333;
    line-height: 1.4;
  }
  .figure-caption span.fig-num {
    font-weight: 800;
    color: #005696;
  }

  .equation {
    text-align: center;
    margin: 12px 0;
    font-size: 10.5pt;
  }

  .references {
    font-size: 8pt;
    line-height: 1.4;
  }
  .references ol {
    padding-left: 18px;
    margin: 0;
  }
  .references li {
    margin-bottom: 6px;
  }
</style>
</head>
<body>

<div class="journal-header">
  <div class="journal-logo">npj <span>Microgravity</span></div>
  <div class="article-type">Article | Open Access</div>
</div>

<h1 class="title">Aerodynamic Boundary-Layer Scaling and Enclosure Regimes Across Spaceflight Plant Growth Hardware: A Multi-Chamber OpenFOAM CFD Framework under Variable Gravity</h1>

<div class="authors">
  Richard Barker<sup>1,*</sup>, Henry Ewald<sup>1</sup>, and Astrobotany Consortium<sup>1,2</sup>
</div>

<div class="affiliations">
  <sup>1</sup> Department of Botany, University of Wisconsin–Madison, Madison, WI 53706, USA<br>
  <sup>2</sup> NASA GeneLab Plant Analysis Working Group (AWG), Moffett Field, CA 94035, USA<br>
  <sup>*</sup> Corresponding author: <code>rbarker2@wisc.edu</code>
</div>

<div class="abstract-box">
  <h2>Abstract</h2>
  <p>
    Plants cultivated in extraterrestrial habitats encounter a physical environment devoid of natural gravity-driven buoyancy (\(Gr \to 0\)), expanding unstirred fluid boundary layers around vegetative canopies and drastically elevating aerodynamic resistance (\(r_a = 1/g_{bl}\)). Here, we present a systematic, multi-chamber 3D computational fluid dynamics (CFD) investigation comparing three distinct spaceflight and controlled-environment agricultural hardware architectures across four gravitational regimes: Earth (\(1.0\text{ g}\)), Mars (\(0.38\text{ g}\)), Moon (\(0.166\text{ g}\)), and Microgravity (\(0\text{ g}\)). Using an OpenFOAM v2606 finite-volume framework with conformal multi-solid analytic geometries, we model: (i) the compact <b>Microgreen Chamber</b> (\(2.33\text{ L}\), through-flow confined jet), (ii) the <b>NASA Vegetable Production System (VEGGIE/VPS)</b> (\(37.6\text{ L}\), top suction with passive cabin air induction), and (iii) the <b>NASA Advanced Plant Habitat (APH)</b> (\(83.4\text{ L}\), ducted closed-loop opposing cross-flow). Parametric gravity sweeps reveal that ceiling-mounted LED arrays induce stable thermal stratification on Earth (\(Ri \approx 0.14 - 1.55\)), which suppresses vertical exchange; counter-intuitively, microgravity collapses this stratification, rendering purely forced convection (\(Ri = 0\)) superior in turbulent kinetic energy and canopy clearance. In VEGGIE, low-fan microgravity operation leads to a critical \(52.8\%\) canopy stagnation volume and a \(39.5\%\) reduction in \(CO_2\) boundary layer conductance (\(g_{bl} = 0.219\text{ mol m}^{-2}\text{s}^{-1}\)), elevating fungal mold vulnerability and guttation stress. Conversely, APH's opposing lateral supply jets (\(0.3 - 1.5\text{ m/s}\)) maintain near-ideal displacement ventilation (air exchange efficiency \(\varepsilon_a \approx 45\%\)) and invariant \(g_{bl} \approx 1.07\text{ mol m}^{-2}\text{s}^{-1}\) across all gravity levels. Analysis of suspended bioaerosols establishes a fundamental biosecurity trade-off: VEGGIE exports \(100\%\) of aerosolized fungal spores directly into astronaut living quarters (\(t_{50} = 13.8\text{ s}\)), whereas APH achieves rapid internal HEPA scrubbing (\(t_{50} = 18.4\text{ s}\)) with zero cabin burden. These findings establish quantitative aerodynamic criteria for designing next-generation bioregenerative life support systems for Lunar and Martian surface missions.
  </p>
</div>

<h2 class="section-title">Introduction</h2>
<p>
  Sustained human exploration of the Moon and Mars under NASA's Artemis and Moon-to-Mars architectures necessitates robust Bioregenerative Life Support Systems (BLSS) capable of producing fresh nutritious crops, recycling water, and revitalizing habitat atmospheres. In spaceflight environments, the absence of natural gravitational acceleration fundamentally alters fluid physics: natural thermal convection ceases (\(Gr \to 0, Ra \to 0\)), removing the buoyancy forces that drive passive air circulation and scalar transport around terrestrial plant canopies.
</p>
<p>
  Under microgravity (\(\mu\text{g}\)), leaves become encased in thickened, stagnant fluid boundary layers, severely increasing aerodynamic resistance (\(r_a = 1/g_{bl}\)) to carbon dioxide (\(CO_2\)) assimilation, transpirational cooling, and volatile release. Without adequate forced convective stirring, localized \(CO_2\) depletion within the canopy suppresses RuBisCO carboxylation efficiency and triggers photorespiratory stress, while transpirational moisture accumulation creates persistent boundary-layer humidity (\(RH > 90\%\)), leading to stomatal dysregulation, hyper-guttation, and devastating fungal phytopathogen outbreaks, such as the <i>Fusarium oxysporum</i> epidemic observed during early VEG-01 flight validation.
</p>

<div class="figure-box">
  <img src="file://__FIG1__" alt="Figure 1">
  <div class="figure-caption">
    <span class="fig-num">Figure 1 | 3D Hardware domain architecture, flow topologies, and aerodynamic design envelopes across the three flight and phenotyping systems.</span>
    <b>a</b>, Cross-sectional schematic of the Microgreen Chamber (\(2.33\text{ L}\) volume) showing the \(\varnothing40\text{ mm}\) through-flow jet and parabolic ceiling. <b>b</b>, NASA VEGGIE/VPS (\(37.6\text{ L}\)) displaying top suction fan, four passive base slots, and 6-pillow configuration. <b>c</b>, NASA Advanced Plant Habitat (\(83.4\text{ L}\)) showing dual lateral supply slots, diffuser baffles, and 4-quadrant Science Carrier. <b>d</b>, Usable growth area and canopy air volume comparison. <b>e</b>, Volumetric flow rate (\(Q\)) and bulk velocity (\(U\)). <b>f</b>, Nominal air exchange rate (\(\text{ACH}\)) and residence time (\(\tau_0\)).
  </div>
</div>

<h2 class="section-title">Results</h2>

<h3 class="subsection-title">Hardware Fluid Domains and Baseline Aerodynamics at 1 g</h3>
<p>
  The geometric and aerodynamic parameters of the three hardware architectures are summarized in Table 1. The fluid domains span nearly two orders of magnitude in volume, ranging from \(2.33\text{ L}\) (Microgreen Chamber) to \(37.61\text{ L}\) (VEGGIE at nominal \(350\text{ mm}\) bellows extension) and \(83.36\text{ L}\) (APH shoot zone).
</p>

<div class="table-caption">
  <span class="tab-num">Table 1 |</span> Physical, aerodynamic, and environmental control specifications across the three plant growth hardware architectures.
</div>
<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Microgreen Chamber</th>
      <th>VEGGIE (VPS)</th>
      <th>Advanced Plant Habitat (APH)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Payload Classification</b></td>
      <td>Educational / Phenotyping</td>
      <td>Deployable Space Garden</td>
      <td>Closed-Loop Phytotron</td>
    </tr>
    <tr>
      <td><b>Enclosure Structure</b></td>
      <td>Rigid acrylic + parabolic hood</td>
      <td>Collapsible FEP bellows</td>
      <td>Carbon-fiber & titanium frame</td>
    </tr>
    <tr>
      <td><b>Growth Footprint (\(A\))</b></td>
      <td>\(0.0224\text{ m}^2\) (\(120 \times 187\text{ mm}\))</td>
      <td>\(0.1075\text{ m}^2\) (\(292 \times 368\text{ mm}\))</td>
      <td>\(0.1708\text{ m}^2\) (\(454 \times 408\text{ mm}\))</td>
    </tr>
    <tr>
      <td><b>Canopy Volume (\(V_{air}\))</b></td>
      <td>\(2.33\text{ L}\)</td>
      <td>\(37.61\text{ L}\)</td>
      <td>\(83.36\text{ L}\) (shoot zone)</td>
    </tr>
    <tr>
      <td><b>Primary Flow Driver</b></td>
      <td>1\(\times\) Axial Fan (\(\varnothing40\text{ mm}\))</td>
      <td>1\(\times\) Top Suction Fan (\(\varnothing50\text{ mm}\))</td>
      <td>2\(\times\) Symmetric ECS Blowers</td>
    </tr>
    <tr>
      <td><b>Airflow Topology</b></td>
      <td>Through-flow confined jet</td>
      <td>Bottom-up forced suction</td>
      <td>Opposing lateral cross-flow \(\to\) sweep</td>
    </tr>
    <tr>
      <td><b>Nominal Flow Rate (\(Q\))</b></td>
      <td>\(11.8\text{ m}^3/\text{h}\) (\(3.27\text{ L/s}\))</td>
      <td>\(85.0\text{ m}^3/\text{h}\) (\(23.61\text{ L/s}\))</td>
      <td>\(26.4\text{ m}^3/\text{h}\) (\(7.34\text{ L/s}\))</td>
    </tr>
    <tr>
      <td><b>Canopy Velocity (\(U_{canopy}\))</b></td>
      <td>\(0.262\text{ m/s}\) (bulk mean)</td>
      <td>\(0.150\text{ m/s}\) (mean draft)</td>
      <td>\(0.300 - 1.500\text{ m/s}\) (controlled)</td>
    </tr>
    <tr>
      <td><b>Air Exchange Rate (\(\text{ACH}\))</b></td>
      <td>\(5,051\text{ h}^{-1}\) (\(\tau = 0.71\text{ s}\))</td>
      <td>\(2,260\text{ h}^{-1}\) (\(\tau = 1.60\text{ s}\))</td>
      <td>\(317\text{ h}^{-1}\) (\(\tau = 11.35\text{ s}\))</td>
    </tr>
    <tr>
      <td><b>Environmental Control</b></td>
      <td>None (ambient lab)</td>
      <td>Cabin-coupled (\(\Delta T = +1.5 - 3^\circ\text{C}\))</td>
      <td>Active closed loop (\(18 - 30^\circ\text{C} \pm 0.5\))</td>
    </tr>
    <tr>
      <td><b>Cabin Interface</b></td>
      <td>Sealed</td>
      <td>Open continuous mass exchange</td>
      <td>Closed loop within EXPRESS Rack</td>
    </tr>
  </tbody>
</table>

<div class="figure-box">
  <img src="file://__FIG2__" alt="Figure 2">
  <div class="figure-caption">
    <span class="fig-num">Figure 2 | Richardson number (\(Ri\)) scaling, buoyancy collapse, and aerodynamic regime transitions across gravitational fields.</span>
    <b>a</b>, \(Ri = Gr / Re^2\) trajectory as a function of gravitational acceleration \(g\) for each hardware platform; horizontal bands demarcate forced-dominated (\(Ri < 0.1\)), mixed (\(0.1 \le Ri \le 1.0\)), and buoyant (\(Ri > 1.0\)) regimes. <b>b</b>, Grashof (\(Gr\)) vs. Reynolds (\(Re\)) regime map. <b>c</b>, Thermal stratification index (\(I_{strat} = \Delta T / \overline{T}\)) decay from \(1\text{ g}\) to \(\mu\text{g}\). <b>d</b>, Canopy aerodynamic resistance (\(r_a = 1/g_{bl}\)) under variable gravity.
  </div>
</div>

<h3 class="subsection-title">Gravity Scaling and the Richardson Number Regime Transition</h3>
<p>
  To quantify the transition between buoyancy-driven and momentum-driven convection, we conducted parametric gravity sweeps across \(g \in \{9.81, 3.72, 1.62, 0.00\}\text{ m/s}^2\), evaluating the dimensionless Grashof (\(Gr\)), Reynolds (\(Re\)), and Richardson (\(Ri\)) numbers:
</p>
<div class="equation">
  \[ Gr = \frac{g \beta \Delta T L^3}{\nu^2}, \quad Re = \frac{U L}{\nu}, \quad Ri = \frac{Gr}{Re^2} = \frac{g \beta \Delta T L}{U^2} \]
</div>
<p>
  As illustrated in Figure 2 and Table 2, VEGGIE under Low Fan at \(1\text{ g}\) operates at \(Ri = 1.551\), placing it in the buoyancy-dominated mixed convection regime. When gravity is removed in microgravity (\(0\text{ g}\)), natural thermal buoyancy vanishes completely (\(Gr = 0, Ri = 0\)). Without the buoyancy-assisted chimney effect, low-fan operation fails to penetrate the dense plant canopy, resulting in a critical \(52.8\%\) stagnant volume fraction. Conversely, APH maintains \(Ri \le 0.1246\) at \(1\text{ g}\) and \(Ri \le 0.0473\) under planetary gravities, remaining strictly within the forced convective regime across all missions.
</p>

<div class="table-caption">
  <span class="tab-num">Table 2 |</span> Dimensionless aerodynamic scaling and convection regime matrix across hardware under variable gravity.
</div>
<table>
  <thead>
    <tr>
      <th>Chamber</th>
      <th>Gravity Regime</th>
      <th>\(g\text{ (m/s}^2\text{)}\)</th>
      <th>\(Gr\)</th>
      <th>\(Re\)</th>
      <th>\(Ri\text{ }(Gr/Re^2)\)</th>
      <th>Convective Regime</th>
      <th>Dominant Mechanism</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Microgreen</b></td>
      <td>Earth (\(1\text{ g}\))</td>
      <td>\(9.81\)</td>
      <td>\(3.87 \times 10^{5}\)</td>
      <td>\(1,669\)</td>
      <td>\(0.1405\)</td>
      <td>Mixed Convection</td>
      <td>Fan jet + ceiling stratification</td>
    </tr>
    <tr>
      <td></td>
      <td>Mars (\(0.38\text{ g}\))</td>
      <td>\(3.72\)</td>
      <td>\(1.47 \times 10^{5}\)</td>
      <td>\(1,669\)</td>
      <td>\(0.0533\)</td>
      <td>Forced-Dominated</td>
      <td>Jet momentum dominates</td>
    </tr>
    <tr>
      <td></td>
      <td>Moon (\(0.166\text{ g}\))</td>
      <td>\(1.62\)</td>
      <td>\(6.39 \times 10^{4}\)</td>
      <td>\(1,669\)</td>
      <td>\(0.0232\)</td>
      <td>Forced-Dominated</td>
      <td>Buoyancy negligible</td>
    </tr>
    <tr>
      <td></td>
      <td>Microgravity (\(0\text{ g}\))</td>
      <td>\(0.00\)</td>
      <td>\(0.00\)</td>
      <td>\(1,669\)</td>
      <td>\(0.0000\)</td>
      <td>Purely Forced</td>
      <td>Flapping confined jet only</td>
    </tr>
    <tr>
      <td><b>VEGGIE</b></td>
      <td>Earth (\(1\text{ g}\))</td>
      <td>\(9.81\)</td>
      <td>\(1.83 \times 10^{7}\)</td>
      <td>\(3,463\)</td>
      <td>\(1.5511\)</td>
      <td>Mixed (Buoyant)</td>
      <td>Thermal plume assists fan</td>
    </tr>
    <tr>
      <td></td>
      <td>Mars (\(0.38\text{ g}\))</td>
      <td>\(3.72\)</td>
      <td>\(6.95 \times 10^{6}\)</td>
      <td>\(3,463\)</td>
      <td>\(0.5880\)</td>
      <td>Mixed (Transitional)</td>
      <td>Weak plume, fan required</td>
    </tr>
    <tr>
      <td></td>
      <td>Moon (\(0.166\text{ g}\))</td>
      <td>\(1.62\)</td>
      <td>\(3.03 \times 10^{6}\)</td>
      <td>\(3,463\)</td>
      <td>\(0.2561\)</td>
      <td>Forced-Dominated</td>
      <td>Low draft, mold risk at low fan</td>
    </tr>
    <tr>
      <td></td>
      <td>Microgravity (\(0\text{ g}\))</td>
      <td>\(0.00\)</td>
      <td>\(0.00\)</td>
      <td>\(3,463\)</td>
      <td>\(0.0000\)</td>
      <td>Purely Forced</td>
      <td>Unstirred boundary layer (low fan)</td>
    </tr>
    <tr>
      <td><b>APH</b></td>
      <td>Earth (\(1\text{ g}\))</td>
      <td>\(9.81\)</td>
      <td>\(3.90 \times 10^{7}\)</td>
      <td>\(17,810\)</td>
      <td>\(0.1246\)</td>
      <td>Forced-Dominated</td>
      <td>Dual cross-jets suppress plumes</td>
    </tr>
    <tr>
      <td></td>
      <td>Mars (\(0.38\text{ g}\))</td>
      <td>\(3.72\)</td>
      <td>\(1.48 \times 10^{7}\)</td>
      <td>\(17,810\)</td>
      <td>\(0.0473\)</td>
      <td>Strongly Forced</td>
      <td>Piston-like upward sweep</td>
    </tr>
    <tr>
      <td></td>
      <td>Moon (\(0.166\text{ g}\))</td>
      <td>\(1.62\)</td>
      <td>\(6.44 \times 10^{6}\)</td>
      <td>\(17,810\)</td>
      <td>\(0.0206\)</td>
      <td>Strongly Forced</td>
      <td>Uniform boundary layer</td>
    </tr>
    <tr>
      <td></td>
      <td>Microgravity (\(0\text{ g}\))</td>
      <td>\(0.00\)</td>
      <td>\(0.00\)</td>
      <td>\(17,810\)</td>
      <td>\(0.0000\)</td>
      <td>Purely Forced</td>
      <td>Engineered forced circulation</td>
    </tr>
  </tbody>
</table>

<div class="figure-box">
  <img src="file://__FIG3__" alt="Figure 3">
  <div class="figure-caption">
    <span class="fig-num">Figure 3 | Canopy microclimatic boundary-layer profiles, turbulence, and mass conductance (\(g_{bl}\)).</span>
    <b>a</b>, Vertical velocity profiles normalized by chamber height (\(z/H\)). <b>b</b>, Boundary-layer conductance \(g_{bl}\) for \(CO_2\) mass transfer as a function of forced velocity \(U\), compared against laminar (\(Sh \propto Re^{0.5}\)) and turbulent (\(Sh \propto Re^{0.8}\)) boundary layer theory. <b>c</b>, Canopy turbulent kinetic energy (TKE) across operational modes. <b>d</b>, Canopy stagnant volume fraction (\(U < 0.05\text{ m/s}\)) with fungal pathogen threshold.
  </div>
</div>

<h3 class="subsection-title">Canopy Boundary-Layer Conductance and Microclimatic Stress</h3>
<p>
  Boundary-layer conductance to \(CO_2\) mass transfer (\(g_{bl}\)) dictates photosynthetic carbon assimilation and transpirational cooling:
</p>
<div class="equation">
  \[ Sh_{CO2} = \frac{h_m d_{leaf}}{D_{CO2}}, \quad g_{bl} = \frac{D_{CO2} Sh_{CO2}}{d_{leaf}} \cdot \left(\frac{P}{R T}\right) \]
</div>
<p>
  As detailed in Table 3 and Figure 3, APH maintains an exceptionally high and uniform boundary layer conductance (\(g_{bl} = 1.071 - 1.102\text{ mol m}^{-2}\text{s}^{-1}\)) under nominal \(0.6\text{ m/s}\) supply across all gravities. In contrast, VEGGIE under Low Fan in microgravity suffers a severe conductance reduction down to \(0.219\text{ mol m}^{-2}\text{s}^{-1}\) (\(\delta_{bl} = 7.95\text{ mm}\)), creating a rate-limiting aerodynamic resistance (\(r_a = 4.56\text{ m}^2\text{s/mol}\)) that exceeds stomatal resistance, explaining the localized high humidity and tipburn observed during ISS growth cycles.
</p>

<div class="table-caption">
  <span class="tab-num">Table 3 |</span> Canopy boundary-layer aerodynamic parameters and effective conductance (\(g_{bl}\)) across platforms.
</div>
<table>
  <thead>
    <tr>
      <th>Hardware</th>
      <th>Gravity</th>
      <th>Operating Mode</th>
      <th>\(\overline{U}_{canopy}\text{ (m/s)}\)</th>
      <th>\(\text{TKE}\text{ (m}^2/\text{s}^2\text{)}\)</th>
      <th>\(\delta_{bl}\text{ (mm)}\)</th>
      <th>\(Sh_{CO2}\)</th>
      <th>\(g_{bl}\text{ (mol m}^{-2}\text{s}^{-1}\text{)}\)</th>
      <th>Stagnant Vol. (\(\%\))</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Microgreen</b></td>
      <td>\(1\text{ g}\)</td>
      <td>Baseline</td>
      <td>\(0.262\)</td>
      <td>\(4.82 \times 10^{-3}\)</td>
      <td>\(2.41\)</td>
      <td>\(28.4\)</td>
      <td>\(0.724\)</td>
      <td>\(14.2\%\)</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>Microgravity</td>
      <td>\(0.262\)</td>
      <td>\(4.40 \times 10^{-3}\)</td>
      <td>\(2.54\)</td>
      <td>\(27.0\)</td>
      <td>\(0.688\)</td>
      <td>\(9.6\%\)</td>
    </tr>
    <tr>
      <td><b>VEGGIE</b></td>
      <td>\(1\text{ g}\)</td>
      <td>Low Fan</td>
      <td>\(0.065\)</td>
      <td>\(1.12 \times 10^{-3}\)</td>
      <td>\(4.82\)</td>
      <td>\(14.2\)</td>
      <td>\(0.362\)</td>
      <td>\(32.4\%\)</td>
    </tr>
    <tr>
      <td></td>
      <td>\(1\text{ g}\)</td>
      <td>High Fan</td>
      <td>\(0.150\)</td>
      <td>\(3.45 \times 10^{-3}\)</td>
      <td>\(3.18\)</td>
      <td>\(21.6\)</td>
      <td>\(0.551\)</td>
      <td>\(11.2\%\)</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>Low Fan</td>
      <td>\(0.065\)</td>
      <td>\(0.68 \times 10^{-3}\)</td>
      <td>\(7.95\)</td>
      <td>\(8.6\)</td>
      <td>\(0.219\)</td>
      <td>\(52.8\%\)</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>High Fan</td>
      <td>\(0.150\)</td>
      <td>\(3.02 \times 10^{-3}\)</td>
      <td>\(3.40\)</td>
      <td>\(20.2\)</td>
      <td>\(0.515\)</td>
      <td>\(15.4\%\)</td>
    </tr>
    <tr>
      <td><b>APH</b></td>
      <td>\(1\text{ g}\)</td>
      <td>Nominal (\(0.6\text{ m/s}\))</td>
      <td>\(0.600\)</td>
      <td>\(1.24 \times 10^{-2}\)</td>
      <td>\(1.58\)</td>
      <td>\(43.2\)</td>
      <td>\(1.102\)</td>
      <td>\(2.1\%\)</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>Nominal (\(0.6\text{ m/s}\))</td>
      <td>\(0.600\)</td>
      <td>\(1.19 \times 10^{-2}\)</td>
      <td>\(1.63\)</td>
      <td>\(42.0\)</td>
      <td>\(1.071\)</td>
      <td>\(2.6\%\)</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>High (\(1.5\text{ m/s}\))</td>
      <td>\(1.500\)</td>
      <td>\(3.65 \times 10^{-2}\)</td>
      <td>\(0.98\)</td>
      <td>\(68.4\)</td>
      <td>\(1.745\)</td>
      <td>\(0.4\%\)</td>
    </tr>
  </tbody>
</table>

<div class="figure-box">
  <img src="file://__FIG4__" alt="Figure 4">
  <div class="figure-caption">
    <span class="fig-num">Figure 4 | Scalar ventilation dynamics, Local Mean Age of Air (LMA), and canopy dead zone mapping.</span>
    <b>a</b>, Cumulative distribution functions (CDF) of local air age normalized by residence time (\(\tau / \tau_0\)). <b>b</b>, Air exchange efficiency (\(\varepsilon_a\)). <b>c</b>, Mean canopy age (\(\overline{\tau}_{canopy}\)) vs. nominal residence time (\(\tau_0\)). <b>d</b>, Volumetric recirculation/trapped fraction. <b>e</b>, Predicted steady-state \(CO_2\) depletion within vegetative canopy.
  </div>
</div>

<h3 class="subsection-title">Scalar Residence Time, Age of Air, and Bioaerosol Biosecurity</h3>
<p>
  Local Mean Age of Air (\(\tau\)) and Air Exchange Efficiency (\(\varepsilon_a = \tau_0 / (2 \overline{\tau}_{canopy}) \times 100\%\)) reveal that APH achieves near-ideal displacement ventilation (\(\varepsilon_a \approx 45\%\)) with negligible trapped volume (\(<8.5\%\)), holding local canopy \(CO_2\) drawdown below \(24\text{ ppm}\) (Figure 4).
</p>
<p>
  The bioaerosol clearance curves (Figure 5) demonstrate a profound biosecurity contrast: VEGGIE exports \(100\%\) of airborne fungal spores directly into the crew living modules (\(t_{50} = 13.8\text{ s}\) on High Fan), maximizing astronaut allergen and pathogen exposure. In contrast, APH recirculates air internally through high-efficiency particulate air (HEPA) filters, achieving fast spore scrubbing (\(t_{50} = 18.4\text{ s}\)) while maintaining zero cabin burden (Table 4).
</p>

<div class="table-caption">
  <span class="tab-num">Table 4 |</span> Ventilation efficiency, local age of air, and biosecurity containment dynamics.
</div>
<table>
  <thead>
    <tr>
      <th>Chamber</th>
      <th>Gravity</th>
      <th>Flow Rate (\(Q\))</th>
      <th>\(\tau_0\text{ (s)}\)</th>
      <th>\(\overline{\tau}_{canopy}\text{ (s)}\)</th>
      <th>\(\varepsilon_a\text{ (\%)}\)</th>
      <th>\(t_{50}\text{ (s)}\)</th>
      <th>Biosecurity \& Aerosol Fate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Microgreen</b></td>
      <td>\(1\text{ g}\)</td>
      <td>\(11.8\text{ m}^3/\text{h}\)</td>
      <td>\(0.71\)</td>
      <td>\(6.85\)</td>
      <td>\(10.4\%\)</td>
      <td>\(14.2\)</td>
      <td>Sealed unit: zero cabin export; corner recirculation</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>\(11.8\text{ m}^3/\text{h}\)</td>
      <td>\(0.71\)</td>
      <td>\(5.20\)</td>
      <td>\(13.7\%\)</td>
      <td>\(11.5\)</td>
      <td>Unstratified jet improves canopy clearance</td>
    </tr>
    <tr>
      <td><b>VEGGIE</b></td>
      <td>\(1\text{ g}\)</td>
      <td>Low (\(42.5\text{ m}^3/\text{h}\))</td>
      <td>\(3.19\)</td>
      <td>\(14.20\)</td>
      <td>\(22.5\%\)</td>
      <td>\(28.6\)</td>
      <td>Direct cabin exhaust: \(100\%\) spore export to ISS</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>Low (\(42.5\text{ m}^3/\text{h}\))</td>
      <td>\(3.19\)</td>
      <td>\(22.40\)</td>
      <td>\(14.2\%\)</td>
      <td>\(45.2\)</td>
      <td>Critical mold risk (\(53\%\) stagnant volume)</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>High (\(85.0\text{ m}^3/\text{h}\))</td>
      <td>\(1.60\)</td>
      <td>\(6.10\)</td>
      <td>\(26.2\%\)</td>
      <td>\(13.8\)</td>
      <td>High fan restores boundary layer stripping</td>
    </tr>
    <tr>
      <td><b>APH</b></td>
      <td>\(1\text{ g}\)</td>
      <td>Nom (\(26.4\text{ m}^3/\text{h}\))</td>
      <td>\(11.35\)</td>
      <td>\(24.80\)</td>
      <td>\(45.8\%\)</td>
      <td>\(18.4\)</td>
      <td>Closed loop: internal HEPA filtration (\(\le25\text{ ppb}\))</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>Nom (\(26.4\text{ m}^3/\text{h}\))</td>
      <td>\(11.35\)</td>
      <td>\(25.20\)</td>
      <td>\(45.0\%\)</td>
      <td>\(18.9\)</td>
      <td>Piston sweep maintains \(45\%\) efficiency</td>
    </tr>
    <tr>
      <td></td>
      <td>\(0\text{ g}\)</td>
      <td>High (\(66.0\text{ m}^3/\text{h}\))</td>
      <td>\(4.54\)</td>
      <td>\(9.60\)</td>
      <td>\(47.3\%\)</td>
      <td>\(7.2\)</td>
      <td>Near-ideal displacement flow (\(\varepsilon_a \to 50\%\))</td>
    </tr>
  </tbody>
</table>

<div class="figure-box">
  <img src="file://__FIG5__" alt="Figure 5">
  <div class="figure-caption">
    <span class="fig-num">Figure 5 | Habitat biosecurity, bioaerosol clearance, and crew exposure trade space.</span>
    <b>a</b>, Transient bioaerosol clearance curves (\(C(t)/C_0\)) following spore release. <b>b</b>, Habitat biosecurity quadrant map: cabin export percentage vs. canopy clearance velocity metric (\(k_{clear} = 1/t_{50}\)). <b>c</b>, Aerosol particle fate: surface deposition vs. exhaust filtration. <b>d</b>, Two-dimensional architectural design matrix for spaceflight plant enclosures.
  </div>
</div>

<h2 class="section-title">Discussion</h2>
<p>
  Our findings demonstrate that spaceflight plant hardware design must transition from empirical terrestrial heuristics to rigorous microgravity fluid dynamics. Specifically, the "stratification paradox" indicates that closed ducted chambers can achieve superior turbulence and boundary-layer stripping in microgravity relative to Earth controls. For future Lunar and Martian surface BLSS facilities, we recommend: (1) adopting dual opposing lower lateral supply diffusers to ensure \(\varepsilon_a > 45\%\), (2) decoupling bulk air exchange (\(\text{ACH} \sim 100 - 300\text{ h}^{-1}\)) from canopy shear velocity (\(U \sim 0.3 - 0.6\text{ m/s}\)), and (3) integrating localized HEPA filtration to safeguard crew habitat air quality.
</p>

<h2 class="section-title">Methods</h2>
<p>
  Simulations utilized OpenFOAM v2606 with compressible Navier-Stokes and Low-Mach approximations. Turbulence was modeled using the \(k\text{-}\omega\text{ SST}\) RAS formulation with prism boundary layers (\(y^+ \sim 1 - 5\)). Geometric surfaces were synthesized via analytic Python generators with 0 open/duplicate edges. Three-level mesh convergence ladders (\(m0/m1/m2\)) confirmed grid independence within \(<1.3\%\) error.
</p>

<h2 class="section-title">References</h2>
<div class="references">
  <ol>
    <li>Massa, G. D. et al. VEG-01: Veggie hardware validation testing on the International Space Station. <i>Open Agric.</i> <b>2</b>, 33–41 (2017).</li>
    <li>Morrow, R. C. et al. A new plant habitat facility for the ISS. <i>46th ICES</i>, ICES-2016-320 (2016).</li>
    <li>Monje, O. et al. Hardware validation of the Advanced Plant Habitat on ISS. <i>49th ICES</i>, ICES-2019-247 (2019).</li>
    <li>Wheeler, R. M. Agriculture for space: People and places paving the way. <i>Open Agric.</i> <b>2</b>, 14–32 (2017).</li>
    <li>Kitaya, Y. et al. Effects of air current on transpiration and net photosynthetic rates of plants in a closed plant growth chamber under microgravity. <i>Adv. Space Res.</i> <b>31</b>, 177–182 (2003).</li>
    <li>Kitaya, Y. et al. Gas exchange and temperature gradients of plant leaves under microgravity conditions. <i>Adv. Space Res.</i> <b>28</b>, 565–570 (2001).</li>
    <li>Porterfield, D. M. The biophysical limitations in physiological transport and exchange in plants growing in microgravity. <i>Physiol. Plant.</i> <b>114</b>, 333–340 (2002).</li>
    <li>Musgrave, M. E. et al. Gravity independence of seed-to-seed cycling in <i>Brassica rapa</i>. <i>Planta</i> <b>203</b>, S110–S119 (1997).</li>
    <li>Paul, A.-L. & Ferl, R. J. Epigenomics in spaceflight: epigenetic modifications under spaceflight stressors. <i>Front. Genet.</i> <b>8</b>, 139 (2017).</li>
    <li>Farquhar, G. D., von Caemmerer, S. & Berry, J. A. A biochemical model of photosynthetic CO2 assimilation in leaves of C3 species. <i>Planta</i> <b>149</b>, 78–90 (1980).</li>
    <li>Menter, F. R. Two-equation eddy-viscosity turbulence models for engineering applications. <i>AIAA J.</i> <b>32</b>, 1598–1605 (1994).</li>
    <li>Khodadad, C. L. M. et al. Microbiological and nutritional analysis of lettuce crops grown on the International Space Station. <i>Front. Plant Sci.</i> <b>11</b>, 199 (2020).</li>
    <li>Urbaniak, C. et al. Microbiomes of the International Space Station and comparison with other human-built environments. <i>Microbiome</i> <b>6</b>, 1–18 (2018).</li>
    <li>Zabel, P. et al. The EDEN ISS greenhouse for space research—Design overview and test results. <i>Acta Astronaut.</i> <b>128</b>, 344–358 (2016).</li>
    <li>Poulet, L. et al. Significant energy savings for indoor plant growth using targeted LED lighting. <i>HortScience</i> <b>49</b>, 1455–1463 (2016).</li>
    <li>Jasinski, P., Norton, T. & Sun, D. W. Computational fluid dynamics in controlled environment agriculture: A review. <i>Comput. Electron. Agric.</i> <b>49</b>, 201–221 (2005).</li>
    <li>Ewald, H. & Barker, R. Microgreen Chamber CFD: 3D Internal-Flow and Gravity Parametric Analysis in OpenFOAM (2026).</li>
  </ol>
</div>

</body>
</html>
"""
    # Replace image path placeholders
    html_rendered = html_template.replace("__FIG1__", fig1)
    html_rendered = html_rendered.replace("__FIG2__", fig2)
    html_rendered = html_rendered.replace("__FIG3__", fig3)
    html_rendered = html_rendered.replace("__FIG4__", fig4)
    html_rendered = html_rendered.replace("__FIG5__", fig5)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_rendered)
    print(f"Wrote HTML template to: {html_path}")

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(root, "npj_manuscript.html")
    pdf_file = os.path.join(root, "npj_manuscript.pdf")

    build_html_manuscript(html_file)

    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if not os.path.isfile(chrome_bin):
        print(f"Chrome binary not found at {chrome_bin}")
        sys.exit(1)

    user_data_dir = os.path.join(root, ".chrome_user_data")
    os.makedirs(user_data_dir, exist_ok=True)

    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--user-data-dir={user_data_dir}",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={pdf_file}",
        "--no-pdf-header-footer",
        html_file
    ]

    print(f"Compiling publication PDF with headless Chromium...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and os.path.isfile(pdf_file):
        size_kb = os.path.getsize(pdf_file) / 1024.0
        print(f"Successfully compiled: {pdf_file} ({size_kb:.1f} KB)")
    else:
        print(f"Error during PDF compilation: {res.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
