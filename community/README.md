# Community skills

Skills shared by Flaim users. They work alongside the Flaim MCP server, but they aren't part of the official plugin and Flaim doesn't maintain them. Read a skill before you install it.

## Start from the example

[`weekly-league-recap`](weekly-league-recap/SKILL.md) is a complete, working community skill. Copy its folder, rename it, and change the instructions. It shows the parts every skill needs: the frontmatter, picking the user's league the same way the official skills do, and which Flaim tools to call.

## Layout

One folder per skill, named after the skill:

```
community/
  weekly-league-recap/
    SKILL.md
    (any supporting files the skill needs)
```

## SKILL.md frontmatter

Start `SKILL.md` with YAML frontmatter, the same way the official skills in `.agents/skills/` do:

- **`name`** (required): lowercase words joined by hyphens. It must match the folder name.
- **`description`** (required): what the skill does and when to use it. The AI reads this to decide when to load the skill, so be specific about the requests it covers.
- **`argument-hint`** (optional): a short hint for slash-command arguments, like `"[days-back, default 2]"`.
- **`license`** (optional): `MIT` is the default for this repo.

## Rules

- No secrets: no API keys, tokens, passwords or cookies.
- Don't claim Flaim can change a league. Flaim is read-only. It can't set lineups, add or drop players, make trades or change league settings.
- Use Flaim's tools for league data. The official [`flaim-fantasy` skill](../.agents/skills/flaim-fantasy/SKILL.md) and the [tool snapshot](../tools/tools.json) show what the tools return.

## Try it

Copy the folder into your project's `.agents/skills/` (or `~/.agents/skills/`), or `.claude/skills/` for Claude Code, and ask a question that matches the description.
