# MCP Server Setup Guide

Connect these servers to unlock the full chief-of-staff system.

## Priority Order

1. Gmail (unlocks /triage and /gm email scan)
2. Google Calendar (unlocks scheduling in /gm and /triage)
3. WhatsApp (unlocks WhatsApp triage)
4. Google Drive (unlocks document access)

---

## Gmail MCP

Install:
```bash
npx @gptscript-ai/gateway-provider-gmail
```

Or use the official Google Workspace MCP:
```bash
# In Claude Code settings (claude.ai/code -> Settings -> MCP)
# Add server: gmail
# Follow OAuth flow
```

Claude Code settings.json entry:
```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gmail"],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "~/.claude/gmail-credentials.json"
      }
    }
  }
}
```

---

## Google Calendar MCP

```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "~/.claude/google-credentials.json"
      }
    }
  }
}
```

---

## WhatsApp MCP

WhatsApp requires a bridge. Options:
1. **whatsapp-web.js bridge** — runs locally, scans QR code
2. **Twilio WhatsApp API** — production-grade, requires number

For local setup:
```bash
npx @pedrocid/whatsapp-mcp-server
```

---

## Adding MCP to Claude Code

In Claude Code, run:
```
/mcp
```

Or edit `~/.claude/settings.json` to add server configs.

---

## Testing Your Setup

Once connected, test with:
- `/gm` — should show today's calendar if Calendar is connected
- `/triage gmail` — should show unread emails if Gmail is connected
- `/enrich all` — should scan connected channels

---

## Resources

- [Claude Code MCP docs](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [MCP server registry](https://github.com/modelcontextprotocol/servers)
