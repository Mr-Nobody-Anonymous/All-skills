---
name: uart
description: "Universal Asynchronous Receiver-Transmitter: baud rate calculation, framing, parity, flow control (RTS/CTS), and RS-485 differential bus"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/uart/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# UART & RS-485 Communication

## Scope
UART protocol engineering, framing parameters, hardware flow control, FIFO buffer management, and differential industrial multidrop networks (RS-485 / Modbus).

## Protocol Specification & Hardware
- **Framing**: 1 Start bit (low), 5-9 Data bits (LSB first), Optional Parity bit (Even/Odd/None), 1-2 Stop bits (high).
- **Baud Rate Clock Generation**:
  $$\text{Baud} = \frac{f_{\text{peripheral}}}{16 \times (\text{USARTDIV})}$$
- **Hardware Flow Control**: RTS (Request to Send) and CTS (Clear to Send) lines preventing receiver FIFO overrun.
- **RS-485 Differential Multidrop**: Half-duplex differential signaling over twisted pair ($A - B$), common-mode rejection, $120\Omega$ termination resistors.

## Standards & References
- **Standards**: TIA/EIA-485-A, Modbus Serial Protocol.
