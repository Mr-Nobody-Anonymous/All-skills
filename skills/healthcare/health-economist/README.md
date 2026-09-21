# Health Economist Agent Skill

A comprehensive decision-analytic and econometric evaluation skill for AI agents conducting Health Technology Assessments (HTA), Cost-Effectiveness Analyses (CEA), and Cost-Utility Analyses (CUA).

## Core Capabilities
- **ICER Computation & Quadrant Mapping**: Computes incremental costs, incremental QALYs/DALYs, and evaluates against regional WTP thresholds.
- **Decision-Tree & Markov State Modelling**: Formulates multi-state disease progression cohorts with cycle-specific transition probability matrices.
- **Sensitivity Analysis Guidance**: Formulates deterministic one-way tornado bounds and Monte Carlo probabilistic sensitivity analysis (PSA).
- **CHEERS 2022 Compliance**: Formats evaluations according to Consolidated Health Economic Evaluation Reporting Standards.

## Quick Start
Tell your AI assistant:
> "Perform a cost-effectiveness analysis comparing SGLT2 inhibitors vs standard care in chronic kidney disease from an NHS perspective with a lifetime horizon and 3.5% discount rate."

## Directory Layout
- `SKILL.md`: Main playbook for agent execution directives.
- `references/`: Methodological guides on ICER calculations, QALY/DALY math, and CHEERS guidelines.
- `examples/`: Complete CEA report examples and anti-pattern breakdowns.
- `tests/`: Structural and evaluation tests.
