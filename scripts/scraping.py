import requests
import pandas as pd
from datetime import datetime
from . import config
from .parsing import parse_scraped_scoreboard
from selectolax.parser import HTMLParser

# Todo: implement the integration of other Leagues
# Need to come up with some idea on how to use the team_slug
# Idea: combine league team slugs to one dict

class BeSoccerNameNotFound(Exception):
    """Exception if league or football team not found or could not be mapped"""
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f"{self.message}"
    

league_slug = config.LEAGUE_SLUG
team_slug = config.ALL_TEAMS_SLUG

def fetch_league_html(league: str) -> str:
    """Fetches the HTML content of the page containing the team's data."""
    # Replace team name to slug
    if league in league_slug.keys():
        league = league_slug[league]

    else:
        raise BeSoccerNameNotFound(f'Could not map {league} to slug.')

    base = config.LEAGUE_URL + league

    response = requests.get(base)

    if response.status_code == 200:
        return response.text
    
    else:
        print(f"Error fetching from {base}: {response.status_code}")
        return None 


def scrape_last_five_games(response_text: str) -> dict:
    """
    Scrapes the last five games, returns a dict with team as key and value as list of results.

    Uses response_text from fetch_league_html().
    """

    if response_text is not None:

        html = HTMLParser(response_text)

        # Gets all rows in table
        rows = html.css_first("table.table").css("td.name")

        # Loop over rows
        results = {}
        for row in rows:
            # Team name found in span with class team-name
            team = row.css_first("span.team-name").text()

            match_res = []
            
            # match results are in 5 spans with class bg-match-res
            # the span class needs to be extracted
            spans = row.css("span.bg-match-res")
            
            # Loop over spans
            for span in spans:
                # Get the class
                match_res.append(span.attributes['class'].split(' ')[-1])
                
            results[team] = match_res
        
        return results
    
    else:
        return {}
    

def fetch_team_html(team: str) -> str:
    """Fetches the HTML content of the page containing the team's data."""
    # Replace team name to slug
    if team in team_slug.keys():
        team = team_slug[team]

    else:
        raise BeSoccerNameNotFound(f'Could not map {team} to slug.')

    base = config.TEAM_URL + team

    response = requests.get(base)

    if response.status_code == 200:
        return response.text
    
    else:
        print(f"Error fetching from {base}: {response.status_code}")
        return None 


def scrape_games_last_week(response_text: str) -> list[str]:
    """
    Scrapes the dates of the games in the last seven days.

    Uses response_text from fetch_team_html().
    """
    dates = []

    # If request failed, response_text will be none.
    if response_text is not None:
        html = HTMLParser(response_text)

        # Dates contained in div
        divs = html.css_first('div.spree-content').css('div.date.color-grey2')

        today = datetime.today()
        for div in divs:
            date_string = div.text()
            date_object = datetime.strptime(date_string, '%d %b.')
            current_year = datetime.now().year
            date_object = date_object.replace(year=current_year)
            
            # If the difference in days < 7, add to list
            difference = today - date_object
            days = difference.days

            if (days < 7):
                dates.append(date_object.strftime("%d %b. %y"))

    return dates


def scrape_coach(response_text: str) -> dict:
    """
    Gets coach data for team from html response.
    
    Uses response_text from fetch_team_html().
    """

    if response_text is not None:
        html = HTMLParser(response_text)

        div = html.css_first('div#mod_coachStats')

        # In some cases, there is no coach statistics on the site.
        # In such a case "div" will be None and we get an AttributeError
        # when calling css_first().
        try:
            name = div.css_first('p.mb5').text()

            data = div.css('div.main-line.mt10.mb5')

            matches = int(data[0].text())
            wins = int(data[1].text())
            draws = int(data[2].text())
            losses = int(data[3].text())

            return {
                'name': name,
                'matches': matches,
                'wins': wins,
                'draws': draws,
                'losses': losses,
            }
        
        except AttributeError:
            return {}

    else:
        return {}
    

def scrape_total_table(response_text: str) -> pd.DataFrame:
    """Scrapes total table from response text.
    
    Uses response_text from fetch_league_html()."""

    if response_text is not None:
        html = HTMLParser(response_text)

        table_div = html.css_first("div.table-body.table-custom.competition-result")

        df = parse_scraped_scoreboard(table_div)

        return df

    else:
        return pd.DataFrame([])


def scrape_home_table(response_text: str) -> pd.DataFrame:
    """Scrapes home table from response text.
    
    Uses response_text from fetch_league_html()."""

    if response_text is not None:
        html = HTMLParser(response_text)

        table_div = html.css("div.table-body.table-custom.competition-result")[1]

        df = parse_scraped_scoreboard(table_div)

        return df

    else:
        return pd.DataFrame([])
    

def scrape_away_table(response_text: str) -> pd.DataFrame:
    """Scrapes away table from response text.
    
    Uses response_text from fetch_league_html()."""

    if response_text is not None:
        html = HTMLParser(response_text)

        table_div = html.css("div.table-body.table-custom.competition-result")[2]

        df = parse_scraped_scoreboard(table_div)

        return df

    else:
        return pd.DataFrame([])


