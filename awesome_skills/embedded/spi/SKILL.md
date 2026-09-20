---
name: spi
description: "Serial Peripheral Interface: master-slave topology, clock polarity/phase (CPOL, CPHA modes 0-3), Quad-SPI (QSPI), and high-speed PCB routing"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/spi/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Serial Peripheral Interface (SPI)

## Scope
SPI synchronous bus protocol engineering, 4-wire signaling, high-speed flash interfaces (Quad-SPI, Octal-SPI), and bus timing constraints.

## Protocol Mechanics & Modes
- **4 Signals**: SCLK (Serial Clock), MOSI (Master Out Slave In), MISO (Master In Slave Out), $\overline{\text{SS}}$ / $\overline{\text{CS}}$ (Chip Select, active low).
- **Clock Modes (CPOL & CPHA)**:
  - Mode 0: $\text{CPOL}=0, \text{CPHA}=0$ (Clock idle low, sample on leading rising edge).
  - Mode 1: $\text{CPOL}=0, \text{CPHA}=1$ (Clock idle low, sample on trailing falling edge).
  - Mode 2: $\text{CPOL}=1, \text{CPHA}=0$ (Clock idle high, sample on leading falling edge).
  - Mode 3: $\text{CPOL}=1, \text{CPHA}=1$ (Clock idle high, sample on trailing rising edge).
- **Quad-SPI (QSPI)**: 4 data lines ($IO_0 - IO_3$) transferring 4 bits per clock cycle for external NOR flash memory-mapped execution (XIP).

## Standards & References
- **Standards**: Motorola SPI specification, JEDEC JESD216 (JESD216 Serial Flash Discoverable Parameters).
