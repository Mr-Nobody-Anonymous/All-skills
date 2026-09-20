---
name: esp32
description: "'Use when writing firmware, wiring plans, or debugging for ESP32 / ESP32-S3 boards (DevKitC, S3-DevKitC-1, WROOM/WROVER modules). Provides exact GPIO/strapping-pin rules, ADC calibration and attenuation tables, LEDC PWM register limits, deep-sleep current budgets, brownout-with-motors wiring, esptoo"
category: robotics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/rahulbachina/robotics-skills"
source_repository: "rahulbachina/robotics-skills"
source_path: "skills/chips/esp32/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# ESP32 / ESP32-S3 Hardware Engineering

Covers classic ESP32 (Xtensa LX6 dual-core, 240 MHz) and ESP32-S3 (Xtensa LX7 dual-core, 240 MHz, native USB). Where behavior differs, both are stated. Default assumption: ESP32-DevKitC (WROOM-32) or ESP32-S3-DevKitC-1 (WROOM-1), Arduino core 3.x (IDF 5.x underneath) or MicroPython 1.22+.

---

## 1. Pin Selection — The Single Biggest Source of Broken Builds

### 1.1 Strapping pins (sampled at reset — wrong external load = boot failure)

**Classic ESP32:**

| GPIO | Strap function | Boot requirement | Safe use after boot? |
|------|---------------|------------------|---------------------|
| 0 | Boot mode | HIGH = run flash, LOW = download mode | Yes, but anything pulling it LOW at reset puts chip in bootloader. Has internal pull-up. OK for active-low button. |
| 2 | Boot mode (with GPIO0) | Must be LOW or floating to enter download mode | Yes. On-board LED on many DevKits. Do NOT tie HIGH if you need serial flashing. |
| 5 | SDIO timing | Outputs PWM-ish glitch at boot | Yes — but avoid for motor enable lines (boot glitch spins motors) |
| 12 (MTDI) | Flash voltage (VDD_SDIO) | **Must be LOW at reset** on 3.3 V flash modules (all WROOM/WROVER). Pulled HIGH at reset = flash runs at 1.8 V = boot loop. | Avoid as input with external pull-up. Fine as output after boot. |
| 15 (MTDO) | Debug log enable | LOW silences boot log; outputs glitch at boot | Yes |

**ESP32-S3:**

| GPIO | Strap function | Note |
|------|---------------|------|
| 0 | Boot mode | Same as classic — LOW at reset = download mode |
| 3 | JTAG signal source | Floating by default; weak — usually fine |
| 45 | VDD_SPI voltage | LOW = 3.3 V (default), HIGH = 1.8 V flash. **Never pull HIGH externally** on standard modules. |
| 46 | Boot mode / ROM log | Input-only-ish at boot; keep LOW or floating at reset |

**Rule for generated code/wiring:** never attach external pull-ups/downs, LEDs to GND, or driver enable lines to GPIO 0, 12, 45, 46 (and treat 2, 5, 15 as "glitches at boot"). Motor driver EN/PWM pins must go on non-strapping, non-glitching GPIOs (classic: 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33; S3: 4–18 except 3, plus 21, 35–42 with PSRAM caveat below).

### 1.2 Input-only and forbidden pins

**Classic ESP32:**
- GPIO 34, 35, 36 (VP), 39 (VN): **input only**, no internal pull-up/pull-down. Need external 10 kΩ pulls for buttons/encoders. Great for ADC.
- GPIO 6–11: connected to internal SPI flash. **Never use.** Touching them crashes/bricks the running firmware.
- GPIO 16, 17 on **WROVER** modules: used by PSRAM. Unavailable on WROVER; available on WROOM.

**ESP32-S3:**
- GPIO 26–32: SPI flash. Never use.
- GPIO 33–37: used by **octal** PSRAM/flash (e.g. N8R8 modules with 8 MB octal PSRAM). On N8R2/N16R2 (quad PSRAM) they're free. If you don't know the module variant, avoid 33–37.
- GPIO 19/20: native USB D−/D+. Using them as GPIO kills USB-CDC console.
- No input-only pins on S3; all GPIOs have programmable pulls.
- GPIO 43/44: default UART0 TX/RX (console).

### 1.3 GPIO matrix — what it does and doesn't fix

Any peripheral (UART, SPI, LEDC, RMT, I2C) can route to almost any GPIO through the matrix. Exceptions and gotchas:
- Signals routed through the matrix add ~2 ns and limit SPI to ~26 MHz on classic ESP32. For 40–80 MHz SPI use **IOMUX pins**: classic VSPI = 18(CLK)/19(MISO)/23(MOSI)/5(CS), HSPI = 14/12/13/15. On S3, SPI2 IOMUX = 12(CLK)/13(MISO)/11(MOSI)/10(CS).
- ADC, DAC (classic: GPIO 25/26 only), and touch are **analog functions tied to physical pins** — the matrix cannot move them.
- Classic ESP32 ADC1 = GPIO 32–39. ADC2 = GPIO 0, 2, 4, 12–15, 25–27. S3: ADC1 = GPIO 1–10, ADC2 = GPIO 11–20.
- At boot, all pins are inputs with pulls per strap table. Pins float HIGH-impedance until your code configures them — add external pull-downs (10 kΩ) on MOSFET gates and motor-driver inputs so outputs stay off during the ~300 ms boot window.

---

## 2. ADC — Nonlinear, Noisy, and WiFi Steals ADC2

### 2.1 Hard rules
1. **ADC2 is unusable while WiFi is active** (classic ESP32 and S3). `adc2_get_raw()` returns ESP_ERR_TIMEOUT / Arduino `analogRead` returns garbage or 0. If the project uses WiFi, put every analog input on ADC1. This is the #1 analog bug in ESP32 projects.
2. ADC is **not** rail-to-rail and **not** linear at the extremes. With 11 dB (`ADC_ATTEN_DB_11` / `ADC_ATTEN_DB_12` in IDF 5) attenuation, usable range is approximately **150 mV – 2450 mV** on classic ESP32 (datasheet says "suggested range ≤ 2450 mV" despite 3.3 V often quoted). Readings above ~2.45 V clip and flatten well before 4095.
3. Attenuation table (classic ESP32, per-channel):

| Attenuation | Usable input range | Use for |
|---|---|---|
| 0 dB | 100–950 mV | precision low-voltage sensors |
| 2.5 dB | 100–1250 mV | |
| 6 dB | 150–1750 mV | best linearity/range tradeoff |
| 11 dB | 150–2450 mV | battery dividers, pots (default in Arduino) |

4. Each chip has a different Vref (1.0–1.2 V, nominal 1.1 V). **Always use the calibration API**, never `raw * 3300 / 4095`:

```cpp
// Arduino core 3.x — calibrated, returns millivolts
uint32_t mv = analogReadMilliVolts(34);   // uses eFuse cal data internally
```

```c
// ESP-IDF 5.x
adc_oneshot_unit_handle_t adc1;
adc_oneshot_unit_init_cfg_t ucfg = { .unit_id = ADC_UNIT_1 };
adc_oneshot_new_unit(&ucfg, &adc1);
adc_oneshot_chan_cfg_t ccfg = { .atten = ADC_ATTEN_DB_12, .bitwidth = ADC_BITWIDTH_12 };
adc_oneshot_config_channel(adc1, ADC_CHANNEL_6, &ccfg);  // GPIO34 = ADC1_CH6

adc_cali_handle_t cali;
adc_cali_line_fitting_config_t lcfg = { .unit_id = ADC_UNIT_1, .atten = ADC_ATTEN_DB_12, .bitwidth = ADC_BITWIDTH_12 };
adc_cali_create_scheme_line_fitting(&lcfg, &cali);
int raw, mv;
adc_oneshot_read(adc1, ADC_CHANNEL_6, &raw);
adc_cali_raw_to_voltage(cali, raw, &mv);
```

```python
# MicroPython
from machine import ADC, Pin
adc = ADC(Pin(34), atten=ADC.ATTN_11DB)   # GPIO34, ADC1
mv = adc.read_uv() // 1000                # read_uv() applies eFuse calibration
```

5. **Noise mitigation:** sample 16–64x and average (or median-of-5 for spiky sources); add 100 nF from the ADC pin to GND; keep WiFi TX bursts in mind — even ADC1 readings jump ±30 mV during transmission. For battery monitoring, read between WiFi activity.
6. Battery divider for a 1S LiPo (4.2 V max) into 11 dB range: 100 kΩ : 100 kΩ gives 2.1 V max — inside the 2.45 V linear ceiling. Add 100 nF across the bottom resistor. Divider draws 21 µA continuously; for deep-sleep designs switch it with a P-MOSFET or use 1 MΩ : 1 MΩ + longer sampling settle time (≥10 ms after enabling).
7. ESP32-S3 ADC is somewhat better (curve-fitting calibration scheme: `adc_cali_create_scheme_curve_fitting`) but the ADC2-vs-WiFi rule still applies.

---

## 3. LEDC PWM — Frequency × Resolution Tradeoff

LEDC clock is 80 MHz (APB). Constraint: **freq × 2^resolution ≤ 80 MHz**.

| Frequency | Max resolution | Typical use |
|---|---|---|
| 50 Hz | 16-bit (use 14) | hobby servos |
| 1 kHz | 16-bit | LED dimming |
| 20 kHz | 11-bit (2048 steps) | silent motor PWM (above hearing) |
| 25 kHz | 11-bit | 4-wire PC fans |
| 78 kHz | 10-bit | high-freq buck |
| 312 kHz | 8-bit | absolute practical limit |

Classic ESP32: 16 channels (8 high-speed + 8 low-speed), 8 timers. S3: 8 channels, 4 timers, low-speed only (still fine to 40 MHz/1-bit theoretical). Channels sharing a timer share frequency.

```cpp
// Arduino core 3.x API (ledcSetup/ledcAttachPin are REMOVED in 3.x — common migration bug)
const int MOTOR_PIN = 16;
ledcAttach(MOTOR_PIN, 20000, 11);          // pin, freq, resolution → auto channel
ledcWrite(MOTOR_PIN, 1024);                // 50% of 2047  (3.x writes BY PIN, not channel)

// Servo at 50 Hz, 14-bit: period 20 ms → counts = us * 16384 / 20000
ledcAttach(SERVO_PIN, 50, 14);
auto servoUs = [](int us){ return (uint32_t)us * 16384 / 20000; };
ledcWrite(SERVO_PIN, servoUs(1500));       // center; 500–2500 µs typical range
```

```python
# MicroPython — duty_u16 is portable, duty() is 10-bit legacy
from machine import Pin, PWM
motor = PWM(Pin(16), freq=20000, duty_u16=0)
motor.duty_u16(32768)                      # 50%
servo = PWM(Pin(17), freq=50)
servo.duty_ns(1_500_000)                   # 1500 µs — duty_ns avoids resolution math
```

Gotchas:
- `ledcWrite` with duty == max gives a short glitch LOW on classic ESP32; for true 100% use duty = 2^res (Arduino 3.x handles this) or drive the pin GPIO-high.
- After `esp_deep_sleep_start()` wake, all LEDC config is lost — reinit.
- For drone ESCs / DShot use the **RMT** peripheral, not LEDC.
- MCPWM (classic + S3) is the right peripheral for H-bridge complementary pairs with dead-time; LEDC has no dead-time insertion. For an L298N/DRV8833/TB6612 with separate IN1/IN2, LEDC is fine.

---

## 4. Power, Brownout, and Motors — Why the Board Keeps Rebooting

### 4.1 The failure mode
Brownout detector trips at ~2.8 V (default) on the 3.3 V rail. Motor inrush (a stalled brushed motor draws 5–10× rated current) sags USB's 5 V, the AMS1117/SGM2212 regulator output dips below 2.8 V, chip prints `Brownout detector was triggered` and resets — usually exactly when the robot starts moving. WiFi TX bursts (peak ~500 mA at 3.3 V on classic ESP32, ~350 mA S3) compound it.

### 4.2 The correct wiring (non-negotiable for motor projects)

```
Battery (+) ──┬── Motor driver VM/VS  (motors powered DIRECTLY from battery)
              └── Buck converter or 5V reg ── ESP32 5V/VIN pin
Battery (−) ──┬── Motor driver GND
              └── ESP32 GND            ← COMMON GROUND, mandatory
ESP32 GPIO ──── driver IN1/IN2/PWM/EN  (signals only, mA-level)
```

Rules:
1. **Separate supplies, common ground.** Logic and motor power must share GND or PWM signals have no return path (symptom: driver does nothing, or erratic motion, or GPIO pins die from ground offset).
2. **Never power motors from the DevKit 3V3 or 5V pin.** The 3V3 regulator is good for ~500–800 mA total including the chip.
3. 470–1000 µF electrolytic across motor driver VM-GND, plus 100 nF ceramic, close to the driver. 100–470 µF across ESP32 5 V input helps survive sags.
4. Flyback: TB6612/DRV88xx have internal protection; L298N boards usually include diodes; bare H-bridges from discrete MOSFETs need Schottky diodes per leg.
5. USB + motors simultaneously (dev time): power motors from battery anyway; do not rely on USB's 500 mA.
6. If brownouts persist with good wiring, do NOT disable the detector (`CONFIG_ESP_BROWNOUT_DET=n`) as a "fix" — it converts clean resets into flash corruption. Fix the supply.
7. Servos: a single SG90 stall-spikes ~700 mA. Power servos from 5 V battery rail/buck, never from the DevKit 5 V pin if more than one servo.

### 4.3 Current budget cheat sheet (3.3 V rail)

| State | Classic ESP32 | ESP32-S3 |
|---|---|---|
| WiFi TX peak (802.11b) | ~500 mA | ~355 mA |
| WiFi active average | 95–180 mA | 90–120 mA |
| CPU 240 MHz, radio off | 40–68 mA | 40–66 mA |
| Modem-sleep (WiFi assoc, DTIM3) | ~20–27 mA avg | ~15–20 mA |
| Light sleep | 0.8 mA | 240 µA |
| Deep sleep (RTC timer) | 10 µA (chip) / **~50 µA–10 mA on a DevKit** | 7–8 µA (chip) |
| Hibernation | 5 µA | — |

DevKit reality: the USB-UART bridge (CP2102/CH340) and AMS1117 quiescent burn 1–10 mA forever. For real battery deep-sleep budgets use a bare module or a board designed for it (e.g. FireBeetle, TinyPICO, boards with ME6211/HT7833 regulators), or cut the bridge's power.

---

## 5. Deep Sleep — Patterns and Traps

```cpp
// Arduino — wake on timer + button (EXT0 must be an RTC GPIO)
#include "esp_sleep.h"
RTC_DATA_ATTR int bootCount = 0;           // survives deep sleep (8 KB RTC slow mem)

void setup() {
  ++bootCount;
  // ... do work fast; deep-sleep designs do everything in setup() ...
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);        // 60 s — note ULL, µs units
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_33, 0);             // wake on LOW; classic: RTC GPIOs only (0,2,4,12-15,25-27,32-39)
  rtc_gpio_pullup_en(GPIO_NUM_33);                          // internal pulls die in deep sleep unless RTC-held
  esp_deep_sleep_start();                                   // never returns; reboot from setup()
}
void loop() {}                                              // unreachable
```

```python
# MicroPython
import machine, esp32
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    pass  # woke from sleep — counters must live in RTC memory or flash
esp32.wake_on_ext0(pin=machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_UP), level=0)
machine.deepsleep(60_000)   # ms in MicroPython (vs µs in IDF — classic unit bug)
```

Traps:
- **Deep sleep is a reboot.** All RAM, peripheral config, WiFi state lost. Only `RTC_DATA_ATTR` variables and RTC GPIO hold states persist.
- Timer arg is **µs in IDF/Arduino, ms in MicroPython**. The 1000× error appears constantly in generated code.
- Classic ESP32 EXT0/EXT1 only work on RTC GPIOs (0, 2, 4, 12–15, 25–27, 32–39). S3: GPIO 0–21 are RTC-capable.
- GPIO output state floats during deep sleep unless held: `gpio_hold_en(pin)` + `gpio_deep_sleep_hold_en()`. Without this, MOSFETs/relays toggle on sleep entry.
- WiFi reconnect after wake costs 1–3 s and a 100+ mA burst; with static IP (`WiFi.config(...)`) and stored channel/BSSID you can get connect+publish under ~600 ms. Budget energy as (wake time × active current), not sleep current — wake duration dominates.
- Touch wake and ULP exist; ULP-RISC-V on S3 can poll sensors at ~µA cost.

---

## 6. Flashing with esptool — Recipes That Work

```bash
pip install esptool

# Identify chip + flash size first (resolves 90% of "wrong binary" issues)
esptool.py --port COM5 flash_id

# Full erase (do this when changing partition tables, NVS corruption, or framework)
esptool.py --port COM5 erase_flash

# Classic ESP32 — standard Arduino/IDF offsets
esptool.py --chip esp32 --port COM5 --baud 921600 write_flash \
  0x1000  bootloader.bin \
  0x8000  partitions.bin \
  0x10000 firmware.bin

# ESP32-S3 — BOOTLOADER IS AT 0x0, NOT 0x1000 (top S3 flashing mistake)
esptool.py --chip esp32s3 --port COM5 --baud 921600 write_flash \
  0x0     bootloader.bin \
  0x8000  partitions.bin \
  0x10000 firmware.bin

# MicroPython
esptool.py --chip esp32 --port COM5 erase_flash
esptool.py --chip esp32 --port COM5 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-*.bin
# S3 MicroPython images flash at 0x0
```

Troubleshooting table:

| Symptom | Cause | Fix |
|---|---|---|
| `Failed to connect: Wrong boot mode` | Auto-reset circuit not working / terminal holding port | Hold BOOT (GPIO0) button, tap RESET, release BOOT, retry. Close serial monitors. |
| Connects then `Invalid head of packet` | Baud too high for cable/bridge | Drop to `--baud 115200` |
| Flashes OK, boot loops with `flash read err, 1000` | Wrong flash mode/freq (QIO vs DIO) | Add `--flash_mode dio --flash_freq 40m`; WROOM is DIO-safe |
| S3 boot loops after flash | Bootloader written to 0x1000 | Rewrite at 0x0 |
| `A fatal error occurred: MD5 of file does not match` | Bad cable / brownout during flash | Shorter cable, powered hub, lower baud |
| Port disappears on S3 when firmware crashes | Native USB-CDC dies with the app | Use the second (UART) port on DevKitC-1, or hold BOOT+RESET to get ROM USB |
| Garbage at 115200 in monitor | Console is 115200 but boot ROM logs at 74880 (classic, 26 MHz xtal clones) | Set monitor to 74880 to read boot messages |

S3 DevKitC-1 has **two USB ports**: "UART" (CH343 bridge — always works for flashing) and "USB" (native USB-OTG — used for USB-CDC console, TinyUSB, JTAG). When generated code sets `ARDUINO_USB_CDC_ON_BOOT=1`, `Serial` goes to the native port; otherwise to UART0.

---

## 7. PSRAM

- Classic ESP32: WROVER modules = 8 MB (4 MB usable as data without himem API), on GPIO 16/17 (those pins become off-limits). WROOM = none.
- S3: module name encodes it — N8R2 = 8 MB flash + 2 MB quad PSRAM; N8R8 / N16R8 = 8 MB **octal** PSRAM (claims GPIO 33–37; also requires `Octal` PSRAM mode in menuconfig/board selection or it's invisible).
- Arduino: Tools → PSRAM → "Enabled" (classic) / "OPI PSRAM" (S3 R8) — wrong setting = `psramFound()` false or boot crash `Octal Flash option selected, but EFUSE not configured`.

```cpp
if (psramFound()) {
  uint8_t *buf = (uint8_t*) ps_malloc(1024 * 1024);   // explicit PSRAM
  // heap_caps_malloc(sz, MALLOC_CAP_SPIRAM) in IDF
}
// With CONFIG_SPIRAM_USE_MALLOC, plain malloc() > threshold goes to PSRAM automatically
```

Constraints: PSRAM is ~4× slower than internal SRAM (cache-mediated); **DMA buffers cannot live in PSRAM** on classic ESP32 (WiFi TX buffers, SPI DMA, I2S audio buffers need `MALLOC_CAP_DMA` internal RAM) — S3 lifts this partially (`MALLOC_CAP_SPIRAM | MALLOC_CAP_DMA` works for some peripherals). Stack cannot be in PSRAM by default. Camera framebuffers (esp32-cam, S3 + OV2640/OV5640) are the canonical PSRAM use: `config.fb_location = CAMERA_FB_IN_PSRAM`.

---

## 8. Working Code Patterns

### 8.1 Differential-drive robot, TB6612FNG, brownout-safe (Arduino C++)

```cpp
// Wiring: VM=battery+, VCC=3V3, GND common. STBY→GPIO27 (has 10k pulldown to GND).
// AIN1=16 AIN2=17 PWMA=18 | BIN1=19 BIN2=21 PWMB=22  — none are strapping pins.
struct Motor { int in1, in2, pwm; };
Motor L{16, 17, 18}, R{19, 21, 22};

void motorInit(const Motor& m) {
  pinMode(m.in1, OUTPUT); pinMode(m.in2, OUTPUT);
  digitalWrite(m.in1, LOW); digitalWrite(m.in2, LOW);
  ledcAttach(m.pwm, 20000, 10);            // 20 kHz silent, 0..1023
  ledcWrite(m.pwm, 0);
}
void motorSet(const Motor& m, int speed) { // -1023..1023
  speed = constrain(speed, -1023, 1023);
  digitalWrite(m.in1, speed > 0); digitalWrite(m.in2, speed < 0);
  ledcWrite(m.pwm, abs(speed));
}
void setup() {
  pinMode(27, OUTPUT); digitalWrite(27, LOW);   // STBY low: driver off during init
  motorInit(L); motorInit(R);
  digitalWrite(27, HIGH);                        // enable only after outputs defined
}
// Soft-start: ramp duty over 100-200 ms instead of step to full — kills inrush brownouts
```

### 8.2 Quadrature encoder via PCNT (don't count edges in an ISR)

```cpp
#include "ESP32Encoder.h"            // madhephaestus/ESP32Encoder — uses PCNT hardware
ESP32Encoder enc;
void setup() {
  ESP32Encoder::useInternalWeakPullResistors = puType::up;
  enc.attachFullQuad(32, 33);        // A, B — classic: 34-39 need EXTERNAL pulls
}
long ticks = enc.getCount();         // glitch-filtered in hardware, zero CPU
```

Classic ESP32 has 8 PCNT units, S3 has 4 → 4 (S3: 2) full-quad encoders in hardware. GPIO-interrupt counting falls apart above ~20 kHz edge rate and steals time from WiFi.

### 8.3 MicroPython: I2C sensor + WiFi + ADC battery, the safe skeleton

```python
import machine, network, time
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400_000)
print(i2c.scan())                    # [] means wiring/pull-up problem — 4.7k to 3V3 required
                                     # external pull-ups mandatory >100kHz or >20cm wires
vbat_adc = machine.ADC(machine.Pin(34), atten=machine.ADC.ATTN_11DB)  # ADC1! WiFi-safe

wlan = network.WLAN(network.STA_IF); wlan.active(True)
wlan.connect("ssid", "pass")
t0 = time.ticks_ms()
while not wlan.isconnected():
    if time.ticks_diff(time.ticks_ms(), t0) > 15_000:
        machine.reset()              # don't loop forever on bad creds
    time.sleep_ms(100)

def vbat_mv():
    s = sorted(vbat_adc.read_uv() for _ in range(5))[2]   # median of 5
    return s // 1000 * 2             # 100k:100k divider
```

### 8.4 Dual-core task split (Arduino/FreeRTOS)

```cpp
// Core 0 runs WiFi/BT stack; pin control loops to Core 1.
TaskHandle_t ctrlTask;
void controlLoop(void*) {
  TickType_t wake = xTaskGetTickCount();
  for (;;) {
    // read sensors, PID, write motors — hard 100 Hz
    vTaskDelayUntil(&wake, pdMS_TO_TICKS(10));   // NOT vTaskDelay — no drift
  }
}
void setup() {
  xTaskCreatePinnedToCore(controlLoop, "ctrl", 4096, nullptr, 5, &ctrlTask, 1);
}
// Never Serial.print() inside a 1 kHz loop; never block Core 0 >~1 s or the WiFi/task WDT fires:
// "Task watchdog got triggered (IDLE0)". Feed with delay(1)/vTaskDelay, not busy-wait.
```

---

## 9. Debugging Checklist (run top to bottom)

1. **Boot loop / instant reset** → read the reset reason in the boot banner:
   - `rst:0x10 (RTCWDT_RTC_RESET)` + `Brownout` → power problem (§4).
   - `flash read err` → flash mode/offset (§6).
   - `Guru Meditation LoadProhibited` → null/uninitialized pointer; decode backtrace with `ESP Exception Decoder` or `xtensa-esp32-elf-addr2line -e firmware.elf <addrs>`.
   - `rst:0x8 (TG1WDT_SYS_RESET)` → task WDT; a loop never yields.
2. **Won't enter download mode** → something on GPIO0/GPIO2 (LED to 3V3 on GPIO2 is enough). Disconnect peripherals from strapping pins.
3. **analogRead returns 0/4095/garbage** → pin on ADC2 with WiFi on? Wrong attenuation for the voltage? Pin actually input-only and you set pinMode OUTPUT elsewhere?
4. **I2C device not found** → `i2c.scan()`; missing 4.7 kΩ pull-ups; sensor is 5 V-only logic (ESP32 is NOT 5 V tolerant — use a level shifter or check sensor has on-board regulator+shifter); SDA/SCL swapped.
5. **Motors twitch at boot** → driver inputs on GPIO 0/2/5/12/15 (boot glitch), or no pull-down on EN/STBY.
6. **WiFi disconnects under load** → shared supply sagging; check with `WiFi.RSSI()` and a scope on 3V3 during TX. Add bulk capacitance; classic ESP32 needs ≥500 mA headroom.
7. **Random crashes only with PSRAM enabled** → DMA buffer landed in PSRAM, or octal/quad mode mismatch (§7).
8. **Deep sleep current too high** → measure at battery, not USB; DevKit bridge/regulator floor (§4.3); floating GPIOs (configure unused pins as inputs with pulls or `rtc_gpio_isolate(GPIO_NUM_12)` — GPIO12 isolation alone saves ~80 µA on WROVER).
9. **Serial prints garbage at boot then works** → 74880-baud ROM log (§6 table); harmless.
10. **It works on USB, fails on battery** → voltage sag under load; scope it or log `analogReadMilliVolts` of the battery divider at fault time.

## 10. Defaults to Generate When Unspecified

- Board: ESP32-DevKitC → I2C on 21/22, UART2 on 16/17, VSPI 18/19/23/5, ADC on 32–36, motor PWM on 25/26/27.
- S3-DevKitC-1: I2C on 8/9, SPI 11/12/13/10, ADC on 1–10, PWM on 4–7, avoid 33–37 and 19/20/43/44/45/46/0/3.
- PWM for motors 20 kHz/10-bit; servos 50 Hz/14-bit.
- All analog on ADC1, calibrated reads, median/mean filtered.
- Strapping pins reserved for buttons (GPIO0) and on-board LED (GPIO2 classic / GPIO48 RGB on S3-DevKitC-1, via `neopixelWrite(48, r, g, b)`).
- Separate motor supply + common ground in every wiring description that includes a motor, servo, solenoid, or relay.
