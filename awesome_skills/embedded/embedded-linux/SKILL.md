---
name: embedded-linux
description: "Buildroot, Yocto Project, Device Trees, U-Boot bootloader, kernel modules, sysfs, and embedded user-space applications"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/embedded-linux/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Embedded Linux

## Scope
Embedded Linux systems architecture, covering boot sequences, board support packages (BSP), custom Linux distribution compilation, device trees, and kernel modules.

## System Architecture
- **Boot Chain**: ROM Code $\to$ Secondary Program Loader (SPL) $\to$ U-Boot $\to$ Linux Kernel $\to$ Root Filesystem (`init` / systemd).
- **Device Tree (`.dts` / `.dtb`)**: Hardware description language passing memory addresses, interrupt lines, and pin assignments to kernel drivers without hardcoding in C.
- **Build Systems**:
  - Buildroot: Fast, simple Makefile-based root filesystem and toolchain generator.
  - Yocto Project / OpenEmbedded: Recipe-based (`bitbake`) industrial standard for scalable custom Linux distributions.
- **Driver Model**: Character devices, platform devices, `sysfs` (`/sys/class/gpio`), `ioctl()`, and netlink sockets.

## Tools & Standards
- **Software**: Buildroot, Yocto, U-Boot, BusyBox.
- **Canonical References**: Hallinan — *Embedded Linux Primer*; Yaghmour et al. — *Building Embedded Linux Systems*.
