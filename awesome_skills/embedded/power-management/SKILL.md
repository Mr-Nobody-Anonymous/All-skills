---
name: power-management
description: "Low-power embedded design: sleep modes, dynamic voltage and frequency scaling (DVFS), power gating, battery life estimation, and energy harvesting"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/power-management/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Embedded Low-Power Management

## Scope
Low-power engineering optimizes energy consumption in battery-operated and energy-harvesting embedded nodes through sleep states, clock gating, and hardware power domains.

## Power Optimization Techniques
- **Dynamic Power Dissipation**: $P_{\text{dyn}} = C V_{DD}^2 f \cdot \alpha$ (where $C$ is capacitance, $V_{DD}$ supply voltage, $f$ clock frequency, $\alpha$ switching activity factor).
- **Dynamic Voltage & Frequency Scaling (DVFS)**: Lowering frequency allows lowering core voltage, yielding cubic power reduction.
- **Sleep Mode Duty Cycling**:
  $$\bar{I} = \frac{I_{\text{active}} t_{\text{active}} + I_{\text{sleep}} t_{\text{sleep}}}{t_{\text{active}} + t_{\text{sleep}}}$$
  Battery Life: $T = \frac{\text{Battery Capacity (mAh)}}{\bar{I} (\text{mA})}$.
- **Hardware Power Gating**: Using P-channel MOSFET load switches to completely disconnect power from quiescent external sensors and transceivers.

## Tools & Standards
- **Hardware**: Otii Arc (power profiling), Nordic Power Profiler Kit (PPK2).
