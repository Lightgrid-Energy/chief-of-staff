# /decide — Decision Support

Forces a clear recommendation on any pending decision.

## When to use

When you're stuck, going in circles, or need a second opinion pushed back at you.

Say: `/decide [the decision you're facing]`

## What Claude does

1. **Reframe the decision** — state it in the sharpest possible terms
2. **Identify the real tradeoff** — what are you actually choosing between?
3. **Check goal alignment** — which option best advances OBJ-1/2/3?
4. **Make a recommendation** — one clear answer with the key assumption
5. **Name the risk** — what has to be true for this to be wrong?
6. **Propose next step** — one concrete action to close the loop

## Output Format

```
DECISION: [restated sharply]

TRADEOFF: [A] vs [B]

GOAL ALIGNMENT:
  Option A → advances [OBJ-X] because [reason]
  Option B → advances [OBJ-Y] but at cost of [Z]

RECOMMENDATION: [Option A/B]
  Key assumption: [what must be true]
  
MAIN RISK: [what would make this wrong]

NEXT STEP: [one concrete action — owner, deadline]
```

## Guardrails

- Always make a recommendation — "it depends" is not acceptable output
- State the assumption explicitly — hidden assumptions kill decisions
- One next step only — if there are two, pick the more important one
- If Mujtaba pushes back, engage with the pushback — don't cave without reason
