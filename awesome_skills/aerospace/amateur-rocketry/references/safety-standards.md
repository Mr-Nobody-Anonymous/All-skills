# Safety Standards for Amateur Rocketry Software

## NASA Power of 10 Subset (Required)
**MUST** enforce these 3 rules:

### 1. **No Goto Statements**
   - **Why**: Prevents unpredictable control flow that complicates verification and validation
   - **Violation**: `goto error_handler;`
   - **Fix**: Use structured error handling with return codes and early returns
   - **Exception Handling**: Only use `setjmp/longjmp` for fault recovery with documented justification

### 2. **No Unbounded Recursion**
   - **Why**: Prevents stack overflow in embedded systems with limited stack space
   - **Violation**: Recursive function without base case or depth limit
   - **Fix**: Use iteration or add recursion depth counter with hard limit
   - **Verification**: Static analysis tools must verify all recursion has provable bounds

### 3. **Loops Must Have Static Bounds**
   - **Why**: Ensures predictable execution time for schedulability analysis
   - **Violation**: `while (sensor_reading() < threshold) { ... }`
   - **Fix**: `for (int i=0; i<MAX_ITER && sensor_reading()<threshold; i++) { ... }`
   - **Definition**: Loop bounds must be determinable at compile time, not runtime

## MISRA C:2012 Essentials (Required)
**MUST** enforce these 6 rules:

### 4. **No Implicit Signedness Conversions**
   - **Why**: Prevents unexpected value changes that propagate through calculations
   - **Violation**: `int16_t x = -5; uint16_t y = x;`
   - **Fix**: Explicit cast: `uint16_t y = (uint16_t)x;`
   - **Tooling**: Enable compiler warnings for sign changes (-Wsign-conversion)

### 5. **Initialize All Variables**
   - **Why**: Prevents use of uninitialized memory leading to undefined behavior
   - **Violation**: `int value; return value;`
   - **Fix**: `int value = 0; return value;`
   - **Exception**: Variables assigned in all code paths before use (document with comment)

### 6. **Limit Macro Usage**
   - **Why**: Reduces preprocessor complexity and improves debuggability
   - **Violation**: `#define MAX(a,b) ((a)>(b)?(a):(b))`
   - **Fix**: Use static inline functions: `static inline int max(int a, int b) { return a>b?a:b; }`
   - **Allowed**: Simple constant definitions (`#define MAX_ITER 100`)

### 7. **No Pointer Arithmetic on Void Pointers**
   - **Why**: Prevents undefined behavior and type safety violations
   - **Violation**: `void* ptr; ptr += 4;`
   - **Fix**: Cast to appropriate pointer type before arithmetic
   - **Alternative**: Use `uint8_t*` for byte-level operations

### 8. **No Assignment in Boolean Context**
   - **Why**: Prevents accidental assignment when comparison was intended
   - **Violation**: `if (x = y) { ... }` // assigns y to x, then checks if x!=0
   - **Fix**: Use explicit comparison: `if (x == y) { ... }`
   - **Tooling**: Compiler warning (-Wparentheses) should catch this

### 9. **Limited Use of Floating-Point**
   - **Why**: Floating-point operations are slower and less predictable in embedded systems
   - **Violation**: Using float/double for control loops without justification
   - **Fix**: Use fixed-point arithmetic or integer scaling where possible
   - **Exception**: Sensor fusion algorithms requiring floating-point (document justification)

## BARR-C Guidelines (Recommended)
**SHOULD** follow these guidelines:

### 10. **Minimize Global Variables**
    - **Why**: Reduces coupling and unintended side effects between modules
    - **Violation**: Non-static global variables accessible across files
    - **Fix**: Use `static` for file-scoped variables or pass as parameters
    - **Exception**: Hardware registers or RTOS objects (document and minimize)

### 11. **Check All Function Return Codes**
    - **Why**: Ensures error handling and prevents silent failures
    - **Violation**: `init_sensor();` // ignoring return value
    - **Fix**: `if (init_sensor() != SUCCESS) { handle_error(); return; }`
    - **Exception**: Functions declared `void` that cannot fail (document why)

### 12. **Use Enumerated Types for State Machines**
    - **Why**: Improves readability and prevents invalid state values
    - **Violation**: Using `#define` or `const int` for state values
    - **Fix**: `typedef enum { PRE_FLIGHT, BOOST, COAST, APOGEE, DESCENT, RECOVERY, LANDED } flight_state_t;`
    - **Benefit**: Compiler checks for unhandled enum values in switch statements

### 13. **Constants for Magic Numbers**
    - **Why**: Improves maintainability and self-documenting code
    - **Violation**: `if (timeout > 3000) { ... }` // what is 3000?
    - **Fix**: `#define SENSOR_TIMEOUT_MS 3000` or `const uint32_t SENSOR_TIMEOUT_MS = 3000;`
    - **Placement**: Define constants near where they're used or in a central header

### 14. **Return Status from All Functions**
    - **Why**: Enables error propagation and consistent error handling
    - **Violation**: `void init_system() { ... }` // no way to report failure
    - **Fix**: `error_t init_system() { ... return SUCCESS; }`
    - **Exception**: `main()` function and ISRs (document why)

### 15. **Compiler Warnings Treated as Errors**
    - **Why**: Ensures code quality and prevents accumulation of technical debt
    - **Violation**: Building with warnings that are ignored
    - **Fix**: Configure build system to treat warnings as errors (`-Werror`)
    - **Process**: Fix warnings immediately; do not allow them to accumulate

## Implementation Guidance

### During Code Review:
- Apply rules using checklists derived from this document
- Start with NASA Power of 10 as baseline for all flight software
- Use static analysis tools: CPPcheck, Clang-Tidy, PC-lint
- Verify rule compliance in both new code and modifications

### Toolchain Recommendations:
- Compiler flags: `-Wall -Wextra -pedantic -Werror`
- Static analysis: Run on every commit via pre-commit hooks
- Formatters: Use clang-format to maintain consistent style
- Complexity tools: Monitor cyclomatic complexity (<10 per function)

### Documentation Requirements:
- Document exceptions to rules with justification and approval
- Maintain traceability from requirements to code to test cases
- Keep version history of this document as rules evolve

## SRD Safety Analysis Callout Box
> **EuRoC Student Rocketry Directive (SRD) Safety Analysis Requirements**
> 
> All EuRoC participating teams must conduct and document a comprehensive safety analysis including:
> - Hazard identification and risk assessment for all rocket subsystems
> - Failure modes and effects analysis (FMEA) for critical components
> - Fault tree analysis (FTA) for top-level safety events
> - Mitigation strategies and verification plans for identified risks
> - Independent review of safety analysis by team mentor or safety officer
> 
> The safety analysis must be submitted as part of the Technical Evaluation Board review package and updated throughout the design process as designs mature.

## EU Radio Compliance Verification Note
> **Important**: For EuRoC competitions held in European countries, teams must verify radio frequency compliance with EU regulations:
> - Equipment must bear CE marking for 863-870 MHz band usage
> - Transmitters must comply with ETSI EN 300 220-1 V3.1.1 (2017-02)
> - Effective Isotropic Radiated Power (EIRP) must not exceed limits without proper authorization
> - Duty cycle restrictions must be implemented in software (typically 1% or 0.1% depending on sub-band)
> - Listen-Before-Talk (LBT) or equivalent spectrum sensing mechanism is required
> - Teams should retain documentation of compliance testing or manufacturer declarations

## Validation Approach
- **Unit Tests**: Verify individual functions comply with rules
- **Code Reviews**: Use checklist to verify rule adherence
- **Static Analysis**: Automated verification on every build
- **Integration Tests**: Verify rule compliance in system context
- **Audit Trail**: Maintain records of rule exceptions and justifications

(End of file - total 228 lines)
