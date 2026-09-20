---
name: cfd
description: "Computational fluid dynamics: FVM discretization, RANS turbulence models (k-epsilon, k-omega SST), boundary conditions, and y+ sizing"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/cfd/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Computational Fluid Dynamics (CFD)

## Scope
CFD models fluid flows, aerodynamic forces, mixing, and thermal convection using numerical finite volume discretization of the Navier-Stokes equations.

## Numerical Formulations & Best Practices
- **Finite Volume Method (FVM)**: Integral conservation equations discretized over control volumes:
  $$\frac{\partial}{\partial t}\int_V \rho \phi dV + \oint_A \rho \phi \mathbf{v} \cdot d\mathbf{A} = \oint_A \Gamma_\phi \nabla \phi \cdot d\mathbf{A} + \int_V S_\phi dV$$
- **Turbulence Modeling (RANS)**:
  - $k-\epsilon$: Superior for free-stream, high Reynolds number bulk flow.
  - $k-\omega\text{ SST}$ (Menter): Blends $k-\omega$ near walls with $k-\epsilon$ in far field; optimal for adverse pressure gradients and separation.
- **Near-Wall Resolution ($y^+$)**:
  $$y^+ = \frac{u_\tau y}{\nu}, \quad u_\tau = \sqrt{\frac{\tau_w}{\rho}}$$
  For resolving viscous sublayer without wall functions: $y^+ < 1$; for wall functions: $30 < y^+ < 300$.

## Tools & Standards
- **Software**: OpenFOAM, ANSYS Fluent, Siemens STAR-CCM+.
- **Canonical References**: Versteeg & Malalasekera — *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*.
