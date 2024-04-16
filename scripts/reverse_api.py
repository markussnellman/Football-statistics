import requests
import pandas as pd
from . import config
from .parsing import parse_total_score, parse_home_away_score
from typing import Callable

headers = config.HEADERS

total_url = config.TOTAL_URL
home_url = config.HOME_URL
away_url = config.AWAY_URL

"""
Requests to these APIs return 403 status code when live on Render.

Need another alternative.
"""


def get_score_board(url: str, headers: str, parse: Callable) -> pd.DataFrame:
    """Gets score board from url and parses JSON with parse function. 
    
    Returns df implemented by parse function."""

    response = requests.get(url, headers=headers)

    # If request successful, proceed
    if response.status_code == 200:
        
        # Turn response to JSON
        data = response.json()
        
        # Parse the JSON data
        df = parse(data)
        return df

    # If request failed, return empty dataframe
    else:
        print(f"Failed to retrieve data from {url}, status code. {response.status_code}")
        return pd.DataFrame([])


def get_total_score_board() -> pd.DataFrame:
    """Returns total score board as dataframe."""
    return get_score_board(total_url, headers, parse_total_score)


def get_home_score_board() -> pd.DataFrame:
    """Returns home score board as dataframe."""
    return get_score_board(home_url, headers, parse_home_away_score)


def get_away_score_board() -> pd.DataFrame:
    """Returns away score board as dataframe."""
    return get_score_board(away_url, headers, parse_home_away_score)


# Testing
if __name__ == "__main__":
    total_score = get_total_score_board()
    home_score = get_home_score_board()
    away_score = get_away_score_board()

    print(total_score)
    print(home_score)
    print(away_score)