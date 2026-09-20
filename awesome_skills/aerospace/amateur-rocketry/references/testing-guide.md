# Testing Strategy Guide

## Test Levels
**MUST** implement four test levels for flight software:
1. **Unit Tests**: Individual functions with mocks (Unity/CMock)
2. **Integration Tests**: Module interfaces and interactions
3. **HIL Tests**: Hardware-in-the-loop with simulated inputs
4. **Flight Simulation**: End-to-end mission profiles

## Unity Framework Usage
**SHALL** follow Arrange-Act-Assert pattern:
```c
void test_altitude_calculation(void) {
    // Arrange
    sensor_data_t input = {.pressure = 101325, .temperature = 20};
    float expected_altitude = 0.0f;
    
    // Act
    float actual = calculate_altitude(&input);
    
    // Assert
    TEST_ASSERT_EQUAL_FLOAT(expected_altitude, actual, 0.1f);
}
```

## Hardware Abstraction Mocking
**SHOULD** mock hardware dependencies:
- **Sensor Interfaces**: Mock read() functions to return test values
- **Actuator Controls**: Mock drive() functions to verify commands
- **Timing Services**: Mock delay()/tick() for deterministic timing

## CMock/Ceedling Guidance
**SHALL** use CMock for automatic mock generation:
1. Define interfaces in header files
2. Run `ceedling module:create[Name]` to generate test/mock files
3. Use `expect_AndReturn()` for stubbing responses
4. Verify call counts with `call_count`

## Test Organization
**MUST** structure tests as:
- `test/` directory mirroring source structure
- Descriptive test names: `test_[module]_[function]_[scenario]`
- One assertion per test when possible
- Test fixtures for complex setup

## Flight Simulation Requirements
**SHALL** simulate:
- Sensor noise and drift
- Communication dropouts
- Fault injection scenarios
- Full mission profiles (pre-flight to recovery)

## Evidence Collection
**MUST** generate:
- Test reports with pass/fail counts
- Coverage reports (statement/branch)
- Static analysis integration (CPPcheck, Clang-Tidy)
- Test execution logs for auditing

