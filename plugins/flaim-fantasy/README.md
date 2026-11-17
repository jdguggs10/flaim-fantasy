# Flaim Fantasy

Flaim Fantasy connects your ESPN, Yahoo, and Sleeper fantasy leagues to Claude so you can ask about your actual team. Get help with start or sit decisions, waiver pickups, trades, standings, league activity, and matchups.

Connect your leagues at [flaim.app](https://flaim.app), then sign in to the Flaim connector in Claude. When your question depends on league data, the plugin's three skills guide Claude in calling the remote Flaim connector at `https://api.flaim.app/mcp`. Claude sends the lookup details, such as a league, season, or player, and Flaim returns the relevant fantasy data. If you ask to refresh your leagues, Flaim updates its own records of your connected leagues. Flaim can't set lineups, add or drop players, make trades, or change league settings.

Flaim is free and isn't affiliated with ESPN, Yahoo, or Sleeper. This application uses fantasy data provided by Yahoo Fantasy.

For help, visit [Flaim support](https://flaim.app/support). See [LICENSE](LICENSE) for license terms.
