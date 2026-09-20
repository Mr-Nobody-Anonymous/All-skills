---
name: psychometrics
description: "Psychological measurement: test construction, reliability, validity, item response theory, factor analysis, and assessment"
category: psychology
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/psychology/psychometrics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Psychometrics

## Scope
Psychometrics is the science of psychological measurement. This skill covers test construction, reliability, validity, classical test theory, item response theory, and factor analysis.

## Classical Test Theory (CTT)

### Core Equation
X = T + E (Observed score = True score + Error)

### Reliability
Reliability = proportion of variance due to true scores: r = σ²_T / σ²_X

| Method | What it Measures | Formula/Approach |
|--------|-----------------|------------------|
| Test-retest | Stability over time | Correlate two administrations |
| Parallel forms | Equivalence of forms | Correlate alternate forms |
| Internal consistency | Item homogeneity | Cronbach's α = (k/(k-1))(1 - Σσ²ᵢ/σ²_total) |
| Split-half | Internal consistency | Spearman-Brown: r = 2r_half/(1 + r_half) |
| Inter-rater | Agreement between raters | Cohen's κ, ICC |

- **Acceptable α**: ≥ 0.70 for research, ≥ 0.90 for individual decisions
- **Standard error of measurement**: SEM = σ_X√(1 - r)

### Validity
| Type | Question | Methods |
|------|----------|---------|
| Content | Does the test cover the domain? | Expert judgment, blueprint alignment |
| Criterion | Does the test predict outcomes? | Predictive/concurrent correlation |
| Construct | Does the test measure the intended construct? | Factor analysis, convergent/discriminant, MTMM |

## Item Response Theory (IRT)

### Models
- **1PL (Rasch)**: P(θ) = 1/[1 + exp(-(θ - b))] — only difficulty parameter b
- **2PL**: P(θ) = 1/[1 + exp(-a(θ - b))] — adds discrimination a
- **3PL**: P(θ) = c + (1-c)/[1 + exp(-a(θ - b))] — adds guessing c

### Key Concepts
- **Item characteristic curve (ICC)**: S-shaped probability function
- **Information function**: I(θ) = [P'(θ)]²/[P(θ)(1-P(θ))] — precision at each ability level
- **Test information**: Sum of item information functions; SE(θ) = 1/√I(θ)
- **Differential item functioning (DIF)**: Item performs differently across groups at same ability level

### Advantages over CTT
- Person parameters independent of item sample (within model)
- Item parameters independent of person sample
- Precision varies by ability level (targeted measurement)

## Factor Analysis

### Exploratory (EFA)
1. Assess factorability (KMO ≥ 0.60, Bartlett's test significant)
2. Determine number of factors (parallel analysis, scree plot, eigenvalue > 1)
3. Extract factors (principal axis factoring, maximum likelihood)
4. Rotate (orthogonal: varimax; oblique: promax, oblimin)
5. Interpret and name factors based on high-loading items

### Confirmatory (CFA)
- Specify hypothesized factor structure a priori
- Fit indices: χ²/df < 3, RMSEA < 0.06, CFI > 0.95, SRMR < 0.08
- Compare competing models with Δχ², AIC/BIC

## Test Construction Pipeline
1. Define construct → literature review → operational definition
2. Write items → expert review → cognitive interviews
3. Pilot test → item analysis (difficulty, discrimination, distractors)
4. Factor analysis → reliability analysis → validity evidence
5. Norming → standard scores → percentiles → cut scores

## Computational Tools
- **R**: `psych`, `mirt`, `lavaan`, `ltm` packages
- **Python**: `factor_analyzer`, `pyirt`
- **Mplus**: SEM and IRT software
- **SPSS**: Factor analysis, reliability analysis
- **Winsteps/ConQuest**: Rasch/IRT analysis

## Standards
- AERA/APA/NCME — *Standards for Educational and Psychological Testing*
- ITC Guidelines on Test Use, Adaptation, and Computer-Based Testing

## References
- Furr — *Psychometrics: An Introduction*
- Embretson & Reise — *Item Response Theory for Psychologists*
- Brown — *Confirmatory Factor Analysis*
