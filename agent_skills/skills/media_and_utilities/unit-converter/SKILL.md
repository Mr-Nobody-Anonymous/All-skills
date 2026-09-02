---
name: unit-converter
description: Convert units and currencies while showing assumptions, precision, and exchange-rate timestamps.
category: media_and_utilities
aliases: [convert, units, currency, conversion, calculator]
triggers:
  - Convert units
  - Currency conversion
  - How many miles in a km
  - Convert this measurement
keywords: [convert, units, currency, measurement, exchange, rate]
required_tools: [exchange-rate-source]
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

# Unit & Currency Converter

## Purpose

Convert between units of measurement and currencies with full transparency on
assumptions, precision levels, and data freshness. The skill ensures accurate
conversions with appropriate uncertainty indicators.

## When to Use

- Converting between metric and imperial units
- Currency conversion for international context
- Scientific or engineering unit transformations
- Recipe or measurement conversions

## When NOT to Use

- For financial transactions (use official exchange services)
- For precise engineering calculations (use specialized tools)
- For legal or compliance measurements

## Capabilities

- Length, weight, temperature, volume conversions
- Currency conversion with live rates
- Area, speed, pressure, energy conversions
- Time zone conversions
- Data size and bandwidth conversions
- Precision control
- Batch conversions
- Common unit shortcuts

## Inputs

- `value` (required) â€” number to convert
- `from_unit` (required) â€” source unit
- `to_unit` (required) â€” target unit
- `precision` (optional) â€” decimal places (default: auto)
- `source` (optional) â€” for currency rates

## Workflow

1. **Parse** â€” Extract value and units from input
2. **Resolve** â€” Map units to standard definitions
3. **Convert** â€” Apply conversion factor
4. **Format** â€” Present with appropriate precision
5. **Document** â€” Show assumptions and data source

## Tools

- Conversion tables (built-in)
- Exchange rate API (for currency)

## Examples

**User:** "Convert 100 euros to dollars"
**Response:**
```
100.00 EUR =
  107.85 USD

Rate: 1 EUR = 1.0785 USD
Source: Exchange Rate API
Timestamp: 2026-02-09T10:00 UTC
Rate age: 2 hours
```

**User:** "How many kilometers is 50 miles?"
**Response:**
```
50 miles = 80.47 kilometers

Precision: 2 decimal places
Conversion factor: 1 mile = 1.60934 km
```

## Safety

- Always indicate data source and timestamp for currency
- Show confidence levels for conversions
- Flag unusual or suspicious conversion requests
- Use official exchange rates for financial context

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `expense-parser` (currency in expense reports)
- `context-summarize` (include conversions in summaries)
- `weather-now` (temperature units)
