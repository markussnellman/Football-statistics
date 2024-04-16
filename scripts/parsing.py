import pandas as pd


def parse_total_score(json_response: dict) -> pd.DataFrame: 
    """
    Parses total score from sofascore API json formatted response.

    Returns dataframe with columns:
    name, position, matches, wins, losses, draws, scores for, scores against, points
    """

    # rows is a list containing each team in dicts
    rows = json_response["standings"][0]["rows"]
    teams = []

    # Loop over rows and extract information
    for row in rows:
        team = {
            'name': row["team"]["name"],
            'position': row["position"],
            'matches': row["matches"],
            'wins': row["wins"],
            'losses': row["losses"],
            'draws': row["draws"],
            'scores for': row["scoresFor"],
            'scores against': row["scoresAgainst"],
            'points': row["points"],
        }
        teams.append(team)
        
    df = pd.DataFrame(teams)

    return df


def parse_home_away_score(json_response: dict) -> pd.DataFrame: 
    """
    Parses home score from sofascore API json formatted response.

    Returns dataframe with columns:
    name, wins, losses, draws, scores for, scores agains, points
    """
    
    # rows is a list containing each team in dicts
    rows = json_response["standings"][0]["rows"]
    teams = []

    # Loop over rows and extract informtion
    for row in rows:
        team = {
            'name': row["team"]["name"],
            'wins': row["wins"],
            'losses': row["losses"],
            'draws': row["draws"],
            'scores for': row["scoresFor"],
            'scores against': row["scoresAgainst"],
            'points': row["points"],
        }
        teams.append(team)
        
    df = pd.DataFrame(teams)

    return df


def parse_scraped_scoreboard(table_div: str) -> pd.DataFrame:
    """
    Parses scraped scoreboard in table_div.

    Used in scrape methods.
    """

    table_rows = table_div.css("tr.row-body")

    teams = []

    for row in table_rows:
        tds = row.css('td')

        team = {
            'name': tds[2].css_first("span").text(),
            'position': int(tds[0].css_first("div").text()),
            'points': int(tds[3].text()),
            'matches': int(tds[4].text().split("\n")[1]),
            'wins': int(tds[5].text()),
            'draws': int(tds[6].text()),
            'losses': int(tds[7].text()),
            'scores for': int(tds[8].text()),
            'scores against': int(tds[9].text()),
        }
        
        teams.append(team)

    df = pd.DataFrame(teams)

    return df