---
name: weekly-league-recap
description: Write a friendly weekly recap of a Flaim-connected fantasy league for the league's group chat, covering the week's matchup results, the standings, and notable adds, drops and trades. Use when the user asks for a weekly recap, a league roundup, or something to post in the league chat, or invokes /weekly-league-recap.
argument-hint: "[week-number, default the most recent completed week]"
license: MIT
---

# Weekly League Recap

Write a short, upbeat recap of the week in the user's fantasy league that they can paste straight into the league group chat.

## Scope

- League data comes only from Flaim's tools. Flaim reads leagues; it can't change lineups, rosters, trades or settings, so the recap reports what happened and never offers to act on it.
- Don't invent scores, records or moves. If a tool doesn't return something, leave it out.

## Workflow

### 1. Pick the league

- Reuse a successful `get_user_session` result from earlier in this chat. If there isn't one, call it.
- If the user names a league, platform or sport, use that league. Otherwise use `defaultLeague` when present, or the relevant sport's entry in `defaultLeagues`.
- If more than one league still fits, ask which one, by league name. Never show internal league IDs.
- Call `get_league_info` once for the selected league so team and owner names are right.

### 2. Gather the week

- `get_matchups` for the requested week. With no argument, use the most recent completed week.
- `get_standings` for the current table.
- `get_transactions` for the same week, to find the notable adds, drops and trades.

### 3. Write the recap

Keep it under about 250 words, in a warm, lightly teasing group-chat voice. Suggested shape:

- **Headline:** one line on the story of the week.
- **Results:** each matchup in one line, winner first, with the score. Call out the closest game and the biggest blowout.
- **Standings:** the top three and anyone who moved a lot. One line on the playoff picture if it's late in the season.
- **Moves:** the two or three most interesting transactions, by team name.
- **Sign-off:** one line looking ahead to next week.

Use team names, not owner real names, unless the user asks otherwise. Keep it kind: tease results, not people.
