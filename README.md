# Flaim Fantasy

Flaim Fantasy connects your ESPN, Yahoo and Sleeper fantasy leagues to ChatGPT and Claude, so you can ask about your actual team. "Who should I start this week?" "Is this trade fair?" "What's on the waiver wire?" The AI answers with your real league in front of it.

Flaim is read-only. It can look at your leagues, but it can't set lineups, add or drop players, make trades or change settings. It's free, and it's an independent project.

<p align="center">
  <img src="media/connected-leagues-widget-2026.png" width="360" alt="Flaim showing connected ESPN, Yahoo, and Sleeper fantasy football leagues in ChatGPT.">
</p>

## Get started

1. **Connect your leagues** at [flaim.app](https://flaim.app). ESPN connects through the Flaim Chrome extension, Yahoo through Yahoo sign-in, and Sleeper by username.
2. **Open Flaim Fantasy** in [ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_69a8f78087e081919e52cacacf00ff36) or [Claude](https://claude.ai/directory/connectors/f1a5b6a4-1f5b-470c-af23-71fc7ab13754) and ask about your team.

That's it. If you use Claude Code, you can also [install the plugin](#install-the-claude-code-plugin).

## See it in action

<table>
  <tr>
    <td align="center" width="33%"><strong>ChatGPT</strong><br>Ask about the team you actually manage</td>
    <td align="center" width="33%"><strong>Claude</strong><br>See what is happening across your league</td>
    <td align="center" width="33%"><strong>Perplexity</strong><br>Bring your league into your research</td>
  </tr>
  <tr>
    <td align="center"><img src="media/homepage-chatgpt-team-status-20260815.png" width="240" alt="ChatGPT answering How is my team doing? with Flaim Fantasy using a connected ESPN baseball league."></td>
    <td align="center"><img src="media/homepage-claude-matchup-status-20260815.png" width="240" alt="Claude showing a Flaim Fantasy answer about the status of a connected ESPN baseball matchup."></td>
    <td align="center"><img src="media/homepage-perplexity-best-team-20260815.png" width="240" alt="Perplexity answering Who has the best team? with Flaim Fantasy using a connected ESPN baseball league."></td>
  </tr>
</table>

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

Pull requests to the official skills are welcome. These files are mirrored from Flaim's main codebase, so instead of merging here we'll bring your change in with co-author credit, and it syncs back automatically.

Not sure about exact wording? [Open an issue](https://github.com/jdguggs10/flaim-fantasy/issues/new/choose) with the **Tool or skill wording suggestion** form. Tell us what the AI got wrong and quote the text you'd change. The tool descriptions in `tools/` are rewritten from the live server every day, so suggest changes to those with the form rather than a pull request.

## Share a skill of your own

Built a skill that works well with Flaim, like a weekly league recap or a trade deadline checklist? Add it under `community/`. The [weekly league recap](community/weekly-league-recap/SKILL.md) is a working example to start from. See [community/README.md](community/README.md) for the layout and [CONTRIBUTING.md](CONTRIBUTING.md) for how contributions work. If you have an idea but not a skill yet, the **Skill idea** issue form is the place for it.

## Need help with your account?

To connect or manage leagues, go to [flaim.app/leagues](https://flaim.app/leagues). For anything else about your account, email [support@flaim.app](mailto:support@flaim.app). Please keep account details out of public issues.

## For tinkerers

- **`.agents/skills/`**: the official Flaim skills. They're the analyst playbook an AI follows for start/sit calls, waivers, trades, keepers, matchups and more.
- **`.claude-plugin/` and `.codex-plugin/`**: plugin packaging for Claude Code and Codex.
- **`.mcp.json` and `server.json`**: how MCP clients find the Flaim server at `https://api.flaim.app/mcp`.
- **`tools/`**: a daily snapshot of the live tool descriptions (`tools.json`) and server instructions (`instructions.md`), taken straight from the server.
- **`community/`**: skills shared by other Flaim users.

The official files are copied here from Flaim's main codebase whenever they change, so this repo always matches what ships.

## License

MIT. See [LICENSE](LICENSE).
