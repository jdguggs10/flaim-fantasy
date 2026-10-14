# Agent Guide

Guidance for AI coding agents working in this repository. This is the only agent instruction file here; Claude Code, Codex, Cursor, Copilot and other agents read it directly.

## What this repo is

The public home of Flaim Fantasy's skills, plugin packaging, a daily snapshot of the live tool descriptions, and skills shared by the community. Flaim is read-only: it can look at fantasy leagues but can't set lineups, add or drop players, make trades or change settings. See `README.md`.

## Official paths are mirrored: don't edit them here

These paths are copied here from Flaim's main codebase and must not be changed in this repo, even by a maintainer:

- `.agents/skills/`
- `.claude-plugin/` and `.codex-plugin/`
- `.mcp.json`, `server.json` and `glama.json`
- `.mirror-state.json` (written by the sync)

A direct edit makes the sync stop until it is reverted. To suggest a change to an official skill, open an issue with the **Tool or skill wording suggestion** form, or a pull request that a maintainer will port upstream. See `CONTRIBUTING.md`.

`tools/` is rewritten daily from the live server. Don't edit it either; suggest wording changes with an issue.

Everything else (`README.md`, `CONTRIBUTING.md`, `community/`, `media/`, `scripts/`, issue forms, this file) takes normal pull requests.

## Community skills

New skills go in `community/<skill-name>/SKILL.md`, with `name` (matching the folder) and `description` frontmatter. Start from `community/weekly-league-recap/SKILL.md` and follow `community/README.md`. A community skill must not claim Flaim can change a league.

## Never commit

No secrets of any kind (API keys, tokens, passwords, cookies), no credentials, and no personal or account data, including in examples, issues and pull request text. This repo is public.

## Validate

Run `python3 scripts/validate.py .` before opening a pull request. It checks that JSON parses, plugin manifest paths exist, skill frontmatter is complete, and there are no symlinks. CI runs the same check.
