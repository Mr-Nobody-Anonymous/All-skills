---
name: freertos
description: "FreeRTOS kernel API: tasks, queues, semaphores, software timers, event groups, stream buffers, and heap memory managers"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/freertos/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# FreeRTOS Kernel Implementation

## Scope
Practical firmware development using the FreeRTOS open-source real-time kernel across ARM Cortex-M, ESP32, and RISC-V microcontrollers.

## FreeRTOS API & Architecture
- **Task Management**: `xTaskCreate()`, `vTaskDelayUntil()` (absolute periodic timing), `vTaskSuspend()`, `vTaskPrioritySet()`.
- **Inter-Task Communication**:
  - Queues: `xQueueSend()`, `xQueueReceive()`, `xQueueSendFromISR()`.
  - Mutexes: `xSemaphoreCreateMutex()`, `xSemaphoreTake()`, `xSemaphoreGive()`.
  - Direct Task Notifications: Fast, lightweight primitive bypassing queue overhead (`xTaskNotifyGive()`).
- **Memory Allocators**: `heap_1.c` (allocate only), `heap_4.c` (best-fit with block coalescing, standard choice), `heap_5.c` (spans multiple non-contiguous memory banks).

## Tools & Standards
- **Canonical References**: Barry — *Mastering the FreeRTOS Real Time Kernel*.
