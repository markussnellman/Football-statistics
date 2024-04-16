from dash import Dash, dcc, Output, Input, State, html, no_update, ctx, dash_table
from scripts.reverse_api import get_total_score_board, get_home_score_board, get_away_score_board
from scripts.scraping import scrape_last_five_games, fetch_team_html, scrape_games_last_week, scrape_coach
from .utils.helpers import format_data_to_table
from .utils.info import table_cols, leagues
import dash_bootstrap_components as dbc   
import numpy as np
import pandas as pd


# App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Debug: test dataframe to debug table updating on Render
data = {
        'Team A': ['Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5', 'Col 6', 'Col 7', 'Col 8', 'Col 9'], 
        'Team B': ['Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5', 'Col 6', 'Col 7', 'Col 8', 'Col 9'],
        }
test_df = pd.DataFrame.from_dict(data, orient='index', columns=table_cols)


# Components
league_dropdown = dcc.Dropdown(options=list(leagues.keys()), value='', id='league-dropdown')

home_team_dropdown = dcc.Dropdown(options=[''], value='', id='home-dropdown')

away_team_dropdown = dcc.Dropdown(options=[''], value='', id='away-dropdown')

table = dash_table.DataTable(
    data = None,
    columns = [{'name': i, 'id': i, 'editable': True if i == 'Saknade nyckelspelare' or i == 'Head to head senaste 3 ggr' or i == 'Övriga kommentarer' else False} for i in table_cols],
    id = 'table',
    style_header={
        'fontWeight': 'bold',
        'fontSize': '1em',
        'whiteSpace': 'normal',
        'height': 'auto',
        'fontFamily': 'Arial, sans-serif',
    },
    style_data={
        'fontSize': '1em',
        'fontFamily': 'Arial, sans-serif',
    },
    style_cell={'whiteSpace': 'normal'},
    )


# Layout
app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H4("Liga", className="card-title"),
                                league_dropdown,
                            ]
                        )
                    ]
                )),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H4("Hemmalag", className="card-title"),
                                home_team_dropdown,
                            ]
                        )
                    ]
                )),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H4("Bortalag", className="card-title"),
                                away_team_dropdown,
                            ]
                        )
                    ]
                )),
            ], className='mb-3',
        ),
        dbc.Row(
            [
                table,
            ]
        ),
        dcc.Store(
            id='scoreboard-store',
            data={
                'total scoreboard': {},
                'home scoreboard': {},
                'away scoreboard': {},
                'last five games': {},
            },
        ),
        dcc.Store(
            id='team-data-store',
            data = {
                'coach': {},
                'games last week': {},
            }
        )
    ], className='m-3',
)

# Callbacks

@app.callback(Output('scoreboard-store', 'data'),
            Output('home-dropdown', 'options'),
            Output('away-dropdown', 'options'),
            Input('league-dropdown', 'value'),
            State('scoreboard-store', 'data'),
            prevent_inital_call=True)
def update_league_dropdown(league, data):
    """
    Gets total, home and away scoreboards if not already present.

    Populates the home and away dropdowns.
    """
    if league != '':
        # Teams is a list from leagues dict
        teams = leagues[league]

        # Check if scoreboards not already populated
        # If not, call functions to scrape data
        # Note that dataframes need to be JSON serializable
        if league not in data['total scoreboard'].keys():
            data['total scoreboard'][league] = get_total_score_board().to_json(date_format='iso', orient='split')

        if league not in data['home scoreboard'].keys():
            data['home scoreboard'][league] = get_home_score_board().to_json(date_format='iso', orient='split')

        if league not in data['away scoreboard'].keys():
            data['away scoreboard'][league] = get_away_score_board().to_json(date_format='iso', orient='split')

        if league not in data['last five games'].keys():
            data['last five games'][league] = scrape_last_five_games()

        return data, teams, teams
    
    else: 
        return no_update, no_update, no_update


@app.callback(Output('table', 'data'),
              Output('team-data-store', 'data'),
              Input('home-dropdown', 'value'),
              Input('away-dropdown', 'value'),
              State('league-dropdown', 'value'),
              State('team-data-store', 'data'),
              State('scoreboard-store', 'data'),
              prevent_inital_call=True)
def on_team_change(home_team, away_team, league, team_data, scoreboard):
    """
    Updates the table data using data from team-data-store and scoreboard-store.

    If home_team or away_team has no data in team-data-store, it is fetched first.

    Data formatting done with format_data_to_table function in utils/helpers.
    """

    # Check that teams are properly selected
    if home_team != '' and away_team != '':

        if home_team not in team_data['coach'].keys():
            # Get home team coach for home team
            home_team_html = fetch_team_html(home_team)
            team_data['coach'][home_team] = scrape_coach(home_team_html)

        if away_team not in team_data['coach'].keys():
            # Get away team coach for away team
            away_team_html = fetch_team_html(away_team)
            team_data['coach'][away_team] = scrape_coach(away_team_html)

        if home_team not in team_data['games last week'].keys():
            # Get last weeks games for home tea
            team_data['games last week'][home_team] = scrape_games_last_week(home_team_html)

        if away_team not in team_data['games last week'].keys():
            # Get last weeks games for away team
            team_data['games last week'][away_team] = scrape_games_last_week(away_team_html)  

        # Get scoreboard data and last five games
        # Note that dfs need to be read as JSON
        total_score = pd.read_json(scoreboard['total scoreboard'][league], orient='split')
        home_score = pd.read_json(scoreboard['home scoreboard'][league], orient='split')
        away_score = pd.read_json(scoreboard['away scoreboard'][league], orient='split')
        last_five_games = scoreboard['last five games'][league]

        # Get team data
        coach_home = team_data['coach'][home_team]
        coach_away = team_data['coach'][away_team]
        home_games_last_week = team_data['games last week'][home_team]
        away_games_last_week = team_data['games last week'][away_team]

        df = format_data_to_table(home_team, away_team, total_score, home_score, away_score, last_five_games, coach_home, coach_away, home_games_last_week, away_games_last_week)
        # Debug returning test df
        return test_df.to_dict('records'), team_data

    else:
        return no_update, no_update
