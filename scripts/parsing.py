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

