# Universal Skill Catalog

Exhaustive index of all 27 voice & multimodal capability categories, verified upstream repositories, and built-in native skill implementations.

---

## 1. Upstream Ecosystem Provenance

### A. Curated Official Catalog Manager
- **Repository**: [OpenVoiceOS/ovos-skill-manager](https://github.com/OpenVoiceOS/ovos-skill-manager)
- **Manifest Source**: [OpenVoiceOS/ovos-skills-manager](https://github.com/OpenVoiceOS/ovos-skills-manager)
- **Sync Tool**: [`scripts/sync_osm_skills.py`](file:///scripts/sync_osm_skills.py)

### B. Verified OpenVoiceOS Upstream Repositories (39 Active)
| Repository | Description | Status |
| :--- | :--- | :---: |
| `OpenVoiceOS/skill-ovos-weather` | Meteorological forecasts, conditions, and alerts | Active |
| `OpenVoiceOS/skill-ovos-wikipedia` | Wikipedia encyclopedic voice lookup | Active |
| `OpenVoiceOS/skill-ovos-wolfram-alpha` | Computational mathematics and knowledge engine | Active |
| `OpenVoiceOS/skill-ovos-ddg` | DuckDuckGo zero-click web search | Active |
| `OpenVoiceOS/skill-ovos-timer` | Multi-timer management and countdowns | Active |
| `OpenVoiceOS/skill-ovos-alarm` | Recurring and one-off alarm clock | Active |
| `OpenVoiceOS/skill-ovos-notes` | Spoken note taking and memory items | Active |
| `OpenVoiceOS/skill-ovos-news` | Audio news stream briefings | Active |
| `OpenVoiceOS/skill-ovos-volume` | Master system volume and mute controls | Active |
| `OpenVoiceOS/skill-ovos-date-time` | Current time, date, and timezone lookup | Active |
| `OpenVoiceOS/skill-ovos-hello-world` | Framework onboarding and introductory skill | Active |
| `OpenVoiceOS/skill-ovos-stop` | Global halt/stop handler for all audio and tasks | Active |
| `OpenVoiceOS/skill-ovos-fallback-unknown` | Unhandled intent fallback and LLM dispatch | Active |
| `OpenVoiceOS/skill-ovos-fallback-chatgpt` | ChatGPT question-answering fallback | Active |
| `OpenVoiceOS/skill-ovos-setup` | Initial voice onboarding and setup assistant | Active |
| `OpenVoiceOS/skill-ovos-wifi-setup` | Captive portal and Wi-Fi provisioning | Active |
| `OpenVoiceOS/skill-ovos-homeassistant` | Home Assistant bridge for entities and automations | Active |
| `OpenVoiceOS/skill-ovos-media` | OpenVoiceOS Common Play media framework | Active |
| `OpenVoiceOS/skill-ovos-sunrise-sunset` | Solar astronomical calculations | Active |
| `OpenVoiceOS/skill-ovos-youtube` | YouTube audio and video playback | Active |
| `OpenVoiceOS/skill-ovos-spotify` | Spotify streaming integration | Active |
| `OpenVoiceOS/skill-ovos-bandcamp` | Bandcamp independent music streaming | Active |
| `OpenVoiceOS/skill-ovos-soundcloud` | SoundCloud artist search and stream | Active |
| `OpenVoiceOS/skill-ovos-radio-browser` | 30,000+ internet radio station browser | Active |
| `OpenVoiceOS/skill-ovos-podcasts` | Podcast RSS feed and episode player | Active |
| `OpenVoiceOS/skill-ovos-iss-location` | International Space Station tracking | Active |
| `OpenVoiceOS/skill-ovos-number-facts` | Interesting numerical and mathematical trivia | Active |
| `OpenVoiceOS/skill-ovos-wordnet` | WordNet dictionary and lexical taxonomy | Active |
| `OpenVoiceOS/skill-ovos-dictation` | Speech-to-text dictation into text files | Active |
| `OpenVoiceOS/skill-ovos-calculator` | Real-time voice arithmetic and unit math | Active |
| `OpenVoiceOS/skill-ovos-translation` | Multi-language translation engine | Active |
| `OpenVoiceOS/skill-ovos-personal` | User preferences and personalization | Active |
| `OpenVoiceOS/skill-ovos-camera` | Web camera snapshot and vision capture | Active |
| `OpenVoiceOS/skill-ovos-laugh` | Conversational humor and chuckles | Active |
| `OpenVoiceOS/skill-ovos-parrot` | Echo and vocal parrot mode | Active |
| `OpenVoiceOS/skill-ovos-speedtest` | Network bandwidth and latency diagnostic | Active |
| `OpenVoiceOS/skill-ovos-icanhazdadjokes` | Dad jokes repository integration | Active |
| `OpenVoiceOS/skill-ovos-naptime` | Low-power sleep and standby mode | Active |
| `OpenVoiceOS/skill-ovos-boot-finished` | Startup chime and system readiness notification | Active |

### C. Verified NeonGecko Upstream Repositories (28 Active)
| Repository | Description | Status |
| :--- | :--- | :---: |
| `NeonGeckoCom/skill-alerts` | Audio and visual notifications | Active |
| `NeonGeckoCom/skill-weather` | Multi-provider weather forecasting | Active |
| `NeonGeckoCom/skill-date_time` | Clock, world time, and calendar | Active |
| `NeonGeckoCom/skill-calendar` | Google and CalDAV calendar sync | Active |
| `NeonGeckoCom/skill-reminder` | Natural language reminders | Active |
| `NeonGeckoCom/skill-translation` | Real-time conversational translation | Active |
| `NeonGeckoCom/skill-fallback-chatgpt` | OpenAI conversation fallback | Active |
| `NeonGeckoCom/skill-duckduckgo` | Privacy search integration | Active |
| `NeonGeckoCom/skill-wikipedia` | Wikipedia knowledge extraction | Active |
| `NeonGeckoCom/skill-wolfram-alpha` | Computational knowledge retrieval | Active |
| `NeonGeckoCom/skill-local_media` | Local filesystem media player | Active |
| `NeonGeckoCom/skill-messaging` | SMS and chat messaging | Active |
| `NeonGeckoCom/skill-converse` | Multi-turn conversational flow | Active |
| `NeonGeckoCom/skill-about` | Device hardware and version query | Active |
| `NeonGeckoCom/skill-device_controls` | System hardware brightness/volume | Active |
| `NeonGeckoCom/skill-iss` | Orbital position calculations | Active |
| `NeonGeckoCom/skill-somafm` | SomaFM commercial-free radio | Active |
| `NeonGeckoCom/skill-casual_conversation` | Small talk dialog generator | Active |
| `NeonGeckoCom/skill-fallback_llm` | Local and remote LLM fallback | Active |
| `NeonGeckoCom/skill-stock` | Stock ticker lookup | Active |
| `NeonGeckoCom/skill-crypto` | Cryptocurrency rates and volume | Active |
| `NeonGeckoCom/skill-npr_news` | NPR hourly radio newscast | Active |
| `NeonGeckoCom/skill-reddit` | Reddit thread parser and reader | Active |
| `NeonGeckoCom/skill-homescreen` | Touchscreen GUI home interface | Active |
| `NeonGeckoCom/skill-audio_record` | Voice memo audio recorder | Active |
| `NeonGeckoCom/skill-voice_ping` | Intercom voice paging | Active |
| `NeonGeckoCom/skill-demo` | Interactive feature showcase | Active |

### D. Archived Mycroft Reference Repositories (22 References)
Archived upstream reference codebases (Mycroft AI 2015-2023) maintained for compatibility and adaptation:
`MycroftAI/skill-weather`, `skill-wiki`, `skill-volume`, `skill-alarm`, `skill-timer`, `skill-reminder`, `skill-date-time`, `skill-npr-news`, `skill-hello-world`, `skill-stop`, `skill-pairing`, `skill-configuration`, `skill-installer`, `skill-ip`, `skill-spelling`, `skill-singing`, `skill-joke`, `skill-audio-record`, `skill-playback-control`, `skill-mark-1-demo`, `mycroft-core`, `mycroft-skills`.

---

## 2. Built-in Native Skill Categories (27 Categories, 405 Packages)

All native packages under `skills/<category>/<skill-id>/` feature complete `__init__.py`, `skill.py`, `manifest.yml`, `requirements.txt`, `README.md`, and `locale/en-us/` intents/vocab/dialog.

1. **`communication`** (Tier 3): `skill-email`, `skill-sms`, `skill-phone-call`, `skill-video-call`, `skill-slack`, `skill-discord`, `skill-telegram`, `skill-whatsapp`, `skill-signal`, `skill-irc`, `skill-matrix`, `skill-twitter`, `skill-facebook`, `skill-instagram`, `skill-linkedin`, `skill-reddit`, `skill-mastodon`, `skill-contacts`, `skill-intercom`, `skill-notifications`.
2. **`media`** (Tier 2): `skill-music-player`, `skill-spotify`, `skill-youtube`, `skill-youtube-music`, `skill-soundcloud`, `skill-bandcamp`, `skill-tidal`, `skill-deezer`, `skill-pandora`, `skill-apple-music`, `skill-local-music`, `skill-podcasts`, `skill-audiobooks`, `skill-radio`, `skill-internet-radio`, `skill-video-player`, `skill-netflix`, `skill-plex`, `skill-kodi`, `skill-jellyfin`, `skill-emby`, `skill-photo-viewer`, `skill-slideshow`, `skill-screen-cast`, `skill-ambient-sounds`, `skill-white-noise`, `skill-sound-effects`, `skill-karaoke`, `skill-metronome`, `skill-tuner`, `skill-media-queue`, `skill-playlist`.
3. **`entertainment`** (Tier 5): `skill-jokes`, `skill-trivia`, `skill-stories`, `skill-twenty-questions`, `skill-rock-paper-scissors`, `skill-tic-tac-toe`, `skill-chess`, `skill-hangman`, `skill-word-games`, `skill-number-games`, `skill-adventure-game`, `skill-dice-roller`, `skill-card-games`, `skill-dnd`, `skill-riddles`, `skill-tongue-twisters`, `skill-mad-libs`, `skill-would-you-rather`, `skill-truth-or-dare`, `skill-movie-info`, `skill-tv-tracker`, `skill-book-recommendations`, `skill-movie-recommendations`, `skill-celebrity-info`, `skill-lyrics`, `skill-guitar-chords`, `skill-meme-generator`.
4. **`information`** (Tier 3): `skill-wikipedia`, `skill-wolfram-alpha`, `skill-duckduckgo`, `skill-google-search`, `skill-dictionary`, `skill-thesaurus`, `skill-spelling`, `skill-grammar`, `skill-etymology`, `skill-quotes`, `skill-proverbs`, `skill-facts`, `skill-this-day-in-history`, `skill-biography`, `skill-country-info`, `skill-city-info`, `skill-calculator`, `skill-unit-converter`, `skill-number-converter`, `skill-periodic-table`, `skill-planet-info`, `skill-animal-info`, `skill-plant-info`, `skill-nutrition`, `skill-recipes`, `skill-medical-info`, `skill-how-to`, `skill-product-info`, `skill-price-comparison`, `skill-color-info`, `skill-emoji-lookup`, `skill-formula-reference`.
5. **`smart_home`** (Tier 3): `skill-home-assistant`, `skill-openhab`, `skill-smartthings`, `skill-hubitat`, `skill-domoticz`, `skill-lights`, `skill-thermostat`, `skill-locks`, `skill-garage`, `skill-blinds`, `skill-fans`, `skill-plugs`, `skill-cameras`, `skill-doorbell`, `skill-sensors`, `skill-security-system`, `skill-sprinkler`, `skill-robot-vacuum`, `skill-sonos`, `skill-philips-hue`, `skill-lifx`, `skill-wink`, `skill-nest`, `skill-ecobee`, `skill-ring`, `skill-arlo`, `skill-wyze`, `skill-tuya`, `skill-mqtt`, `skill-zigbee`, `skill-zwave`, `skill-matter`, `skill-node-red`, `skill-ifttt`, `skill-scenes`, `skill-routines`, `skill-energy-monitor`.
6. **`productivity`** (Tier 2): `skill-calendar`, `skill-google-calendar`, `skill-outlook-calendar`, `skill-todo-list`, `skill-todoist`, `skill-reminders`, `skill-alarms`, `skill-timers`, `skill-stopwatch`, `skill-pomodoro`, `skill-notes`, `skill-voice-memo`, `skill-dictation`, `skill-transcription`, `skill-meetings`, `skill-project-management`, `skill-habit-tracker`, `skill-time-tracker`, `skill-expense-tracker`, `skill-budget`, `skill-file-manager`, `skill-cloud-storage`, `skill-documents`, `skill-pdf`, `skill-printing`, `skill-clipboard`, `skill-automation`.
7. **`navigation`** (Tier 3): `skill-directions`, `skill-traffic`, `skill-nearby-places`, `skill-restaurant-finder`, `skill-hotel-finder`, `skill-flight-tracker`, `skill-uber`, `skill-lyft`, `skill-parking`, `skill-ev-charging`, `skill-gas-prices`, `skill-public-transit`, `skill-travel-info`, `skill-timezone`, `skill-sunrise-sunset`, `skill-tides`, `skill-road-conditions`.
8. **`weather`** (Tier 3): `skill-weather`, `skill-weather-forecast`, `skill-severe-weather`, `skill-air-quality`, `skill-pollen`, `skill-uv-index`, `skill-moon-phase`, `skill-astronomy-events`, `skill-earthquake`, `skill-wildfire`, `skill-marine-forecast`.
9. **`health`** (Tier 4): `skill-fitness-tracker`, `skill-workout`, `skill-exercise`, `skill-calorie-counter`, `skill-water-tracker`, `skill-weight-tracker`, `skill-medication-reminder`, `skill-symptom-checker`, `skill-first-aid`, `skill-meditation`, `skill-breathing`, `skill-sleep`, `skill-mood-tracker`, `skill-mental-health`, `skill-bmi-calculator`, `skill-fitbit`, `skill-google-fit`, `skill-apple-health`.
10. **`finance`** (Tier 4): `skill-stocks`, `skill-crypto`, `skill-forex`, `skill-commodities`, `skill-portfolio`, `skill-market-news`, `skill-currency-converter`, `skill-mortgage-calculator`, `skill-loan-calculator`, `skill-tip-calculator`, `skill-tax-calculator`, `skill-retirement-calculator`, `skill-bill-splitter`, `skill-economic-indicators`, `skill-financial-news`.
11. **`education`** (Tier 4): `skill-flashcards`, `skill-language-learning`, `skill-translator`, `skill-math-tutor`, `skill-science-tutor`, `skill-history-tutor`, `skill-geography-quiz`, `skill-coding-tutorial`, `skill-typing-tutor`, `skill-speed-reading`, `skill-memory-games`, `skill-brain-teasers`, `skill-study-timer`, `skill-citation-generator`, `skill-gpa-calculator`, `skill-career-guidance`.
12. **`news`** (Tier 3): `skill-news`, `skill-news-briefing`, `skill-bbc-news`, `skill-cnn`, `skill-reuters`, `skill-npr`, `skill-hacker-news`, `skill-rss-reader`, `skill-sports-scores`, `skill-sports-schedules`, `skill-election-tracker`, `skill-tech-news`, `skill-science-news`, `skill-reddit`.
13. **`shopping`** (Tier 4): `skill-shopping-list`, `skill-grocery-list`, `skill-price-lookup`, `skill-price-comparison`, `skill-deal-finder`, `skill-order-tracker`, `skill-wishlist`, `skill-meal-planner`, `skill-barcode-scanner`, `skill-store-finder`.
14. **`system`** (Tier 0 & Tier 1): `skill-volume`, `skill-brightness`, `skill-wifi`, `skill-bluetooth`, `skill-battery`, `skill-storage`, `skill-screen`, `skill-power`, `skill-updates`, `skill-apps`, `skill-settings`, `skill-accessibility`, `skill-diagnostics`, `skill-speed-test`, `skill-network`, `skill-process-manager`, `skill-file-transfer`, `skill-remote-desktop`, `skill-wake-on-lan`, `skill-ssh`, `skill-docker`.
15. **`creative`** (Tier 5): `skill-chatgpt`, `skill-claude`, `skill-llama`, `skill-stable-diffusion`, `skill-dalle`, `skill-ai-music`, `skill-ai-video`, `skill-creative-writing`, `skill-poetry`, `skill-songwriting`, `skill-name-generator`, `skill-color-palette`, `skill-rhyme`, `skill-anagram`, `skill-crossword`, `skill-sudoku`, `skill-craft-ideas`, `skill-diy-projects`.
16. **`automotive`** (Tier 6): `skill-obd-diagnostics`, `skill-tesla`, `skill-ev-charging`, `skill-vehicle-remote`, `skill-fuel-tracker`, `skill-maintenance`, `skill-dashcam`, `skill-car-finder`, `skill-roadside-assistance`, `skill-vehicle-valuation`.
17. **`security`** (Tier 2): `skill-password-generator`, `skill-2fa`, `skill-breach-check`, `skill-vpn`, `skill-security-audit`, `skill-privacy`, `skill-encrypted-notes`, `skill-network-security`.
18. **`science`** (Tier 4): `skill-scientific-calculator`, `skill-statistics`, `skill-chemistry`, `skill-physics`, `skill-biology`, `skill-astronomy`, `skill-iss-tracker`, `skill-space-launches`, `skill-nasa`, `skill-arxiv`, `skill-pubmed`, `skill-carbon-footprint`, `skill-lab-tools`.
19. **`cooking`** (Tier 4): `skill-recipe-search`, `skill-recipe-reader`, `skill-cooking-timer`, `skill-cooking-conversion`, `skill-substitutions`, `skill-meal-planner`, `skill-wine-pairing`, `skill-cocktails`, `skill-coffee-guide`, `skill-food-safety`, `skill-pantry`, `skill-food-delivery`.
20. **`social`** (Tier 5): `skill-birthday-reminder`, `skill-anniversary`, `skill-date-ideas`, `skill-gift-ideas`, `skill-compliment`, `skill-ice-breakers`, `skill-personality-test`, `skill-party-planner`, `skill-baby-names`, `skill-pet-care`, `skill-volunteer`, `skill-charity`.
21. **`emergency`** (Tier 0): `skill-emergency-call`, `skill-first-aid`, `skill-cpr`, `skill-emergency-contacts`, `skill-medical-id`, `skill-hospital-finder`, `skill-pharmacy-finder`, `skill-disaster-prep`, `skill-evacuation`, `skill-survival`, `skill-amber-alert`, `skill-emergency-translation`.
22. **`legal`** (Tier 6): `skill-legal-definitions`, `skill-rights-info`, `skill-lawyer-finder`, `skill-court-dates`, `skill-patent-search`, `skill-compliance`.
23. **`agriculture`** (Tier 6): `skill-crop-planner`, `skill-planting-calendar`, `skill-pest-management`, `skill-soil-info`, `skill-livestock`, `skill-farm-weather`.
24. **`developer`** (Tier 3): `skill-code-runner`, `skill-code-explain`, `skill-github`, `skill-stack-overflow`, `skill-server-status`, `skill-ci-cd`, `skill-cloud-management`, `skill-database`, `skill-api-tester`, `skill-regex`, `skill-json-tools`, `skill-git`, `skill-dependency-check`.
25. **`accessibility`** (Tier 1): `skill-screen-reader`, `skill-magnification`, `skill-high-contrast`, `skill-color-blind`, `skill-dyslexia`, `skill-cognitive`, `skill-motor`, `skill-hearing`, `skill-visual`, `skill-speech`, `skill-sign-language`.
26. **`fun`** (Tier 5): `skill-coin-flip`, `skill-dice`, `skill-magic-8-ball`, `skill-fortune-cookie`, `skill-horoscope`, `skill-tarot`, `skill-decision-maker`, `skill-random-generator`, `skill-fun-facts`, `skill-word-of-the-day`, `skill-quote-of-the-day`, `skill-motivation`, `skill-affirmation`, `skill-gratitude`, `skill-dream-journal`, `skill-bucket-list`.
27. **`fallback`** (Tier 0): `skill-fallback-unknown`, `skill-fallback-chatgpt`, `skill-fallback-wolfram`, `skill-fallback-duckduckgo`, `skill-fallback-wikipedia`, `skill-fallback-web-search`.
