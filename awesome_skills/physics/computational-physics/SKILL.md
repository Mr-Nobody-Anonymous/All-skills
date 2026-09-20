---
name: computational-physics
description: "Numerical methods for physics: Monte Carlo, molecular dynamics, finite element/difference methods, and scientific computing"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/computational-physics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Computational Physics

## Scope
Computational physics uses numerical algorithms and computer simulations to solve physical problems that are analytically intractable. This skill covers core numerical methods, simulation paradigms, and best practices for scientific computing.

## Core Numerical Methods

### Ordinary Differential Equations (ODEs)
- **Euler method**: yₙ₊₁ = yₙ + h·f(tₙ, yₙ) — O(h), unstable for stiff problems
- **RK4 (Runge-Kutta 4th order)**: O(h⁴), standard workhorse
  - k₁ = f(t, y), k₂ = f(t+h/2, y+hk₁/2), k₃ = f(t+h/2, y+hk₂/2), k₄ = f(t+h, y+hk₃)
  - yₙ₊₁ = yₙ + (h/6)(k₁ + 2k₂ + 2k₃ + k₄)
- **Adaptive step**: Embedded RK pairs (Dormand-Prince), error control via tolerance
- **Symplectic integrators**: Velocity Verlet, leapfrog — conserve energy in Hamiltonian systems

### Partial Differential Equations (PDEs)
- **Finite Difference (FDM)**: Discretize derivatives on a grid. Central difference: f''(x) ≈ (f(x+h) - 2f(x) + f(x-h))/h²
- **Finite Element (FEM)**: Weak form, basis functions, mesh. Best for complex geometries
- **Spectral methods**: Expand in orthogonal functions (Fourier, Chebyshev). Exponential convergence for smooth solutions
- **Stability**: CFL condition Δt ≤ Δx/c for explicit methods

### Linear Algebra
- **Direct**: LU decomposition, Cholesky (symmetric positive definite), QR
- **Iterative**: Conjugate gradient (SPD), GMRES (general), multigrid (hierarchical)
- **Eigenvalue problems**: Lanczos (symmetric), Arnoldi (general), power iteration

### Monte Carlo Methods
- **Random sampling**: Estimate integrals by averaging f(x) over random points
- **Markov Chain Monte Carlo (MCMC)**: Metropolis-Hastings, Gibbs sampling — sample from complex distributions
- **Importance sampling**: Reduce variance by sampling from a distribution close to the target
- **Monte Carlo integration error**: ∝ 1/√N (independent of dimension)

## Simulation Paradigms

### Molecular Dynamics (MD)
- Integrate Newton's equations for N particles with pairwise potentials
- **Force fields**: Lennard-Jones, Coulomb, bonded interactions (AMBER, OPLS)
- **Thermostats**: Nosé-Hoover, Berendsen, Langevin
- **Barostats**: Parrinello-Rahman, Berendsen
- **Time step**: ~ 1-2 fs for atomic systems

### N-body Simulations
- **Direct summation**: O(N²) — only for N < 10⁴
- **Barnes-Hut tree**: O(N log N) — multipole expansion with tree structure
- **Particle-Mesh**: O(N log N) — FFT-based long-range force calculation

### Lattice Models
- **Ising model**: Monte Carlo with Metropolis algorithm, measure ⟨M⟩, ⟨E⟩, χ, Cᵥ
- **Lattice QCD**: Path integral on discretized spacetime

## Best Practices
1. **Validation**: Compare with known analytical solutions
2. **Convergence**: Verify results converge with decreasing step size / mesh refinement
3. **Conservation**: Check conserved quantities (energy, momentum, charge)
4. **Reproducibility**: Set random seeds, document parameters, version-control code

## Tools & Libraries
- **Python**: NumPy, SciPy, Matplotlib, Numba (JIT compilation)
- **Fortran/C++**: Still dominant for HPC physics codes
- **Julia**: Modern language combining Python ease with C speed
- **HPC**: MPI (distributed memory), OpenMP (shared memory), CUDA/OpenCL (GPU)
- **Visualization**: ParaView, VisIt, Mayavi

## Standards & References
- Newman — *Computational Physics* (Python-based)
- Thijssen — *Computational Physics*
- Press et al. — *Numerical Recipes*
