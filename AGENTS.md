# AGENTS.md — abillionrobots.com

## What This Is

abillionrobots.com is a running public log of ground-level robotics observations — signals, deals, trends, and field intel gathered from the team. It's not a news site. It's a curated feed of real signal.

## Core Rules

**Never fabricate entries.** Every entry must come from a real observation sent by a real person. If you're not sure, ask — don't fill in.

**Never auto-publish.** The publish step (`scripts/publish-rollup.sh`) requires explicit approval from all three owners (Erik, Ethan, Raymond) before running. Never call it autonomously.

**Redact before publishing.** Apply the rules below to every entry before it goes public.

---

## Redaction Rules (Apply Before Any Public Post)

### Always redact
- **Author names** (Ethan, Erik, Raymond) → use "a team member" or just remove attribution
- **Personal contacts** (e.g. "Anand", "Eugene") → "a contact", "an operator", "a founder"
- **Deal specifics** — dollar amounts, close dates, undisclosed terms

### Redact unless confirmed public
- **Startup/company names** not yet in public announcements → replace with "a robotics company", "a hotel operator", etc. Flag with [REDACT?] if unsure
- **Strategic maneuvers** that could doxx the company or source (e.g. corporate structure advice that implies inside knowledge)

### Keep as-is (public info)
- Public company names (FANUC, BorgWarner, DeWalt, etc.)
- Public events and conferences (Automate 2026, etc.)
- Public robots and products (T800, etc.)
- General market observations with no source fingerprint

### Flag with [REDACT?] when ambiguous
If you're unsure whether a name or detail is safe to publish, leave it as `[REDACT? — <name/detail>]` in the draft and let the team decide before publishing.

---

## File Structure

```
abillionrobots/
  changelog.json         # Raw entries (internal, includes real names)
  index.html             # Public-facing site
  updates/index.html     # Updates feed
  scripts/
    publish-rollup.sh    # DO NOT run without triple approval
  AGENTS.md              # This file
```

## Key Source Files

- `../robotics-learnings.md` — Raw daily log (internal). This is the source of truth. Agents read from here to build rollups.
- `changelog.json` — Structured entries (internal). May contain real names — treat as internal.

---

## Weekly Rollup Workflow

1. Every Sunday at 6pm, a cron job reads `robotics-learnings.md` and compiles the week's entries
2. Applies redaction rules above
3. Sends the draft to the team group chat for review
4. Waits for explicit approval from all three: Erik, Ethan, and Raymond
5. Only then runs `publish-rollup.sh`

If you are a rollup agent: produce the draft, send it, stop. Do not publish.

---

## Adding Entries

When a team member sends a robotics observation via Telegram DM:
1. Append to `../robotics-learnings.md` with date + author (real name OK here — it's internal)
2. Commit and push immediately: `git add robotics-learnings.md && git commit -m "log: robotics observation from [author] [date]" && git push`
3. Confirm to the sender

Do not wait for the cron. Save on receipt.
