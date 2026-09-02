---
name: calendar-assistant
description: Plan and modify calendar events with timezone checks, conflict detection, and confirmation.
category: communication
aliases: [calendar, schedule, event, google-calendar, outlook]
triggers:
  - Schedule this meeting
  - Add to my calendar
  - What's on my calendar
  - Find a time for
  - Check for conflicts
keywords: [calendar, schedule, meeting, event, time, timezone]
required_tools: [calendar-access]
risk: medium
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

# Calendar Assistant

## Purpose

Plan, modify, and query calendar events with proper timezone handling, conflict
detection, and explicit user confirmation for all changes. The skill helps users
manage their time effectively without overbooking or scheduling conflicts.

## When to Use

- Scheduling a new meeting or event
- Checking availability before committing
- Finding time slots for a proposed meeting
- Querying upcoming events

## When NOT to Use

- Real-time calendar monitoring (use notifications)
- Automatic scheduling without user approval
- Accessing shared calendars without authorization

## Capabilities

- List upcoming events (today, this week, custom range)
- Create events with title, time, duration, location, attendees
- Update event details
- Cancel or delete events
- Find available time slots
- Conflict detection and alerts
- Timezone conversion and display
- Recurring event support

## Inputs

- `action` (required) â€” one of: list, create, update, delete, find-time
- `event_details` (required for create/update) â€” title, time, duration, etc.
- `range` (optional for list) â€” today, this-week, custom dates
- `attendees` (optional) â€” list of participant emails

## Workflow

1. **Query** â€” Fetch current calendar state
2. **Check** â€” Detect conflicts, show availability
3. **Draft** â€” Prepare event details for user review
4. **Confirm** â€” Wait for explicit approval
5. **Execute** â€” Create/update/delete event
6. **Notify** â€” Confirm action taken

## Tools

- Calendar API (Google Calendar, Outlook, or CalDAV)
- Timezone library

## Examples

**User:** "Find time for a 1-hour meeting with alice@example.com tomorrow"
**Response:**
```
Available slots tomorrow (Feb 10):
- 10:00-11:00 AM âœ“ (Alice available)
- 2:00-3:00 PM âš ï¸ (You have 'Lunch' 1-2pm)
- 4:00-5:00 PM âœ“

Select a slot or I'll propose 10:00 AM.
```

## Safety

- ALWAYS require confirmation before creating/modifying events
- Never auto-schedule meetings
- Verify attendee availability before booking
- Warn about double-booking
- Respect calendar access permissions
- Include timezone information in all responses

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `time-blocking` (deep work scheduling)
- `meeting-action-extractor` (extract follow-ups)
- `focus-guard` (protect scheduled focus time)
