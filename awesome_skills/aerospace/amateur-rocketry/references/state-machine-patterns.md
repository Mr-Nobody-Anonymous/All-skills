# State Machine Patterns for Amateur Rocketry Flight Software

## Flight State Machine Overview

Standard flight state machine for amateur/high-power rocketry:
```
[Pre-Flight] -> [Boost] -> [Coast] -> [Apogee] -> [Descent] -> [Recovery] -> [Landed]
```

### State Definitions:
1. **Pre-Flight**: Ground operations, sensor calibration, arming procedures
2. **Boost**: Motor ignition through burnout (high thrust phase)
3. **Coast**: Post-burnout to apogee (unpowered ascent)
4. **Apogee**: Peak altitude point (zero vertical velocity)
5. **Descent**: Apogee to main chute deployment (drogue chute phase)
6. **Recovery**: Main chute deployment to ground contact
7. **Landed**: Vehicle stationary on ground (post-flight analysis)

## State Machine Implementation Pattern

### Generic State Structure:
```c
typedef enum {
    STATE_PRE_FLIGHT,
    STATE_BOOST,
    STATE_COAST,
    STATE_APOGEE,
    STATE_DESCENT,
    STATE_RECOVERY,
    STATE_LANDED,
    STATE_FAULT
} FlightState_t;

typedef struct {
    FlightState_t current_state;
    FlightState_t previous_state;
    uint32_t state_entry_time_ms;
    uint32_t time_in_state_ms;
    
    // Transition conditions
    bool (*exit_conditions[8])(void);
    void (*entry_actions[8])(void);
    void (*exit_actions[8])(void);
    void (*during_actions[8])(void);
} FlightStateMachine_t;
```

### State Transition Logic:
```c
void update_state_machine(FlightStateMachine_t* fsm) {
    uint32_t now = millis();
    fsm->time_in_state_ms = now - fsm->state_entry_time_ms;
    
    // Check exit conditions for current state
    if (fsm->exit_conditions[fsm->current_state]()) {
        // Execute exit actions
        if (fsm->exit_actions[fsm->current_state]) {
            fsm->exit_actions[fsm->current_state]();
        }
        
        // Transition to next state
        FlightState_t next_state = get_next_state(fsm->current_state);
        
        // Execute entry actions for new state
        if (fsm->entry_actions[next_state]) {
            fsm->entry_actions[next_state]();
        }
        
        // Update state tracking
        fsm->previous_state = fsm->current_state;
        fsm->current_state = next_state;
        fsm->state_entry_time_ms = now;
    }
    
    // Execute during actions for current state
    if (fsm->during_actions[fsm->current_state]) {
        fsm->during_actions[fsm->current_state]();
    }
}
```

## Key State-Specific Details

### Pre-Flight:
- **Entry**: Sensor init, calibration, arming checks
- **During**: Sensor monitoring, ground comms
- **Exit**: Arm command + safety checks OR manual abort OR timeout

### Boost:
- **Entry**: Ignition start, motor fire command
- **During**: High-freq accel/gyro (1000+ Hz), thrust vector control, structural monitoring
- **Exit**: Accel < thrust threshold OR time-based burnout OR max boost duration

### Coast:
- **Entry**: Deploy boost-phase mechanisms
- **During**: Standard telemetry (100 Hz), apogee prediction, drogue arming
- **Exit**: Vertical velocity crosses zero OR predicted apogee within window OR max coast time

### Apogee:
- **Entry**: Fire separation charge (if used), deploy drogue, start descent timer
- **During**: Monitor descent rate for drogue stability, prepare main chute params
- **Exit**: Drogue deployed + descent rate stabilized OR time at apogee exceeded OR manual main chute

### Descent:
- **Entry**: Record apogee altitude, begin descent rate monitoring
- **During**: Altitude/velocity tracking, wind drift estimation, main chute algo eval
- **Exit**: Altitude < main chute threshold OR descent rate > drogue-only limits OR manual main chute

### Recovery:
- **Entry**: Deploy main parachute
- **During**: Monitor descent rate for main chute inflation, ground track prediction, beacon activation
- **Exit**: Landing detected (low velocity + stable orientation) OR touchdown confirmation OR max descent time

### Landed:
- **Entry**: Disable pyrotechnic safing, save flight data, activate recovery beacon
- **During**: Low-power telemetry, sensor data preservation, await recovery team
- **Exit**: Manual reset for next flight

## Guarded Transition Patterns

### Hysteresis Implementation:
Prevent rapid state chattering near transition boundaries:
```c
// Apogee detection with hysteresis
bool check_apogee_exit_condition(void) {
    static float max_altitude = 0.0f;
    float current_altitude = get_altitude();
    
    // Update maximum altitude seen
    if (current_altitude > max_altitude) {
        max_altitude = current_altitude;
    }
    
    // Exit coast state when:
    // 1. Vertical velocity negative for sustained period AND
    // 2. Altitude has dropped significantly from peak
    bool descending = (get_vertical_velocity() < -0.5f); // m/s
    bool significant_drop = (max_altitude - current_altitude) > 5.0f; // meters
    
    return descending && significant_drop;
}
```

### Redundant Condition Checking:
Multiple sensors for critical transitions:
```c
bool check_boost_exit_condition(void) {
    // Primary: Accelerometer-based burnout detection
    bool accel_burnout = (get_acceleration_z() < 2.0f); // Less than 2G
    
    // Secondary: Chamber pressure drop (if available)
    bool pressure_burnout = (get_chamber_pressure() < 100000.0f); // < 1 bar
    
    // Tertiary: Time-based backup
    bool time_burnout = (get_time_in_state() > expected_burn_time * 1.2f);
    
    // Require at least two indications
    int indications = (accel_burnout ? 1 : 0) + 
                     (pressure_burnout ? 1 : 0) + 
                     (time_burnout ? 1 : 0);
                     
    return indications >= 2;
}
```

## Critical Safety Considerations

### Fault Detection and Recovery:
- Implement watchdog timers for each state
- Independent altitude verification (barometer + GPS + accelerometer)
- Manual override capability via ground command or mechanical switch

### State Persistence:
- Save state to non-volatile memory on each transition
- Power-on state reconstruction from storage
- CRC protection for state variables in memory

### Testing Guidelines:
- Unit test each state's entry/exit/during actions
- Simulate sensor failures and verify fault handling
- Test transition boundaries with edge case values
- Validate timing constraints under worst-case scenarios

## Implementation Checklist

- [ ] Define state enumeration with clear entry/exit criteria
- [ ] Implement state transition logic with hysteresis
- [ ] Create entry/action/during functions for each state
- [ ] Implement redundant condition checking for critical transitions
- [ ] Add fault detection and safe state handling
- [ ] Include state persistence to non-volatile memory
- [ ] Implement comprehensive unit tests for each state
- [ ] Validate timing requirements under worst-case scenarios
- [ ] Document configuration parameters for vehicle-specific tuning

## EuRoC-Specific State Machine Requirements

### Mandatory GPS Logging State Note
> **EuRoC SRD Requirement**: All flight computers must log GPS position data at a minimum rate of 1Hz throughout the entire flight trajectory. This data must be stored in non-volatile memory and included in the post-flight data package submitted to the Technical Evaluation Board. The GPS logging function shall be considered safety-critical and shall continue operating even if other non-essential systems experience faults.

### CATS Vega State Tracking Requirement
> **EuRoC Range Safety Requirement**: When launching from facilities that support CATS Vega (Command and Telemetry System for Vega rocket) operations, flight software must implement a specific state to monitor for CATS Vega telemetry signals. This state shall:
> - Monitor the 869.4-869.65 MHz frequency band for CATS Vega transmissions
> - Trigger a safety hold state if CATS Vega activity is detected during ascent phase
> - Maintain logs of CATS Vega signal strength and frequency for post-flight analysis
> - Automatically exit the CATS Vega monitoring state upon landing detection