---
name: thermodynamics
description: "Thermodynamic cycles (Rankine, Brayton, Otto, Diesel), refrigeration, psychrometrics, and exergy destruction analysis"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/thermodynamics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Mechanical Thermodynamics

## Scope
Mechanical thermodynamics evaluates energy transformation, heat-work conversion efficiency, thermal power plant cycles, internal combustion cycles, and HVAC psychrometrics.

## Power Cycles & Formulations
- **Rankine Cycle (Steam Power)**:
  - Thermal efficiency: $\eta_{\text{th}} = \frac{w_{\text{net}}}{q_{\text{in}}} = \frac{(h_3 - h_4) - (h_2 - h_1)}{h_3 - h_2}$.
  - Reheat and regeneration to increase mean heat addition temperature.
- **Brayton Cycle (Gas Turbines)**:
  - Ideal efficiency: $\eta = 1 - \frac{1}{r_p^{(\gamma - 1)/\gamma}}$, where $r_p = P_2 / P_1$.
- **Otto (Gasoline) & Diesel Cycles**: Compression ratio $r = V_{\max}/V_{\min}$, cutoff ratio $r_c$.
- **Exergy Analysis**: Exergy destruction $X_{\text{destroyed}} = T_0 S_{\text{gen}}$.

## Tools & Standards
- **Software**: REFPROP, CoolProp, EES (Engineering Equation Solver).
- **Canonical References**: Moran, Shapiro et al. — *Fundamentals of Engineering Thermodynamics*.
