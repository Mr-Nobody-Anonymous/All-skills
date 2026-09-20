---
name: device-drivers
description: "Writing hardware abstraction layers (HAL), peripheral drivers (I2C, SPI, UART, ADC), DMA integration, and interrupt handlers"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/device-drivers/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Embedded Device Drivers

## Scope
Device driver engineering designs clean, robust software interfaces between low-level silicon registers and high-level application business logic.

## Driver Design Patterns
- **Layered Architecture**: Hardware Layer (Registers) $\to$ Device Driver $\to$ Hardware Abstraction Layer (HAL) $\to$ Application API.
- **Execution Modes**:
  1. *Blocking / Polling*: Spin-waits on status flags; simple but wastes CPU cycles.
  2. *Non-Blocking / Interrupt-Driven*: Initiates transfer and returns; notifies completion via callback.
  3. *DMA-Driven*: Hardware handles multi-byte streaming directly to/from RAM; interrupts only on buffer half/full completion.

## Tools & Standards
- **Canonical References**: Ganssle — *The Art of Designing Embedded Systems*.
