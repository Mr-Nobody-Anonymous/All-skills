# Integration Guide: Amateur Rocketry & Embedded Rocketry Skills

## Purpose
This guide explains how to co-load and effectively use the amateur-rocketry skill alongside the embedded-rocketry skill for student rocketry projects. It defines boundaries, complementary usage patterns, and workflow integration.

## Skill Boundaries

### Amateur Rocketry Skill Focus
- **Process & Standards**: Safety-critical development practices (NASA Power of 10, MISRA, BARR-C)
- **Documentation**: Competition requirements (IREC/ESRA), test procedures, flight reviews
- **Flight Software Architecture**: State machines, telemetry patterns, ground support systems
- **Verification & Validation**: Testing strategies, coverage requirements, audit preparation

### Embedded Rocketry Skill Focus
- **Hardware Implementation**: STM32 configuration, peripheral drivers, register-level programming
- **Real-Time Systems**: RTOS usage, interrupt handling, timing constraints
- **Low-Level Telemetry**: Direct sensor interfacing, ADC/DAC configuration, communication protocols
- **Memory Management**: Stack/heap allocation, DMA usage, peripheral initialization

## Co-Loading Guidelines

### When to Load Both Skills
Load both skills when working on:
- Flight computer firmware development
- Payload controller software
- Ground station communication systems
- Any embedded rocketry software requiring both safety standards and hardware implementation

### Loading Order
1. Load `embedded-rocketry` first for hardware/foundation concerns
2. Load `amateur-rocketry` second for process/standards overlay
3. The amateur-rocketry skill provides governance over the embedded-rocketry implementation

## Complementary Usage Patterns

### Flight Software Development Workflow
1. **Explore Phase** (amateur-rocketry lead):
   - Define mission requirements and safety constraints
   - Identify applicable standards and competition rules
   - amateur-rocketry: Explore → embedded-rocketry: Explore

2. **Specify Phase** (amateur-rocketry lead):
   - Write safety-critical requirements with testability
   - Specify telemetry structures and state machines
   - amateur-rocketry: Specify → embedded-rocketry: Specify (hardware interfaces)

3. **Implement Phase** (embedded-rocketry lead with amateur-rocketry governance):
   - Implement hardware drivers per embedded-rocketry
   - Apply safety standards per amateur-rocketry
   - embedded-rocketry: Implement → amateur-rocketry: Implement (standards compliance)

4. **Verify Phase** (Joint responsibility):
   - embedded-rocketry: Hardware validation, unit tests
   - amateur-rocketry: Safety compliance, test coverage, documentation
   - Cross-validate: Does hardware implementation meet safety requirements?

5. **Archive Phase** (amateur-rocketry lead):
   - Document flight results and lessons learned
   - Prepare competition documentation
   - Archive build configurations and test evidence

## Boundary Definitions

### Process vs. Domain Boundary
- **Process Boundary** (amateur-rocketry): How we develop (standards, documentation, reviews)
- **Domain Boundary** (embedded-rocketry): What we develop (drivers, protocols, real-time behavior)

### Decision Making Authority
- Safety/process questions → amateur-rocketry has final say
- Hardware/implementation questions → embedded-rocketry has final say
- Conflicts resolved by: Safety > Functionality > Schedule

## Common Flight Software Tasks Integration

### Telemetry System Development
1. **embedded-rocketry**: Configure UART/SPI, implement packet encoding/decoding
2. **amateur-rocketry**: Define packet structure per competition rules, add CRC validation, specify transmission schedules
3. **Joint**: Verify timing constraints meet flight phase requirements

### State Machine Implementation
1. **embedded-rocketry**: Implement timer interrupts, sensor polling loops
2. **amateur-rocketry**: Define flight states with entry/exit conditions, specify guarded transitions
3. **Joint**: Validate timing bounds satisfy NASA Power of 10 loop requirements

### Ground Support Equipment
1. **embedded-rocketry**: Implement USB/Serial communication, command parsing
2. **amateur-rocketry**: Define GSE procedures, safety interlocks, data visualization requirements
3. **Joint**: Test command-response timing and error handling

## Verification Cross-Checks

### Safety Standards Verification
- amateur-rocketry provides checklists for:
  - NASA Power of 10 compliance (no dynamic memory, bounded loops)
  - MISRA C essentials (signedness conversions, pointer arithmetic)
  - BARR-C guidelines (no static globals, explicit function contracts)

### Hardware Validation Verification
- embedded-rocketry provides methods for:
  - Peripheral register validation
  - Timing analysis with oscilloscope/logic analyzer
  - Communication protocol verification (baud rates, packet integrity)

## Conflict Resolution Examples

### Scenario: Memory Allocation for Telemetry Buffer
- embedded-rocketry preference: Dynamic allocation for flexibility
- amateur-rocketry requirement: No dynamic memory after initialization (NASA Power of 10 Rule 3)
- **Resolution**: Pre-allocate fixed-size buffers at startup, implement ring buffer with compile-time bounds

### Scenario: Floating-Point Usage for Altitude Calculation
- embedded-rocketry preference: FP for simplicity and accuracy
- amateur-rocketry requirement: <2% floating-point operations (NASA Power of 10 Rule 4)
- **Resolution**: Use fixed-point math for critical flight phases, limit FP to ground processing only

### Scenario: Function Pointers for State Machine
- embedded-rocketry preference: Function pointer state machines for flexibility
- amateur-rocketry requirement: No function pointers (NASA Power of 10 Rule 10)
- **Resolution**: Use switch-state enum with explicit function calls, maintainability through clear naming

## Maintenance Guidelines

### Skill Updates
- When embedded-rocketry updates hardware patterns, amateur-rocketry verifies safety compliance
- When amateur-rocketry updates standards, embedded-rocketry validates hardware compatibility

### Version Compatibility
- Both skills should maintain backward compatibility within major versions
- Breaking changes require joint validation and updated integration documentation

### Troubleshooting Co-Loading Conflicts
1. Identify which skill governs the concern (process vs domain)
2. Apply the governing skill's hard rules
3. Document exception with justification if unavoidable
4. Verify exception doesn't violate higher-priority constraints from other skill