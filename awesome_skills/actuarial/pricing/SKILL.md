---
name: pricing
description: "Fit Poisson frequency and Gamma severity GLMs with log link functions to establish multi-variable multiplicative tariff rating structures."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - pricing
  - glm
  - frequency-severity
---

# Generalized Linear Models (GLM) for Insurance Rating

## Overview & Core Principles
Fit Poisson frequency and Gamma severity GLMs with log link functions to establish multi-variable multiplicative tariff rating structures.

### Multiplicative Tariff Model
$$\ln(E[Y]) = \beta_0 + \sum_j \beta_j X_j$$
- Frequency model: Poisson with exposure offset $\ln(\text{exposure})$.
- Severity model: Gamma with log link on non-zero claims.
