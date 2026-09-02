---
name: weather-now
description: Retrieve current weather and local conditions with location, timestamp, and source clarity.
category: media_and_utilities
aliases: [weather, forecast, temperature, conditions]
triggers:
  - What's the weather
  - Weather forecast
  - Current conditions
  - Temperature
keywords: [weather, forecast, temperature, conditions, location]
required_tools: [weather-api]
risk: low
version: 1.0.0
source: openclawskills.net
enabled: true
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: null
---

# Weather & Local Info

## Purpose

Retrieve current weather conditions and forecasts with clear location identification,
timestamps, and data source attribution. The skill provides accurate weather information
for planning and decision-making.

## When to Use

- User asks about current weather or forecast
- Weather affects planned activities
- Including weather in summaries or reports

## When NOT to Use

- For critical decisions (aviation, emergency services)
- When precise instruments are required
- For historical weather data (use specialized services)

## Capabilities

- Current conditions (temperature, humidity, wind, precipitation)
- Hourly and daily forecasts
- Severe weather alerts
- Multiple location support
- Unit conversion (Celsius/Fahrenheit)
- Data source attribution
- Cache management for rate limits

## Inputs

- `location` (required) â€” city name, coordinates, or location ID
- `units` (optional) â€” metric or imperial
- `forecast` (optional) â€” current, hourly, daily, extended
- `include_alerts` (optional, default: true) â€” include severe weather

## Workflow

1. **Resolve** â€” Convert location to coordinates
2. **Fetch** â€” Query weather API
3. **Format** â€” Present in clear, readable format
4. **Attribute** â€” Include source and timestamp
5. **Cache** â€” Store for repeated queries

## Tools

- Weather API (OpenWeatherMap, WeatherAPI, etc.)
- Geocoding service

## Examples

**User:** "What's the weather in San Francisco?"
**Response:**
```
San Francisco, CA
Updated: Feb 9, 2026 at 10:30 AM PST
Source: OpenWeatherMap

Current: 58Â°F (14Â°C), Partly Cloudy
Humidity: 72%
Wind: 8 mph NW
Visibility: 10 miles

Today's Forecast:
- Morning: 54Â°F, Clear
- Afternoon: 62Â°F, Partly Cloudy
- Evening: 55Â°F, Clear

No severe weather alerts.
```

## Safety

- Always include data freshness timestamp
- Attribute data source
- Flag low-confidence forecasts
- Don't use for critical safety decisions

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `calendar-assistant` (weather in event planning)
- `context-summarize` (include weather in summaries)
- `time-blocking` (weather-aware scheduling)
