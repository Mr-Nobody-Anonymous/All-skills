---
name: computational-chemistry
description: "Density functional theory (DFT), ab initio methods, molecular mechanics, molecular dynamics, and conformational search"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/computational-chemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Computational Chemistry

## Scope
Computational chemistry applies numerical algorithms, quantum mechanics, and classical physics to simulate chemical structures, molecular dynamics, and reaction energetics.

## Methodological Hierarchy

### 1. Quantum Chemical Methods
| Method | Scaling | Accuracy / Application |
|---|---|---|
| **Hartree-Fock (HF)** | $O(N^4)$ | Baseline mean-field theory; neglects electron correlation. |
| **Density Functional Theory (DFT)** | $O(N^3) - O(N^4)$ | Modern standard for electronic structure; functionals: B3LYP, PBE0, $\omega$B97X-D (with dispersion). |
| **Møller-Plesset Perturbation (MP2)** | $O(N^5)$ | Captures dynamic electron correlation. |
| **Coupled Cluster (CCSD(T))** | $O(N^7)$ | "Gold standard" for small-to-medium molecules ($<30$ atoms). |

### 2. Basis Sets
- Pople style: $6-31G(d,p)$, $6-311+G(2df,2p)$ (split-valence, polarization, diffuse functions).
- Dunning correlation-consistent: $cc-pVDZ, cc-pVTZ, aug-cc-pVTZ$.
- Def2 series: $def2-SVP, def2-TZVP$ (balanced accuracy and efficiency).

### 3. Molecular Mechanics & Molecular Dynamics (MD)
- **Force Field Potential**:
  $$V = \sum_{\text{bonds}} k_b(r - r_0)^2 + \sum_{\text{angles}} k_\theta(\theta - \theta_0)^2 + \sum_{\text{torsions}} V_n[1 + \cos(n\phi - \gamma)] + \sum_{i < j}\left[\frac{q_i q_j}{4\pi\varepsilon_0 r_{ij}} + 4\epsilon\left(\left(\frac{\sigma}{r_{ij}}\right)^{12} - \left(\frac{\sigma}{r_{ij}}\right)^6\right)\right]$$
- Standard packages: AMBER, CHARMM, GROMACS, OPLS-AA.

## Tools & Standards
- **Software**: Gaussian, ORCA, Q-Chem, VASP, PSI4, GROMACS, LAMMPS.
- **Canonical References**: Cramer — *Essentials of Computational Chemistry*; Jensen — *Introduction to Computational Chemistry*.
