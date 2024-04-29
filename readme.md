# Football statistics app

Lets users select leagues and their teams to compare their performance.

To add a new league:

1. Navigate to scripts/config.py
2. Create a new dict (called "NEW_LEAGUE" in this example) with team name as key, and the html slug as value.
3. Concatinate it with the "ALL_TEAMS_SLUG" dict.
4. Navigate to dash_app/info.py
5. In the "league" dict, concatinate the keys from "NEW_LEAGUE" as such: "New League": list(scripts.config.NEW_LEAGUE.keys())
