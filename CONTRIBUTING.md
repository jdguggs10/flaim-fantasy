# Contributing

Thanks for helping make Flaim better. Flaim is a small project worked on in spare time, so reviews are best effort and it may take a while to hear back.

## Official paths

These paths are mirrored from Flaim's main codebase:

- `.agents/skills/`
- `.claude-plugin/` and `.codex-plugin/`
- `.mcp.json`, `server.json` and `glama.json`

Every sync overwrites them, so a pull request that changes them can't be merged here. Instead, a maintainer ports the change into the main codebase and credits you as a co-author on that commit. It shows up here on the next sync. Opening an issue with the **Tool or skill wording suggestion** form works just as well as a pull request.

Wording changes to the shipped skills can take a while to go live. The ChatGPT app ships skill text as part of a reviewed app version, so an accepted change may wait for the next version to be submitted and approved.

`tools/` is written by a daily job from the live server. Please don't edit it; suggest wording changes with an issue instead.

Everything else here, including this file, the README, the issue forms and `community/`, takes normal pull requests.

## Community skills

`community/` accepts skills as they are. A community skill:

- lives at `community/<skill-name>/SKILL.md`, with `name` and `description` frontmatter (see [community/README.md](community/README.md));
- must not contain secrets: no API keys, tokens, passwords or cookies;
- must not claim Flaim can change a league. Flaim is read-only. It can't set lineups, add or drop players, make trades or change league settings.

Community skills aren't bundled into the official plugin, and their authors own them. We check them against the rules above, not for quality.

## Bugs and ideas

Use the issue forms. For a problem with your own account, email [support@flaim.app](mailto:support@flaim.app) instead of opening an issue.

## License

By contributing, you agree that your contribution is licensed under the MIT license, like the rest of this repo.
