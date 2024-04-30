from dash import Dash, dcc, Output, Input, State, html, no_update, dash_table, MATCH, ALL, ctx
from dash.exceptions import PreventUpdate
from scripts.scraping import scrape_last_five_games, fetch_team_html, scrape_games_last_week, scrape_coach, fetch_league_html, scrape_total_table, scrape_home_table, scrape_away_table
from .utils.helpers import format_data_to_table, format_conditional_styling, table_style_to_cell_map
from .utils.info import table_cols, leagues
import dash_bootstrap_components as dbc   
import pandas as pd
import xlsxwriter
from io import BytesIO


# App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks='initial_duplicate')

# Components
# Layout
app.layout = html.Div(
    [
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
        ),
        dcc.Download('download-component'),        
        html.Div(id='hidden-div', style={'display': 'none'}),
        dbc.Button(
            "Lägg till lag", id="add-team-button", className="me-2 mb-3", n_clicks=0
        ),
        dbc.Button(
            "Spara", id="save-matches-button", className="me-3 mb-3", n_clicks=0
        ),
        html.Div(
            children=[],
            id='component-container'
        ),
    ], className='m-3', id ='main-container',
)


# Callbacks   
@app.callback(Output('download-component', 'data'),
              Input('save-matches-button', 'n_clicks'),
              State({'type': 'table', 'index': ALL}, 'data'),
              State({'type': 'table', 'index': ALL}, 'style_data_conditional'),
              State({'type': 'match-container', 'index': ALL}, 'style'),
              prevent_initial_call=True)
def save_excel_new(n_clicks, data, data_styles, display_styles):
    """
    Saves the content of all tables with data as a formatted excel doc.
    """

    if n_clicks and data != [] and not all(isinstance(e, dict) for e in display_styles):
        # Convert data from tables to dataframes
        # To fix a certain bug, set to None otherwise
        dfs = [pd.DataFrame(d) if d != None else None for d in data]

        styles = table_style_to_cell_map(data_styles)

        output = BytesIO()

        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        workbook = None
        worksheet = None

        non_empty_df_number = 0

        for df_number, df in enumerate(dfs):
            # Checks that data is present and that it is not a deleted match
            if isinstance(df, pd.DataFrame) and display_styles[df_number] == None:
                df.to_excel(writer, sheet_name="Sheet1", index=False, header=True, startrow = 1 + 5 * non_empty_df_number)

                # Access the workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets["Sheet1"]

                bold = workbook.add_format({'bold': True})
                worksheet.write(non_empty_df_number * 5, 0, f"Match {non_empty_df_number + 1}", bold)

                # Apply styles to cells
                # We need to rewrite the pandas data because xlsxwriter can't style cells without writing data
                values = df.values
                for row in range(values.shape[0]):
                    for col in range(values.shape[1]):
                        color = workbook.add_format()
                        color.set_bg_color(styles[non_empty_df_number, row, col])
                        # When writing, row must be incremented by two due to Match label and column headers
                        worksheet.write(row + 2 + 5 * non_empty_df_number, col, values[row, col], color)

                non_empty_df_number += 1

        # In the case where we have a removed dataset + an empty dataset
        if worksheet != None:
            # This makes sure the columns expand to fit the text
            worksheet.autofit()
            
            # Writer needs to be closed first
            writer.close()
            output.seek(0)  # Move the pointer to the start of the BytesIO object
            return dcc.send_bytes(output.read(), filename="matcher.xlsx")
        
        else:
            return no_update
        
    else:
        return no_update
        

@app.callback(Output('component-container', 'children'),
              Input('add-team-button', 'n_clicks'),
              State('component-container', 'children'),
              prevent_initial_call=True)
def add_team(n_clicks, children):
    """
    Adds new team component to layout dynamically when button is pressed.
    """
    
    if n_clicks > 0:
        league_dropdown = dcc.Dropdown(options=list(leagues.keys()), value='', 
                                       id={'type': 'league-dropdown', 'index': n_clicks})

        home_team_dropdown = dcc.Dropdown(options=[''], value='', 
                                          id={'type': 'home-dropdown', 'index': n_clicks})

        away_team_dropdown = dcc.Dropdown(options=[''], value='', 
                                          id={'type': 'away-dropdown', 'index': n_clicks})

        table = dash_table.DataTable(
            data = None,
            columns = [{'name': i, 'id': i, 'editable': True if i == 'Saknade nyckelspelare' or i == 'Head to head senaste 3 ggr' or i == 'Övriga kommentarer' else False} for i in table_cols],
            id={'type': 'table', 'index': n_clicks},
            style_header={
                'fontWeight': 'bold',
                'fontSize': '0.8em',
                'whiteSpace': 'normal',
                'height': 'auto',
                'fontFamily': 'Arial, sans-serif',
            },
            style_data={
                'fontSize': '0.8em',
                'fontFamily': 'Arial, sans-serif',
            },
            style_cell={'whiteSpace': 'normal'},
            )

        container = html.Div(
            [
                html.H3(f"Match {n_clicks}", className='mb-3', id={'type': 'match-title', 'index': n_clicks}),
                dbc.Button(
                    "Ta bort", id={'type': 'remove-button', 'index': n_clicks}, className="me-3 mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4("Liga", className="card-title"),
                                    league_dropdown,
                                ])
                            ])
                        ), 
                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4("Hemmalag", className="card-title"),
                                    home_team_dropdown,
                                ])
                            ])
                        ), 
                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4("Bortalag", className="card-title"),
                                    away_team_dropdown,
                                ])
                            ])
                        ), 
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        table,
                    ], className='mb-3',
                )
            ], id={'type': 'match-container', 'index': n_clicks}, 
        )

        children.append(container)

        return children
          
    else:
        return no_update
    

@app.callback(Output({'type': 'match-container', 'index': MATCH}, 'style'),
              Input({'type': 'remove-button', 'index': MATCH}, 'n_clicks'),
              prevent_initial_call=True)
def remove_match(_):
    return {"display": "none"}


@app.callback(Output({'type': 'match-title', 'index': ALL}, 'children'),
              Input('add-team-button', 'n_clicks'),
              Input({'type': 'match-container', 'index': ALL}, 'style'),
              prevent_initial_call=False)
def update_titles(_, styles):
    """
    Fix titles when we press add or remove match.
    """
    print("Clicked!")
    print(styles)
    new_titles = [''] * len(styles)
    match_index = 1
    for i in range(len(styles)):
        if styles[i] == None:
            new_titles[i] = f"Match {match_index}"
            match_index += 1

    return new_titles


# Problem: all outputs must be of MATCH index! So can't update data since it is not a match
@app.callback(Output({'type': 'home-dropdown', 'index': MATCH}, 'options'),
            Output({'type': 'away-dropdown', 'index': MATCH}, 'options'),
            Input({'type': 'league-dropdown', 'index': MATCH}, 'value'),
            prevent_initial_call=True)
def update_league_dropdown(league):
    """
    Populates the home and away dropdowns.
    """
    if league != '' and league is not None:
        # Teams is a list from leagues dict
        teams = leagues[league]

        return teams, teams
    
    else: 
        raise PreventUpdate
    

@app.callback(Output('scoreboard-store', 'data'),
              Input({'type': 'league-dropdown', 'index': ALL}, 'value'),
              State('scoreboard-store', 'data'),
              prevent_initial_call=True)
def update_scoreboards(league, data):
    """
    Updates scoreboard when any league dropdown changes.
    """
    if league != [''] and league is not None:
        # Due to the Input: ALL from dropdowns, leage will be a list, so we need to access correct idx
        triggered = ctx.triggered_id['index']
        league = league[triggered - 1]

        if league != '':

            # Check if scoreboards not already populated
            # If not, call functions to scrape data
            # Note that dataframes need to be JSON serializable
            if league not in data['total scoreboard'].keys():
                # All scrape methods here use the same response_text object as parameter
                # Getting it once is enough
                response_text = fetch_league_html(league)
                total_table = scrape_total_table(response_text)
                data['total scoreboard'][league] = total_table.to_json(date_format='iso', orient='split')

            if league not in data['home scoreboard'].keys():
                home_table = scrape_home_table(response_text)
                data['home scoreboard'][league] = home_table.to_json(date_format='iso', orient='split')

            if league not in data['away scoreboard'].keys():
                away_table = scrape_away_table(response_text)
                data['away scoreboard'][league] = away_table.to_json(date_format='iso', orient='split')

            if league not in data['last five games'].keys():
                last_five_games = scrape_last_five_games(response_text)
                data['last five games'][league] = last_five_games

            return data
        
        return no_update
    
    else:
        return no_update


@app.callback(Output({'type': 'table', 'index': ALL}, 'data'),
              Output({'type': 'table', 'index': ALL}, 'style_data_conditional'),
              Output('team-data-store', 'data'),
              Input({'type': 'home-dropdown', 'index': ALL}, 'value'),
              Input({'type': 'away-dropdown', 'index': ALL}, 'value'),
              State({'type': 'league-dropdown', 'index': ALL}, 'value'),
              State({'type': 'table', 'index': ALL}, 'data'),
              State({'type': 'table', 'index': ALL}, 'style_data_conditional'),
              State('team-data-store', 'data'),
              State('scoreboard-store', 'data'),
              prevent_initial_call=True)
def on_team_change(home_team, away_team, league, table_data, style_data_conditional, team_data, scoreboard):
    """
    Updates the table data using data from team-data-store and scoreboard-store.

    If home_team or away_team has no data in team-data-store, it is fetched first.

    Data formatting done with format_data_to_table function in utils/helpers.
    """
    # We need to determine which ID changed.
    # We have to do it this way to be able to u - 1pdate a specific table and the data store in the same callback
    triggered_id = ctx.triggered_id['index']
    home_team = home_team[triggered_id - 1]
    away_team = away_team[triggered_id - 1]
    league = league[triggered_id - 1]

    # Check that teams are properly selected
    if home_team != '' and away_team != '' and league != '':

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

        # Update table data
        df = format_data_to_table(home_team, away_team, total_score, home_score, away_score, last_five_games, coach_home, coach_away, home_games_last_week, away_games_last_week)

        table_data[triggered_id - 1] = df.to_dict('records')

        # Update conditional styling
        conditional_style = format_conditional_styling(home_team, away_team, total_score, home_score, away_score, last_five_games, coach_home, coach_away, home_games_last_week, away_games_last_week)

        # Give styling to the correct table
        style_data_conditional[triggered_id - 1] = conditional_style
        
        return table_data, style_data_conditional, team_data

    else:
        raise PreventUpdate