---
name: esp32
description: "Espressif ESP32/ESP32-S3/C3, ESP-IDF framework, dual-core FreeRTOS, Wi-Fi/BLE stacks, non-volatile storage (NVS), and deep sleep"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/esp32/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# ESP32 Embedded Systems

## Scope
Firmware engineering for Espressif ESP32 SoCs using the native ESP-IDF framework, dual-core task pinning, wireless stacks, and ultra-low-power ULP co-processors.

## ESP-IDF System Architecture
- **Dual-Core Execution**: Pinning FreeRTOS tasks to Core 0 (Protocol stack) or Core 1 (Application logic) via `xTaskCreatePinnedToCore()`.
- **Memory Architecture**: Embedded SRAM, external SPI Flash and PSRAM with hardware cache mapping.
- **Power Management**: Active, Modem-sleep, Light-sleep, Deep-sleep ($<10\mu\text{A}$), RTC memory retention, ULP coprocessor wake triggers.
- **Wireless Stacks**: Wi-Fi (Station, SoftAP, ESP-NOW), Bluetooth Low Energy (NimBLE stack).

## Tools & Standards
- **Framework**: ESP-IDF (C/C++), esptool.py, ESP-Prog.
