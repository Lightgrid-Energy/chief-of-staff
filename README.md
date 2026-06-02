# Lightgrid Energy — AI Chief of Staff

Personal AI operating system built on Claude Code. Doubles executive productivity by unifying inboxes, managing tasks, deepening relationships, and pushing back on decisions.

## What This Does

- **`/gm`** — Morning briefing: calendar, tasks, goal health, inbox scan
- **`/triage`** — Unified inbox across Gmail, WhatsApp, Slack with send-ready drafts
- **`/my-tasks`** — Task list Claude actively works on, aligned to your goals
- **`/enrich`** — Auto-enriches contact records from all communications
- **`/decide`** — Forces a clear recommendation on any pending decision
- **`/prep`** — Meeting prep brief pulled from contact files and recent comms

## Setup

```bash
git clone https://github.com/Lightgrid-Energy/chief-of-staff
cd chief-of-staff
bash install.sh
```

Then:
1. Edit `~/.claude/CLAUDE.md` — fill in all `CUSTOMIZE` sections with your details
2. Edit `~/.claude/goals.yaml` — set your actual quarterly goals
3. Connect MCP servers — see `docs/mcp-setup.md`
4. Open Claude Code and run `/gm`

## File Structure

```
chief-of-staff/
├── CLAUDE.md           # Core AI system definition — your operating system
├── goals.yaml          # Quarterly objectives (source of truth for priorities)
├── my-tasks.yaml       # Active task list
├── install.sh          # Installs files to ~/.claude/
├── sync.sh             # Pulls changes from ~/.claude/ back to repo
├── commands/
│   ├── gm.md           # /gm morning briefing
│   ├── triage.md       # /triage inbox processing
│   ├── my-tasks.md     # /my-tasks task management
│   ├── enrich.md       # /enrich contact enrichment
│   ├── decide.md       # /decide decision support
│   └── prep.md         # /prep meeting preparation
├── contacts/           # Contact files (gitignored — keep private)
├── docs/
│   └── mcp-setup.md    # How to connect Gmail, Calendar, WhatsApp, etc.
└── README.md
```

## Key Concept

`CLAUDE.md` is your AI operating system. The more you customize it — your voice, your team, your goals, your constraints — the better it performs. It compounds.

## Credits

Inspired by [Mike Murchison's claude-chief-of-staff](https://github.com/mimurchison/claude-chief-of-staff). Customized for Lightgrid Energy.
