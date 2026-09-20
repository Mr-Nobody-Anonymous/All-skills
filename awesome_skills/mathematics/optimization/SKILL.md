---
name: optimization
description: "Linear programming, convex optimization, KKT conditions, gradient descent, quasi-Newton (BFGS), and non-linear programming"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/optimization/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Optimization

## Scope
Mathematical optimization finds the best element from a set of available alternatives with respect to defined criteria, covering linear, convex, and non-convex regimes.

## Core Formulations
- **Convex Optimization**: Minimize $f_0(x)$ subject to $f_i(x) \le 0$, $h_i(x) = a_i^T x - b_i = 0$, where $f_0, \dots, f_m$ are convex. Local minimum is global minimum.
- **Karush-Kuhn-Tucker (KKT) Conditions**:
  - Stationarity: $\nabla f_0(x^*) + \sum \lambda_i^* \nabla f_i(x^*) + \sum \nu_i^* a_i = 0$
  - Primal feasibility: $f_i(x^*) \le 0, h_i(x^*) = 0$
  - Dual feasibility: $\lambda_i^* \ge 0$
  - Complementary slackness: $\lambda_i^* f_i(x^*) = 0$
- **Algorithms**: Simplex, Interior Point, Gradient Descent, L-BFGS, Nelder-Mead.

## Tools & References
- **Software**: CVXPY, Gurobi, SciPy (`scipy.optimize`), MOSEK.
- **Canonical References**: Boyd & Vandenberghe — *Convex Optimization*; Nocedal & Wright — *Numerical Optimization*.
