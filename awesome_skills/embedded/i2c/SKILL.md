---
name: i2c
description: "Inter-Integrated Circuit: open-drain architecture, pull-up resistor sizing, start/stop conditions, 7/10-bit addressing, and clock stretching"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/i2c/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# I2C Communication Protocol

## Scope
I2C two-wire serial bus engineering, open-drain hardware interfacing, pull-up resistor sizing, multi-master arbitration, and bus fault recovery.

## Electrical & Protocol Specification
- **Physical Lines**: SDA (Serial Data) and SCL (Serial Clock), both bidirectional open-drain requiring external pull-up resistors ($R_p$).
- **Pull-Up Resistor Sizing**:
  $$R_{p(\min)} = \frac{V_{DD} - V_{OL}}{I_{OL}}, \quad R_{p(\max)} = \frac{t_r}{0.8473 \cdot C_b}$$
  where $t_r$ is maximum allowable rise time ($1000\text{ ns}$ standard mode, $300\text{ ns}$ fast mode), $C_b$ bus capacitance (limit $400\text{ pF}$).
- **Bus Framing**:
  - START: SDA pulled low while SCL high.
  - STOP: SDA released high while SCL high.
  - Acknowledge: 9th clock cycle, receiver pulls SDA low (ACK) or leaves high (NACK).
- **Bus Recovery**: If a slave locks SDA low, master toggles SCL up to 9 times to reset slave state machine.

## Standards & References
- **Standards**: NXP UM10204 (I2C-bus specification and user manual).
