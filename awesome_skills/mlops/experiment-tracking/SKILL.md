---
name: experiment-tracking
description: "MLflow, Weights & Biases, hyperparameter logging, metric visualization, artifact tracking, and reproducible model runs"
category: mlops
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mlops/experiment-tracking/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# ML Experiment Tracking

## Scope
Experiment tracking systematically logs hyperparameters, dataset hashes, code commits, environment dependencies, and training evaluation metrics across machine learning runs.

## Core Invariants & Best Practices
- **Reproducibility Manifest**: Every experiment run must log: Git commit hash, Python environment (`pip freeze`), hardware specs, random seed, training configuration.
- **Metric Time-Series**: Continuous logging of training/validation loss, learning rate schedules, accuracy, and F1-score per epoch.
- **Artifact Versioning**: Logging trained model checkpoints, confusion matrices, ROC curves, and sample prediction tables.

## Tools & Platforms
- **Platforms**: MLflow, Weights & Biases (wandb), Neptune.ai, TensorBoard.
