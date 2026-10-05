# Flaim Fantasy

Flaim Fantasy connects your ESPN, Yahoo and Sleeper fantasy leagues to ChatGPT and Claude, so you can ask about your actual team. "Who should I start this week?" "Is this trade fair?" "What's on the waiver wire?" The AI answers with your real league in front of it.

Flaim is read-only. It can look at your leagues, but it can't set lineups, add or drop players, make trades or change settings. It's free, and it's an independent project. Sign up and connect your leagues at [flaim.app](https://flaim.app).

## What's in this repo

- **`.agents/skills/`**: the official Flaim skills. They're the analyst playbook an AI follows for start/sit calls, waivers, trades, keepers, matchups and more.
- **`.claude-plugin/` and `.codex-plugin/`**: plugin packaging for Claude Code and Codex.
- **`.mcp.json` and `server.json`**: how MCP clients find the Flaim server at `https://api.flaim.app/mcp`.
- **`tools/`**: a daily snapshot of the live tool descriptions (`tools.json`) and server instructions (`instructions.md`), taken straight from the server.
- **`community/`**: skills shared by other Flaim users.

The official files are copied here from Flaim's main codebase whenever they change, so this repo always matches what ships.

## Install the Claude Code plugin

The plugin bundles the skills and the Flaim MCP server.

```bash
claude plugin marketplace add jdguggs10/flaim-fantasy
claude plugin install flaim-fantasy@flaim
```

Then run `/mcp` in Claude Code and choose the Flaim server to sign in. You'll need a Flaim account with at least one league connected.

If you only want the MCP server, run:

```bash
claude mcp add --transport http flaim https://api.flaim.app/mcp
```

## Use the skills in other tools

Tools that support Agent Skills look for them in your project's `.agents/skills/` folder, or in `~/.agents/skills/` for every project. Copy the skill folder over:

```bash
git clone https://github.com/jdguggs10/flaim-fantasy.git
cp -r flaim-fantasy/.agents/skills/flaim-fantasy ~/.agents/skills/flaim-fantasy
```

The AI picks up the skill on its own when you ask a fantasy question.

## Suggest a wording change

The tool descriptions and skills are written for an AI to read, and small wording changes can make a real difference. If you've watched the AI misread a tool, or a skill gave advice you'd change, [open an issue](https://github.com/jdguggs10/flaim-fantasy/issues/new/choose) with the **Tool or skill wording suggestion** form. Quoting the current text and what went wrong helps a lot.

Please don't open a pull request against `tools/`. Those files are rewritten from the live server every day.

## Share a skill of your own

Built a skill that works well with Flaim, like a weekly league report or a trade deadline checklist? Add it under `community/`. See [community/README.md](community/README.md) for the layout and [CONTRIBUTING.md](CONTRIBUTING.md) for how contributions work. If you have an idea but not a skill yet, the **Skill idea** issue form is the place for it.

## Need help with your account?

To connect or manage leagues, go to [flaim.app/leagues](https://flaim.app/leagues). For anything else about your account, email [support@flaim.app](mailto:support@flaim.app). Please keep account details out of public issues.

## License

MIT. See [LICENSE](LICENSE).
