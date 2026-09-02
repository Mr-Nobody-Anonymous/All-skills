---
name: system-monitor
description: Inspect system telemetry and summarize CPU, memory, disk, process, and network anomalies.
category: media_and_utilities
aliases: [system, monitor, telemetry, metrics, server, performance]
triggers:
  - Check system status
  - System health
  - Server metrics
  - CPU usage
  - Memory check
keywords: [system, monitor, cpu, memory, disk, network, metrics, telemetry]
required_tools: [system-tools]
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

# System Telemetry Monitor

## Purpose

Inspect system telemetry and provide clear summaries of CPU usage, memory allocation,
disk space, running processes, and network activity. The skill highlights anomalies
and helps diagnose performance issues.

## When to Use

- Checking system health and resource usage
- Diagnosing performance problems
- Monitoring server or workstation status
- Investigating resource bottlenecks

## When NOT to Use

- Real-time continuous monitoring (use dedicated monitoring tools)
- Accessing systems without authorization
- Automated remediation without human approval

## Capabilities

- CPU usage and load average
- Memory utilization and swap
- Disk space and I/O statistics
- Running processes (top consumers)
- Network connections and throughput
- Temperature and hardware sensors (where available)
- Anomaly detection and alerting
- Historical trend analysis (if data available)

## Inputs

- `target` (optional) â€” system hostname or local (default: local)
- `scope` (optional) â€” all, cpu, memory, disk, network, processes
- `timeframe` (optional) â€” current, last-hour, last-day
- `alert_threshold` (optional) â€” custom alert levels

## Workflow

1. **Connect** â€” Establish access to target system
2. **Collect** â€” Gather telemetry data
3. **Analyze** â€” Compare against baselines, detect anomalies
4. **Summarize** â€” Present findings in clear format
5. **Alert** â€” Flag any critical issues
6. **Recommend** â€” Suggest investigation steps if needed

## Tools

- System utilities (top, htop, ps, df, netstat, etc.)
- Platform-specific tools (Windows Task Manager equivalent, Linux sysstat)

## Examples

**User:** "Check system health"
**Response:**
```
System Status: Healthy

CPU: 34% utilized (normal)
Memory: 67% used, 4.2GB available
Disk: 45% used (120GB / 256GB)
  - /home: 78% (warning)
  - /var: 52%
Network: Normal activity

Anomalies:
âš ï¸ /home partition above 75% threshold
âœ“ No other issues detected
```

## Safety

- Only access systems with proper authorization
- Never store sensitive system data beyond the session
- Use read-only commands by default
- Confirm before any system modifications

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `docker-manager` (container resource monitoring)
- `db-inspector` (database performance)
- `cmd-safety-check` (before running system commands)
