# /prep — Meeting Preparation

Prepares a concise brief for any upcoming meeting.

## Usage

`/prep [meeting name or person]` or just `/prep` to prep for the next calendar event.

## Steps

1. **Identify the meeting** — pull from calendar or use provided context
2. **Check contact files** — read `~/.claude/contacts/[person].md` for each attendee
3. **Scan recent comms** — any email or message threads with attendees in last 30 days
4. **Check goal alignment** — which OBJ does this meeting advance? If none, flag it.
5. **Build the brief**

## Output Format

```
MEETING PREP — [Meeting Name]
[Date] [Time] | [Duration] | [Attendees]

GOAL ALIGNMENT: [Which OBJ? If none — flag]

CONTEXT
[2-3 sentences on relationship history and why this meeting matters]

AGENDA / OUTCOMES
→ [What you want to get out of this meeting — be specific]
→ [Any decisions to make or close]

THEIR LIKELY PRIORITIES
→ [What they care about going in]
→ [Any asks they might make of you]

TALKING POINTS
• [Key point to land]
• [...]

WATCH-OUTS
• [Anything sensitive, tricky, or to avoid]

FOLLOW-UP PREP
→ [Draft any follow-up email in advance? Y/N]
```

## Guardrails

- Keep it to one screen — brief, not exhaustive
- If no contact file exists, ask if you should create one after the meeting
- Always state goal alignment (or lack thereof)
