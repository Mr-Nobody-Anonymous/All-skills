# Code Review Checklist for Amateur Rocketry Software

## Purpose
Systematic review of flight software for safety, correctness, and maintainability.

## Function Correctness
- [ ] Behavior matches specification exactly
- [ ] All input parameter ranges handled correctly
- [ ] Output values within expected ranges
- [ ] Edge cases (min/max values, zero, null pointers) properly handled

### Error Handling
- [ ] All possible error conditions identified and handled
- [ ] Error return values checked and propagated
- [ ] System enters safe state on errors
- [ ] Error conditions logged for post-flight analysis

### Boundary Testing
- [ ] Array indices checked against bounds
- [ ] Buffer lengths validated before use
- [ ] Timing constraints verified (deadlines, timeouts)

## Style and Readability
### Naming
- [ ] Function/variable names descriptive and unambiguous
- [ ] Names follow conventions (get_/set_/is_ prefixes)
- [ ] Constants named meaningfully (no magic numbers)

### Formatting
- [ ] Indentation consistent and readable
- [ ] Line lengths reasonable (<= 80 characters preferred)
- [ ] Related operations grouped logically

### Comments
- [ ] Comments explain why, not what
- [ ] Complex algorithms/non-obvious decisions documented
- [ ] TODO comments addressed or tracked

## Architecture and Cohesion
### Responsibility
- [ ] Each module has single, well-defined responsibility
- [ ] Concerns properly separated (sensing vs. control vs. communication)

### Coupling
- [ ] Module dependencies explicit and minimal
- [ ] Global variables avoided or justified
- [ ] Data structures passed explicitly, not accessed globally
- [ ] Hardware dependencies isolated in abstraction layers

### Abstraction
- [ ] Hardware interactions hidden behind abstraction layers
- [ ] Abstraction layers thin enough to not impact performance

### Data Flow
- [ ] Data flow through system easy to trace
- [ ] Transformations on data clearly documented
- [ ] Data ownership and lifetime clear

## Exception Handling
### Detection
- [ ] All possible exception sources considered
- [ ] Sensor plausibility checks implemented
- [ ] Communication timeouts and failures handled
- [ ] Computational overflows/underflows prevented

### Response
- [ ] System responds to exceptions timely
- [ ] Exception responses prioritized by severity
- [ ] System enters well-defined safe state on exceptions
- [ ] Recovery attempted when appropriate, shutdown preferred

### Logging
- [ ] Exceptions logged with sufficient context for diagnosis
- [ ] Timestamps included in exception logs
- [ ] System state captured when exceptions occur

## Timing and Performance
### Execution Time
- [ ] Worst-case execution times estimated for critical paths
- [ ] Timing budgets allocated and respected
- [ ] Blocking operations minimized in interrupt contexts

### Resources
- [ ] Stack usage within safe limits
- [ ] Heap usage avoided or strictly controlled
- [ ] Static memory allocations sufficient for worst-case

### Rate Limiting
- [ ] Message rates limited to prevent bus overload
- [ ] Sensor sampling rates appropriate for application
- [ ] Control loop frequencies sufficient for stability

## Testing and Verification
### Coverage
- [ ] Unit tests present for all public functions
- [ ] Test cases cover normal, boundary, and error conditions
- [ ] Code coverage sufficient to detect untested paths

### Quality
- [ ] Tests follow Arrange-Act-Assert pattern
- [ ] Test names descriptive of what is being verified
- [ ] Mocks used appropriately to isolate units under test

### Integration
- [ ] Interfaces between modules tested
- [ ] Data format conversions verified
- [ ] Timing interactions between modules validated

## Hardware Interactions
### Register Access
- [ ] Hardware registers accessed through defined abstraction layers
- [ ] Bit-field manipulations clearly documented and verified
- [ ] Volatile qualifiers used correctly for memory-mapped I/O
- [ ] Read-modify-write operations performed atomically when needed

### Interrupt Safety
- [ ] Interrupt service routines kept short and fast
- [ ] Shared data between ISR and main code properly protected
- [ ] Interrupts disabled for minimal necessary durations

### DMA/Peripherals
- [ ] DMA transfers properly configured and monitored
- [ ] Peripheral clocks enabled before use, disabled when idle
- [ ] Unused peripherals disabled to save power

## Safety-Critical Specifics
### Fail-Safe
- [ ] System defaults to safe state on power-on/reset
- [ ] Watchdog timers used and properly serviced
- [ ] Critical outputs failsafe (valves close on power loss)
- [ ] Redundant checks performed for critical decisions

### Determinism
- [ ] System behavior predictable and repeatable
- [ ] Sources of non-determinism eliminated (uninitialized vars)
- [ ] Timing jitter within acceptable limits for control

### Health Monitoring
- [ ] System health checks performed regularly
- [ ] Critical parameters monitored for drift/degradation
- [ ] Fault detection and isolation mechanisms implemented

## Review Process
### Preparation
- [ ] Reviewer read relevant specifications and design docs
- [ ] Reviewer understands module's role in larger system
- [ ] Reviewer has access to test results and verification evidence

### Conduct
- [ ] Review focuses on code, not author
- [ ] Review comments specific, actionable, and kind
- [ ] Review addresses both present and missing elements
- [ ] Review considers maintainability as well as correctness

### Follow-up
- [ ] All review comments addressed or formally deferred
- [ ] Deferred comments tracked with clear justification
- [ ] Code re-reviewed after changes made
- [ ] Review decisions documented for audit purposes

## Application Examples
### Sensor Driver Review
```c
// Code under review:
uint16_t read_pressure_sensor() {
    uint16_t raw_value;
    raw_value = *((volatile uint16_t*)0x40012345);  // Hardware register
    return raw_value * 10 / 1024;  // Convert to kPa
}

// Review Application:
// Function Correctness:
// - [ ] Does conversion formula match sensor datasheet?
// - [ ] Are overflow conditions checked in multiplication?
//
// Hardware Interactions:
// - [ ] Is register access properly abstracted?
// - [ ] Is volatile qualifier used correctly?
//
// Style:
// - [ ] Are magic numbers (10, 1024) replaced with named constants?
```

### State Machine Review
```c
// Code under review:
void update_state() {
    switch(state) {
        case BOOST:
            if(pressure > threshold) {  // No debounce or filtering
                state = COAST;
                ignite_parachute();     // Direct hardware call
            }
            break;
        // ...
    }
}

// Review Application:
// Function Correctness:
// - [ ] Is pressure threshold validated against noise?
// - [ ] Are hysteresis or debouncing mechanisms considered?
//
// Architecture:
// - [ ] Is hardware call abstracted through proper layer?
// - [ ] Are state transition conditions clearly documented?
//
// Safety-Critical:
// - [ ] Are redundant checks used for critical deployment decision?
// - [ ] Is system in safe state if state transition fails?
```

## Maintenance
### Technical Debt
- [ ] Known issues documented in issue tracking system
- [ ] Shortcuts/temporary fixes clearly marked
- [ ] Plan to address technical debt before flight

### Knowledge Transfer
- [ ] Code understandable by someone new to project
- [ ] Complex algorithms explained in comments/docs
- [ ] Build and test procedures documented

### Change Impact
- [ ] Potential side effects of changes considered
- [ ] Regression tests run after modifications
- [ ] Interface changes communicated to dependent modules

## References
- Koopman, Philip. "Better Embedded System Software" - Code Reviews
- NASA Software Safety Guidebook
- BARR-C:2018 Embedded C Coding Standard
- MISRA C:2023 Guidelines