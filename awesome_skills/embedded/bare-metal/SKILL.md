---
name: bare-metal
description: "Programming without an OS: startup code (crt0), linker scripts (.ld), memory section placement, and super-loop scheduling"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/bare-metal/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Bare-Metal Embedded Systems

## Scope
Bare-metal development programs microcontrollers directly without an operating system, handling startup initialization, linker script layout, and deterministic execution loops.

## Low-Level System Mechanics
- **Linker Script (`.ld`)**:
  - Defines `MEMORY` blocks (`FLASH`, `RAM`) with origins and lengths.
  - Assigns `SECTIONS`: `.text` (code), `.rodata` (constants), `.data` (initialized RAM data copied from Flash), `.bss` (zero-initialized RAM data), stack and heap bounds.
- **Startup Code (`crt0.s` / `startup.c`)**:
  1. Sets initial Stack Pointer ($SP$).
  2. Copies `.data` from Flash to RAM.
  3. Zeroes the `.bss` section in RAM.
  4. Calls system clock configuration and jumps to `main()`.
- **Super-Loop Pattern**: Foreground interrupt handlers (ISRs) capture high-priority real-time events; background `while(1)` loop processes accumulated event flags.

## Tools & References
- **Tools**: GNU Binutils (`ld`, `objdump`, `readelf`, `nm`), Make/CMake.
