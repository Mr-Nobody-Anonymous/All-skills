---
name: model-registry
description: "Centralized model registry: versioning, staging/production stage transitions, model signing, and metadata governance"
category: mlops
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mlops/model-registry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Model Registry & Governance

## Scope
A model registry provides a centralized repository for managing the full lifecycle of machine learning models from training completion through production retirement.

## Registry Lifecycle Stages
- **Model Versioning**: Semantic versioning ($1.0.0$) associated with source experiment run ID and dataset lineage.
- **Stage Transitions**: Development $\to$ Staging (automated integration test validation) $\to$ Production (serving live inference) $\to$ Archived.
- **Artifact Governance**: Cryptographic model checksums, model signatures, dependencies, and Model Cards detailing intended use cases and benchmarked accuracy.

## Tools & Platforms
- **Software**: MLflow Model Registry, AWS SageMaker Model Registry, Seldon.
