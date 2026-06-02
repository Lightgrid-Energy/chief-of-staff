# /triage — Inbox Triage

Processes all connected inboxes and produces send-ready drafts for approval.

## Steps

1. **Establish context** — get current time, note what was already triaged this session to avoid re-surfacing

2. **Scan connected channels** (only query what's connected):
   - Gmail — direct messages only, skip newsletters/automated
   - WhatsApp — personal and business threads
   - Slack — direct messages and @mentions (skip general channels unless flagged)
   - Any other connected inbox

3. **Classify each item**:
   - **Tier 1:** Respond NOW — from investor/customer/key partner, time-sensitive, blocking someone
   - **Tier 2:** Handle today — important but not urgent
   - **Tier 3:** Archive — newsletter, notification, FYI

4. **Draft responses** for Tier 1 and 2:
   - Match Mujtaba's voice (direct, short, founder-authentic)
   - Check calendar before any scheduling-related reply
   - Never propose a meeting time without verifying availability first

5. **Present for approval** — show drafts, wait for "Send" or "Y" before executing anything

## Output Format

```
TRIAGE — [timestamp]

TIER 1 — ACT NOW
[1] [Channel] | From: [name] | Subject/thread
    → Draft: "[draft text]"
    Send? [Y/N]

[2] ...

TIER 2 — TODAY
[3] [Channel] | From: [name] | Subject/thread
    → Draft: "[draft text]"
    Send? [Y/N]

TIER 3 — ARCHIVED
- [count] items archived ([brief description of types])

DONE — [X] items processed, [Y] drafts ready
```

## Modes

- `/triage` — full triage, all tiers with drafts
- `/triage t1` — Tier 1 only (fastest)
- `/triage [channel]` — specific channel only (e.g., `/triage gmail`)

## Guardrails

- **Never send without "Send" or "Y"** — no exceptions
- Skip items already handled in this session
- If a draft requires confidential info check, run the confidentiality protocol first
- For scheduling: always verify calendar before proposing times
