# /gm — Morning Briefing

Run this every morning to orient the day. Pulls everything together into one screen.

## Steps

1. **Get current date/time** — use Google Calendar or system time to anchor the briefing

2. **Calendar scan** — pull today's events:
   - List all meetings with time, attendees, and purpose
   - Flag back-to-back meetings with no buffer
   - Flag meetings with no stated agenda
   - Identify any prep needed (is there a contact file? recent email thread?)

3. **Task review** — read `~/.claude/my-tasks.yaml`:
   - Surface: overdue tasks, due today, due this week
   - Flag anything at risk
   - Identify the single most important task to complete today

4. **Goal alignment check** — read `~/.claude/goals.yaml`:
   - Which OBJ has had no progress this week?
   - Is today's calendar aligned to top priorities?
   - Surface misalignments plainly

5. **Inbox scan** (if Gmail connected):
   - Tier 1 messages only — anything that needs a response today
   - Flag anything from investors, customers, or key partners

## Output Format

Keep it to one screen. Lead with what's critical.

```
GOOD MORNING — [DATE]

CALENDAR TODAY
[time] [event] — [prep needed? Y/N]
[time] [event] — [note]
⚠️  [flag any issues]

TOP TASK TODAY
→ [single most important task]

GOAL HEALTH
✅ OBJ-1: [status]
⚠️  OBJ-2: [no progress this week — flag]
✅ OBJ-3: [status]

INBOX (Tier 1 only)
→ [from] — [subject] — [action needed]

FOCUS RECOMMENDATION
[1-2 sentences on where to put energy today and why]
```

## Behavior Notes

- If calendar is not connected, say so and skip that section
- If no Tier 1 emails, say "Inbox clear"
- Always end with a focus recommendation — don't leave it open-ended
- If a meeting has no goal alignment, flag it
