# Telemetry Patterns for Amateur Rocketry

## LoRa Packet Structure

Standard LoRa packet format for rocketry telemetry:
```
+--------+------+--------+---------+------+
| Preamble | Sync | Header | Payload | CRC  |
+--------+------+--------+---------+------+
```

### Field Definitions:
- **Preamble**: 8+ bytes of 0x55 for receiver synchronization
- **Sync Word**: 2 bytes (typically 0x34 0x12 for LoRaWAN compatibility)
- **Header**: Variable length (explicit/implicit mode)
  - Explicit: 4 bytes (Address, Length, Packet Type, Flags)
  - Implicit: Pre-configured parameters
- **Payload**: Sensor data (typically 1-50 bytes)
- **CRC**: 2 bytes CCITT-CRC for error detection

### Recommended Configuration:
- Spreading Factor: SF7-SF12 (balance range vs data rate)
- Bandwidth: 125 kHz (standard for ISM bands)
- Coding Rate: 4/5 (good error correction without excessive overhead)
- Frequency Hopping: Optional for interference mitigation

## Frequency Planning (EuRoC/IREC/ESRA)

### Europe (863-870 MHz ISM Band) - EuRoC Primary Focus
- Primary frequencies: 868 MHz (center)
- Channel spacing: 200 kHz
- Max EIRP: 14 dBm (25mW) or 27 dBm (0.5W) with LBT
- Duty cycle: 1% or 0.1% depending on sub-band
- Recommended channels: 868.1, 868.3, 868.5 MHz
- Regulatory framework: ETSI EN 300 220 (equivalent to FCC Part 15 in US)
- Mandatory compliance: Listen-Before-Talk (LBT) and Adaptive Frequency Agility (AFA)

### United States (902-928 MHz ISM Band):
- Primary frequencies: 915 MHz (center)
- Channel spacing: 200 kHz
- Max EIRP: 36 dBm (4W) with duty cycle limits
- Recommended channels: 902.3, 902.5, 902.7, 902.9 MHz
- Regulatory framework: FCC Part 15
- Note: Higher power limits but stricter duty cycle enforcement in some regions

### EuRoC-Specific Considerations:
- RF Window Constraints in Airframe Design: Antenna placement must maintain line-of-sight to ground stations while accounting for carbon fiber shielding effects
- CATS Vega Telemetry Coordination: When flying near CATS Vega launch sites, avoid 869.4-869.65 MHz band reserved for aeronautical telemetry
- EU Duty-Cycle Planning Strategies: Implement adaptive transmission rates based on flight phase (higher during ascent/descent, lower during apogee)
- Geographical Restrictions: Certain EU countries have additional restrictions on 868 MHz band usage; verify national regulations for launch site location

### Implementation Notes:
- Use frequency agility to avoid interference
- Implement listen-before-talk (LBT) for EU compliance
- Consider geographical restrictions for specific channels
- Always verify local regulations before flight
- For EuRoC competitions, prioritize EU 863-870 MHz band compliance over US band usage

## Forward Error Correction (FEC)

### Reed-Solomon Implementation:
- Block codes: RS(255,223) for good balance
- Interleaving depth: 4-8 for burst error protection
- Implementation libraries: 
  - Custom C implementation for STM32
  - Reed Solomon library for Arduino
  - Built-in FEC in some LoRa modules

### Convolutional Coding Alternative:
- Constraint length: K=7
- Code rate: 1/2
- Generator polynomials: 0xED, 0x09 (octal 133, 171)
- Viterbi decoder implementation

### Practical Recommendations:
- For short packets (<32 bytes): Use Reed-Solomon only
- For longer packets: Combine convolutional + Reed-Solomon
- Always implement CRC in addition to FEC
- Test FEC performance with bit error injection

## SD Card Data Logging

### File System:
- FAT32 for compatibility with ground station tools
- exFAT for cards >32GB (if needed)
- Cluster size: 4096 bytes for optimal performance

### File Naming Convention:
```
FLIGHT_YYYYMMDD_HHMMSS.BIN
FLIGHT_20260525_143022.BIN
```

### Data Format:
Binary format for efficiency:
```c
typedef struct {
    uint32_t timestamp_ms;   // Time since boot
    float altitude_m;        // Barometric altitude
    float velocity_m_s;      // Vertical velocity
    float acceleration_m_s2[3]; // 3-axis acceleration
    float temperature_C;     // Internal temperature
    float pressure_Pa;       // Barometric pressure
    uint16_t battery_mV;     // Battery voltage
    uint8_t flight_state;    // Current flight state enum
    uint16_t crc16;          // CCITT-CRC of struct
} TelemetrySample_t;
```

### Logging Strategy:
- Sample rate: 100 Hz for flight-critical data
- Buffer size: 1024 samples (10 seconds at 100 Hz)
- Write trigger: Buffer full or altitude > 10m (launched)
- File size limit: 16MB (prevents card fill during long flights)
- Power loss protection: Supercapacitor for final buffer flush

### Ground Station Compatibility:
- Include text header in binary file:
  ```
  # ROCKET_TELEMETRY_V1
  # FIELDS: timestamp_ms,altitude_m,velocity_m_s,accel_x,accel_y,accel_z,temperature_C,pressure_Pa,battery_mV,flight_state
  # UNITS: ms,m,m/s,m/s2,m/s2,C,Pa,mV,enum
  # START_TIME: 2026-05-25T14:30:22Z
  ```
- Followed by binary data records

## Implementation Examples

### STM32 LoRa Configuration:
```c
// LoRa parameter initialization
LoRa.setFrequency(915000000);      // 915 MHz
LoRa.setSpreadingFactor(9);        // SF9
LoRa.setSignalBandwidth(125E3);    // 125 kHz
LoRa.setCodingRate4(5);            // 4/5
LoRa.setPreambleLength(8);         // 8 bytes
LoRa.setSyncWord(0x34);            // LoRaWAN sync word
LoRa.enableCrc();                  // Enable CRC
```

### SD Card Initialization:
```c
// SD card setup with error handling
if (!SD.begin(SD_CS_PIN)) {
    log_error("SD Card initialization failed");
    enter_safe_mode();
}

// Create new flight file
char filename[32];
time_t now = time(NULL);
strftime(filename, sizeof(filename), "FLIGHT_%Y%m%d_%H%M%S.BIN", localtime(&now));
File dataFile = SD.open(filename, FILE_WRITE);
if (!dataFile) {
    log_error("Failed to create data file");
    enter_safe_mode();
}

// Write header
dataFile.println("# ROCKET_TELEMETRY_V1");
dataFile.println("# FIELDS: timestamp_ms,altitude_m,velocity_m_s,accel_x,accel_y,accel_z,temperature_C,pressure_Pa,battery_mV,flight_state");
dataFile.println("# UNITS: ms,m,m/s,m/s2,m/s2,C,Pa,mV,enum");
dataFile.print("# START_TIME: ");
dataFile.println(iso8601_timestamp());
```

## Best Practices

### Power Management:
- LoRa sleep mode between transmissions (90%+ power savings)
- SD card power cycling to prevent corruption
- Brown-out detection for reliable reset

### Data Integrity:
- Dual logging: Primary SD card + backup flash
- Periodic file system checks
- Immutable log segments for critical phases

### Ground Station Considerations:
- Telemetry packet IDs for loss detection
- RSSI/SNR logging for link quality monitoring
- Encryption options for sensitive data (AES-128)
- Telemetry format versioning for backward compatibility

## Safety Notes
- Never exceed local transmission power limits
- Implement automatic transmit timeout (max 1 second continuous)
- Include failsafe beacon mode for recovery
- Test RF compatibility with ground equipment pre-flight