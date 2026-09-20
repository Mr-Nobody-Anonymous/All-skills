---
name: bootloaders
description: "Custom bootloader design, in-system programming (ISP), over-the-air (OTA) updates, dual-bank flash, and cryptographic signature verification"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/bootloaders/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Embedded Bootloaders & OTA Updates

## Scope
Bootloader engineering develops self-programming firmware residing in protected flash sectors to verify, decrypt, and install new application images safely.

## Bootloader Architecture & Protocols
- **Dual-Bank Flash Memory Architecture**:
  - Bank A (Active Application), Bank B (Staging Slot for New Image).
  - Power-loss safe update: verify CRC32 / SHA-256 and digital signature before updating boot vector table.
- **Vector Table Relocation**: Updating the Vector Table Offset Register (VTOR on ARM Cortex-M) before executing application `Reset_Handler`.
- **Over-The-Air (OTA) Protocols**: Chunked binary delivery over BLE, Wi-Fi, or cellular (MQTT, HTTPS, CoAP), rollback mechanism upon boot watchdog timeout.

## Tools & Standards
- **Standards**: NIST SP 800-193 (Platform Firmware Resiliency Guidelines).
- **Software**: MCUBoot, U-Boot, custom bare-metal bootloaders.
