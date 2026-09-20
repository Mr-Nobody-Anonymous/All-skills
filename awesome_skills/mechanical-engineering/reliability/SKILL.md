---
name: reliability
description: "Weibull distribution, MTTF/MTBF, failure modes and effects analysis (FMEA), fault tree analysis (FTA), and reliability block diagrams"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/reliability/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Reliability Engineering

## Scope
Reliability engineering mathematically models system failure rates, evaluates component lifetimes, and designs fault-tolerant, fail-safe mechanical and electronic systems.

## Core Statistical Models
- **Weibull Distribution**:
  $$R(t) = \exp\left(-\left(\frac{t}{\eta}\right)^\beta\right)$$
  where $\beta$ is shape parameter ($\beta < 1$ infant mortality, $\beta = 1$ constant random failure rate $\lambda = 1/\eta$, $\beta > 1$ wear-out failure), $\eta$ scale parameter (characteristic life).
- **Mean Time Between Failures (MTBF)**: For constant failure rate $\lambda$: $\text{MTBF} = 1 / \lambda$.
- **FMEA / FMECA**: Risk Priority Number $\text{RPN} = \text{Severity} (S) \times \text{Occurrence} (O) \times \text{Detection} (D)$ (each rated 1-10).
- **Reliability Block Diagrams (RBD)**:
  - Series: $R_{\text{sys}} = \prod R_i$.
  - Parallel (redundant): $R_{\text{sys}} = 1 - \prod (1 - R_i)$.

## Tools & Standards
- **Standards**: MIL-HDBK-217F, IEC 60812 (FMEA), IEEE 493.
- **Software**: ReliaSoft (Weibull++, BlockSim), Isograph.
- **Canonical References**: O'Connor & Kleyner — *Practical Reliability Engineering*.
