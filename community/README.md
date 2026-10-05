# Community skills

Skills shared by Flaim users. They work alongside the Flaim MCP server, but they aren't part of the official plugin and Flaim doesn't maintain them. Read a skill before you install it.

## Layout

One folder per skill, named after the skill:

```
community/
  weekly-league-report/
    SKILL.md
    (any supporting files the skill needs)
```

## SKILL.md frontmatter

Start `SKILL.md` with YAML frontmatter, the same way the official skills in `.agents/skills/` do:

```markdown
---
name: weekly-league-report
description: Write a weekly recap of the user's Flaim-connected fantasy league, with standings movement, the week's best and worst lineups, and notable transactions. Use when the user asks for a weekly report or invokes /weekly-league-report.
license: MIT
---

# Weekly League Report

Instructions for the AI go here.
```

- **`name`** (required): lowercase words joined by hyphens. It must match the folder name.
- **`description`** (required): what the skill does and when to use it. The AI reads this to decide when to load the skill, so be specific about the requests it covers and the ones it doesn't.
- **`argument-hint`** (optional): a short hint for slash-command arguments, like `"[days-back, default 2]"`.
- **`license`** (optional): `MIT` is the default for this repo.

## Rules

- No secrets: no API keys, tokens, passwords or cookies.
- Don't claim Flaim can change a league. Flaim is read-only. It can't set lineups, add or drop players, make trades or change league settings.
- Use Flaim's tools for league data. The official [`flaim-fantasy` skill](../.agents/skills/flaim-fantasy/SKILL.md) and the [tool snapshot](../tools/tools.json) show what the tools return.

## Try it

Copy the folder into your project's `.agents/skills/` (or `~/.agents/skills/`), or `.claude/skills/` for Claude Code, and ask a question that matches the description.
