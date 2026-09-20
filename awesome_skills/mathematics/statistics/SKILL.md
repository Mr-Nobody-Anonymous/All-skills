---
name: statistics
description: "Hypothesis testing, maximum likelihood estimation, confidence intervals, regression, Bayesian inference, and non-parametrics"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/statistics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Statistics

## Scope
Statistics is the mathematical science of collecting, analyzing, interpreting, and presenting data, providing rigorous inferential decision frameworks.

## Core Statistical Frameworks
- **Maximum Likelihood Estimation (MLE)**: $\hat{\theta}_{\text{MLE}} = \arg\max_\theta \sum_{i=1}^n \ln f(x_i | \theta)$.
- **Hypothesis Testing (Neyman-Pearson)**: Type I error ($\alpha$, false positive), Type II error ($\beta$, false negative), Power ($1 - \beta$).
- **Linear Models (OLS)**: $\hat{\beta} = (X^T X)^{-1} X^T y$, Gauss-Markov theorem (BLUE).
- **Bayesian Inference**: Posterior $p(\theta | D) \propto p(D | \theta) p(\theta)$, Markov Chain Monte Carlo (MCMC).

## Tools & References
- **Software**: R, Python (`scipy.stats`, `statsmodels`), Stan.
- **Canonical References**: Casella & Berger — *Statistical Inference*; Wasserman — *All of Statistics*.
