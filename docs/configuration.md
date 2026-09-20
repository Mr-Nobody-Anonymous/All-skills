# Platform Configuration

Configuration files reside under the [`config/`](file:///config/) directory.

---

## 1. API Keys & External Services

Copy the template to create your local credentials file:

```bash
cp config/api_keys.yml.template config/api_keys.yml
```

Configure external service credentials as needed:
- **Weather**: OpenWeatherMap API key
- **Knowledge & Math**: Wolfram Alpha App ID
- **AI Models**: OpenAI API key, Anthropic API key
- **Cloud & Voice**: Google Cloud, Microsoft Azure, ElevenLabs
- **Smart Home**: Home Assistant URL and long-lived access token
- **Media**: Spotify Client ID and Secret

---

## 2. Priority & Scheduling Configuration

Priority tiers and execution limits are governed by [`config/priority_config.yml`](file:///config/priority_config.yml):

| Tier | Name | Latency Target | Description |
| :--- | :--- | :--- | :--- |
| **0** | `CRITICAL_SYSTEM` | 10 ms | Core OS routines, volume, halt, safe emergency fallback |
| **1** | `ESSENTIAL_REALTIME` | 50 ms | Clock, timer, alarm, immediate offline intents |
| **2** | `HIGH_PRODUCTIVITY` | 200 ms | Calendar, reminders, fast calculations, media control |
| **3** | `MEDIUM_CONNECTED` | 800 ms | Weather, news, smart home, navigation queries |
| **4** | `STANDARD_COMPLEX` | 2,500 ms | Finance, health, science, research, recipe search |
| **5** | `LOW_ENTERTAINMENT` | 5,000 ms | Games, jokes, creative generation, social prompts |
| **6** | `LAZY_ON_DEMAND` | On-demand | Heavy domain packages (legal, agriculture, OBD-II) |

---

## 3. Core Engine Configuration

[`config/default_config.yml`](file:///config/default_config.yml) defines default STT, TTS, wakeword, and audio pipeline plugins:

```yaml
system:
  name: "All-Skills Universal OS"
  default_locale: "en-us"
  stt_engine: "vosk"        # Options: vosk, whisper, deepgram
  tts_engine: "piper"       # Options: piper, mimic3, espeakng, elevenlabs
  wake_word: "openwakeword" # Options: openwakeword, precise, vosk
```

---

## 4. Logging Configuration

Logging levels and rotations are managed in [`config/logging_config.yml`](file:///config/logging_config.yml). Logs are emitted to `data/logs/system_logs/` and `data/logs/skill_logs/`.
