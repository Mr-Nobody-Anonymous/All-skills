---
name: numerical-methods
description: "Root-finding, interpolation, numerical quadrature, linear solvers, eigenvalue algorithms, and error propagation"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/numerical-methods/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Numerical Methods

## Scope
Numerical methods designs and analyzes algorithms for solving mathematical problems with numerical approximations on digital computers, managing truncation and round-off errors.

## Core Algorithms
- **Root Finding**: Newton-Raphson $x_{n+1} = x_n - f(x_n)/f'(x_n)$ (quadratic convergence); Bisection (linear, guaranteed).
- **Linear System Solvers**: LU, Cholesky, QR, Conjugate Gradient, GMRES.
- **Numerical Quadrature**: Simpson's rule, Gauss-Legendre quadrature $\int_{-1}^1 f(x) dx \approx \sum w_i f(x_i)$.
- **Interpolation**: Lagrange polynomials, Chebyshev nodes (avoids Runge's phenomenon), cubic splines.

## Tools & References
- **Software**: NumPy, SciPy, MATLAB.
- **Canonical References**: Burden & Faires — *Numerical Analysis*; Trefethen & Bau — *Numerical Linear Algebra*.
