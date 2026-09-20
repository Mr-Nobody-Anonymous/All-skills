---
name: embedded-security
description: "Hardware security: Secure Boot, Root of Trust (RoT), ARM TrustZone, cryptographic accelerators (AES/ECC), secure key storage, and side-channel mitigation"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/embedded-security/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Embedded Hardware Security

## Scope
Embedded security secures microcontroller firmware and cryptographic keys against physical tampering, reverse engineering, unauthorized firmware updates, and side-channel attacks.

## Security Primitives & Architectures
- **Root of Trust (RoT)**: Immutable public key burned into hardware One-Time-Programmable (OTP) eFuses verifying the initial bootloader stage.
- **Secure Boot Chain**: Cryptographic signature verification (RSA-2048 or ECDSA P-256) executed at each boot phase before transferring execution.
- **Hardware Isolation (ARM TrustZone-M)**: Silicon partition into Secure and Non-Secure memory, peripherals, and interrupts; transitions only via secure gateway instructions (`SG`).
- **Cryptographic Accelerators**: Hardware engines for AES-128/256, SHA-256, True Random Number Generator (TRNG).
- **Tamper Protection**: Active mesh shields, brownout detection, side-channel attack (DPA) resistance, JTAG debug port permanent disabling (RDP Level 2).

## Tools & Standards
- **Standards**: NIST SP 800-140, PSA Certified (Platform Security Architecture), SESIP.
