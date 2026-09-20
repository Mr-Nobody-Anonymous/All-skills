---
name: robotics
description: "Forward/inverse kinematics (DH parameters), robot dynamics (Newton-Euler), trajectory generation, ROS2, and motion planning"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/robotics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Robotics & Kinematics

## Scope
Robotics designs and controls articulated manipulators, mobile platforms, and autonomous robots using spatial kinematics, multi-body dynamics, and trajectory generation.

## Kinematic & Dynamic Frameworks
- **Denavit-Hartenberg (DH) Parameters**: 4-parameter convention ($d, \theta, a, \alpha$) for homogenous transform $T_{i-1}^i$:
  $$T_{i-1}^i = \operatorname{Rot}_z(\theta_i) \operatorname{Trans}_z(d_i) \operatorname{Trans}_x(a_i) \operatorname{Rot}_x(\alpha_i)$$
- **Robot Jacobian**: Relates joint velocities to end-effector spatial velocities: $\mathbf{v} = \mathbf{J}(\mathbf{q}) \mathbf{\dot{q}}$.
  - Singularities occur when $\det(\mathbf{J}) = 0$ (loss of degree of freedom).
- **Inverse Kinematics**: Closed-form (Pieper's criterion: 3 consecutive intersecting revolute axes) vs. numerical (damped least squares / Levenberg-Marquardt).

## Tools & Standards
- **Software**: ROS / ROS2, Gazebo, MoveIt2, Pinocchio, MuJoCo.
- **Canonical References**: Craig — *Introduction to Robotics: Mechanics and Control*; Lynch & Park — *Modern Robotics*.
