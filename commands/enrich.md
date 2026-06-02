# /enrich — Contact Enrichment

Maintains the personal CRM at `~/.claude/contacts/`.

## Operations

### `/enrich all`
Scan recent communications across all connected channels (email, WhatsApp, calendar) and update contact files with new interactions, topics discussed, and follow-ups needed.

Steps:
1. Scan last 7 days of connected channels
2. For each contact mentioned or communicated with, find or create their contact file
3. Add new interaction notes with date
4. Flag follow-ups or relationship gaps
5. Report: X contacts updated, Y new contacts created, Z relationships flagged as stale

### `/enrich stale`
Check all contact files against their tier cadence:
- Tier 1: flag if no contact in 14 days
- Tier 2: flag if no contact in 30 days
- Tier 3: flag if no contact in 60 days

Output:
```
STALE RELATIONSHIPS
[name] — Tier [X] — Last contact: [date] ([N days ago])
  → Suggested: [brief touchpoint idea]
```

### `/enrich [name]`
Deep enrichment for a specific contact:
1. Scan all connected channels for mentions of this person
2. Review their contact file
3. Pull latest calendar events featuring them
4. Build: updated profile, recent topics, suggested talking points, any follow-ups
5. Ideal for meeting prep

## Contact File Template

`~/.claude/contacts/[firstname-lastname].md`

```markdown
# [Full Name]

## Quick Reference
- **Company:** [company]
- **Role:** [title]
- **Relationship Tier:** [1/2/3]
- **Contact cadence:** [every X days]
- **Email:** [email]
- **Phone/WhatsApp:** [number]

## Relationship Context
[How you know them, why they matter, what you've built together]

## Communication Style
[How they communicate — direct/formal/informal, response speed, preferences]

## Interaction History
- [YYYY-MM-DD] [brief note on conversation/meeting]
- [YYYY-MM-DD] [...]

## Talking Points & Interests
- [interest/topic] (added [date])
- [...]

## Follow-ups
- [ ] [follow-up item] — by [date]
```

## Guardrails

- Practical notes only — no speculation, no judgment
- Assign tiers based on actual importance, not aspiration
- Stale alerts are suggestions, not obligations
- Always include dates on added notes
- Privacy: don't expose contact details across channels without cause
