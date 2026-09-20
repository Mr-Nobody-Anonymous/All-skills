---
name: spectroscopy
description: "NMR, IR, Raman, UV-Vis, fluorescence, structural elucidation, and spectral interpretation"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/spectroscopy/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Spectroscopy

## Scope
Spectroscopy analyzes the interaction between electromagnetic radiation and matter to identify chemical composition, molecular structure, dynamics, and concentration.

## Spectral Methodologies

### 1. Nuclear Magnetic Resonance (NMR)
- **Chemical Shift ($\delta$, ppm)**: $\delta = (\nu - \nu_{\text{TMS}}) / \nu_{\text{spectrometer}} \times 10^6$.
- **$^1H$-NMR Diagnostic Regions**:
  - Alkyl ($C-H$): 0.8 - 1.8 ppm
  - Alkynyl ($C\equiv C-H$): 2.0 - 3.0 ppm
  - Heteroatom ($C-H$ adjacent to $O, N, X$): 3.0 - 4.5 ppm
  - Vinylic ($C=C-H$): 4.5 - 6.5 ppm
  - Aromatic ($Ar-H$): 6.5 - 8.5 ppm
  - Aldehydic ($CHO$): 9.0 - 10.0 ppm
  - Carboxylic ($COOH$): 10.5 - 12.5 ppm
- **Spin-Spin Coupling ($J$, Hz)**: Pascal's triangle multiplicity ($n+1$ rule for $I=1/2$).
- **2D NMR**: COSY ($^1H-^1H$ coupling), HSQC ($^1H-^{13}C$ direct 1-bond correlation), HMBC ($^1H-^{13}C$ long-range 2-3 bond correlation).

### 2. Infrared (IR) & Raman Spectroscopy
- **Diagnostic IR Bands**:
  - $O-H / N-H$ stretch: $3200 - 3600\text{ cm}^{-1}$ (broad/sharp)
  - $C-H$ stretch: $2850 - 3100\text{ cm}^{-1}$ ($sp^3 < 3000 < sp^2$)
  - $C\equiv C, C\equiv N$: $2100 - 2260\text{ cm}^{-1}$
  - $C=O$ stretch: $1650 - 1780\text{ cm}^{-1}$ (esters, ketones, acids, amides)
  - Fingerprint region: $600 - 1400\text{ cm}^{-1}$
- **Raman Mutual Exclusion**: For centrosymmetric molecules, vibrations active in IR are inactive in Raman, and vice versa.

## Tools & Standards
- **Software**: MestReNova, TopSpin, Origin, SpecKit.
- **Canonical References**: Silverstein, Webster & Kiemle — *Spectrometric Identification of Organic Compounds*; Pavia et al. — *Introduction to Spectroscopy*.
