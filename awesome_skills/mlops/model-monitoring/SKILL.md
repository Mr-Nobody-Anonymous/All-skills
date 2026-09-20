---
name: model-monitoring
description: "Monitoring ML in production: data drift (KS test, PSI), concept drift, prediction drift, latency p99, and automated retraining triggers"
category: mlops
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mlops/model-monitoring/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# ML Model Monitoring & Drift Detection

## Scope
Production ML monitoring detects degradation in model performance, input data distribution shifts (data drift), and changes in ground-truth relationships (concept drift).

## Drift Detection Statistical Tests
- **Population Stability Index (PSI)**:
  $$\text{PSI} = \sum_{i=1}^k (B_i - T_i) \ln\left(\frac{B_i}{T_i}\right)$$
  where $B_i$ is baseline population fraction, $T_i$ target production fraction ($\text{PSI} < 0.1$ stable, $\text{PSI} > 0.25$ significant shift).
- **Kolmogorov-Smirnov (KS) Test**: Non-parametric test comparing continuous feature cumulative distribution functions; drift flagged if $p < 0.05$.
- **Operational Metrics**: Latency percentiles (p50, p95, p99), error rates, throughput (QPS).

## Tools & Platforms
- **Software**: Evidently AI, Whylabs, Arize AI, Prometheus + Grafana.
