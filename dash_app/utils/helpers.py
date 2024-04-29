import pandas as pd
import numpy as np
from .info import table_cols
from datetime import datetime

def format_data_to_table(home_team: str, away_team: str, total_score: pd.DataFrame, home_score: pd.DataFrame, away_score: pd.DataFrame, last_five_games: dict, coach_home: dict, coach_away: dict, home_games_last_week: list[str], away_games_last_week: list[str]) -> pd.DataFrame:

    # Debug
    # print('Home team:', home_team)
    # print('Away team:', away_team)
    # print('Total score', total_score)
    # print('Home score', home_score)
    # print('Away score', away_score)
    # print('Last five games', last_five_games)
    # print('Coach home', coach_home)
    # print('Coach away',coach_away)
    # print('Home games last week', home_games_last_week)
    # print('Away games last week', away_games_last_week)

    # Format first column
    col_1_home = 'Hemma:' + " " + home_team
    col_1_away = 'Borta:' + " " + away_team

    # Format second column
    # Position
    if not total_score.empty:
        home_position = total_score.loc[total_score['name'] == home_team, 'position'].values[0]
        away_position = total_score.loc[total_score['name'] == away_team, 'position'].values[0]

        # Total points
        home_total_points = total_score.loc[total_score['name'] == home_team, 'points'].values[0]
        away_total_points = total_score.loc[total_score['name'] == away_team, 'points'].values[0]

        # Scores
        home_total_scores_for = total_score.loc[total_score['name'] == home_team, 'scores for'].values[0]
        home_total_scores_against = total_score.loc[total_score['name'] == home_team, 'scores against'].values[0]
        away_total_scores_for = total_score.loc[total_score['name'] == away_team, 'scores for'].values[0]
        away_total_scores_against = total_score.loc[total_score['name'] == away_team, 'scores against'].values[0]

        col_2_home = str(home_position) + ", " + str(home_total_points) + "p, " + str(home_total_scores_for) + ":" + str(home_total_scores_against)
        col_2_away = str(away_position) + ", " + str(away_total_points) + "p, " + str(away_total_scores_for) + ":" + str(away_total_scores_against)

    else:
        col_2_home = "Could not retrieve data."
        col_2_away = "Could not retrieve data."

    # Format third column
    # Home team result
    if not home_score.empty and not away_score.empty:
        home_wins = home_score.loc[home_score['name'] == home_team, 'wins'].values[0]
        home_draws = home_score.loc[home_score['name'] == home_team, 'draws'].values[0]
        home_losses = home_score.loc[home_score['name'] == home_team, 'losses'].values[0]

        # Away team result
        away_wins = away_score.loc[away_score['name'] == away_team, 'wins'].values[0]
        away_draws = away_score.loc[away_score['name'] == away_team, 'draws'].values[0]
        away_losses = away_score.loc[away_score['name'] == away_team, 'losses'].values[0]

        # Home team points
        home_points = home_score.loc[home_score['name'] == home_team, 'points'].values[0]

        # Away team points
        away_points = away_score.loc[away_score['name'] == away_team, 'points'].values[0]

        # Home scores
        home_scores_for = home_score.loc[home_score['name'] == home_team, 'scores for'].values[0]
        home_scores_against = home_score.loc[home_score['name'] == home_team, 'scores against'].values[0] 

        # Away scores
        away_scores_for = away_score.loc[away_score['name'] == away_team, 'scores for'].values[0]
        away_scores_against = away_score.loc[away_score['name'] == away_team, 'scores against'].values[0] 

        col_3_home = str(home_wins) + "-" + str(home_draws) + "-" + str(home_losses) + ", " + str(home_points) + "p, " + str(home_scores_for) + ":" + str(home_scores_against)
        col_3_away = str(away_wins) + "-" + str(away_draws) + "-" + str(away_losses) + ", " + str(away_points) + "p, " + str(away_scores_for) + ":" + str(away_scores_against)
    
    else:
        col_3_home = "Could not retrieve data."
        col_3_away = "Could not retrieve data."

    # Format fourth column
    col_4_home = str(last_five_games[home_team].count('win')) + "-" + str(last_five_games[home_team].count('draw')) + '-' + str(last_five_games[home_team].count('lose'))
    col_4_away = str(last_five_games[away_team].count('win')) + "-" + str(last_five_games[away_team].count('draw')) + '-' + str(last_five_games[away_team].count('lose'))

    # Format fifth column
    col_5_home = ''
    col_5_away = ''

    # Format sixth column
    if coach_home == {}:
        # Format to present in table in the case where coach info could not be obtained
        coach_home = {
            'name': 'Kunde inte hitta info.',
            'wins': np.nan,
            'draws': np.nan,
            'losses': np.nan,
        }

    win_percentage_home = round(100 * coach_home['wins'] / (coach_home['wins'] + coach_home['draws'] + coach_home['losses']), 1)
    draw_percentage_home = round(100 * coach_home['draws'] / (coach_home['wins'] + coach_home['draws'] + coach_home['losses']), 1)
    loss_percentage_home = round(100 * coach_home['losses'] / (coach_home['wins'] + coach_home['draws'] + coach_home['losses']), 1)   

    if coach_away == {}:
        # Format to present in table in the case where coach info could not be obtained
        coach_away = {
            'name': 'Kunde inte hitta info.',
            'wins': np.nan,
            'draws': np.nan,
            'losses': np.nan,
        }
    
    win_percentage_away = round(100 * coach_away['wins'] / (coach_away['wins'] + coach_away['draws'] + coach_away['losses']), 1)
    draw_percentage_away = round(100 * coach_away['draws'] / (coach_away['wins'] + coach_away['draws'] + coach_away['losses']), 1)
    loss_percentage_away = round(100 * coach_away['losses'] / (coach_away['wins'] + coach_away['draws'] + coach_away['losses']), 1)

    col_6_home = coach_home['name'] + ", " + str(coach_home['wins']) + " (" + str(win_percentage_home) + "%) - " + str(coach_home['draws']) + " (" + str(draw_percentage_home) + "%) - " + str(coach_home['losses']) + " (" + str(loss_percentage_home) + "%)"
    col_6_away = coach_away['name'] + ", " + str(coach_away['wins']) + " (" + str(win_percentage_away) + "%) - " + str(coach_away['draws']) + " (" + str(draw_percentage_away) + "%) - " + str(coach_away['losses']) + " (" + str(loss_percentage_away) + "%)"

    # Format seventh column
    # Not yet implemented
    col_7_home = ''
    col_7_away = ''

    # Format eighth column
    col_8_home = ", ".join(home_games_last_week)
    col_8_away = ", ".join(away_games_last_week)

    # Format ninth column
    col_9_home = ''
    col_9_away = ''
    
    # Gather data as dict
    data = {
        home_team: [col_1_home, col_2_home, col_3_home, col_4_home, col_5_home, col_6_home, col_7_home, col_8_home, col_9_home], 
        away_team: [col_1_away, col_2_away, col_3_away, col_4_away, col_5_away, col_6_away, col_7_away, col_8_away, col_9_away],
        }

    # Turn data in dict to dataframe with table_cols
    df = pd.DataFrame.from_dict(data, orient='index', columns=table_cols)

    return df


color_scale = ['#ff3300', '#ff5200', '#ff6800', '#fe7b00', '#f59200', '#e7a900', '#d2bf00', '#bbd300', '#91e800', '#00ff33']

def format_conditional_styling(home_team: str, away_team: str, total_score: pd.DataFrame, home_score: pd.DataFrame, away_score: pd.DataFrame, last_five_games: dict, coach_home: dict, coach_away: dict, home_games_last_week: list[str], away_games_last_week: list[str]) -> dict:
    """
    Formats the cells of the dash data-table.
    """
    major_color = '#90EE90'
    mid_color = '#FFFFED'
    minor_color = '#FF474C'

    # Format second column style
    home_pos = total_score.loc[total_score['name'] == home_team, 'position'].values[0]
    away_pos = total_score.loc[total_score['name'] == away_team, 'position'].values[0]

    column_2_style = [
        {
            'if': {
                'row_index': 0,
                'column_id': f'{table_cols[1]}',
            },
            'backgroundColor': major_color if home_pos < away_pos else minor_color
        },
        {
            'if': {
                'row_index': 1,
                'column_id': f'{table_cols[1]}',
            },
            'backgroundColor': major_color if home_pos > away_pos else minor_color
        }
    ]

    # Format column 3 style
    home_points = home_score.loc[home_score['name'] == home_team, 'points'].values[0]
    away_points = away_score.loc[away_score['name'] == away_team, 'points'].values[0]

    column_3_style = [
        {
            'if': {
                'row_index': 0,
                'column_id': f'{table_cols[2]}',
            },
            'backgroundColor': major_color if home_points > away_points else minor_color
        },
        {
            'if': {
                'row_index': 1,
                'column_id': f'{table_cols[2]}',
            },
            'backgroundColor': major_color if home_points < away_points else minor_color
        }
    ]

    # Format column 4 style
    last_5_games_home = last_five_games[home_team].count('win') * 3 + last_five_games[home_team].count('draw')
    last_5_games_away = last_five_games[away_team].count('win') * 3 + last_five_games[away_team].count('draw')

    column_4_style = [
        {
            'if': {
                'row_index': 0,
                'column_id': f'{table_cols[3]}',
            },
            'backgroundColor': major_color if last_5_games_home > last_5_games_away else (mid_color if last_5_games_home == last_5_games_away else minor_color)
        },
        {
            'if': {
                'row_index': 1,
                'column_id': f'{table_cols[3]}',
            },
            'backgroundColor': major_color if last_5_games_home < last_5_games_away else (mid_color if last_5_games_home == last_5_games_away else minor_color)
        }
    ]

    # Format sixth column style
    if coach_home == {}:
        # Format to present in table in the case where coach info could not be obtained
        coach_home = {
            'name': 'Kunde inte hitta info.',
            'wins': np.nan,
            'draws': np.nan,
            'losses': np.nan,
        }

    if coach_away == {}:
        # Format to present in table in the case where coach info could not be obtained
        coach_away = {
            'name': 'Kunde inte hitta info.',
            'wins': np.nan,
            'draws': np.nan,
            'losses': np.nan,
        }

    win_percentage_home = round(100 * coach_home['wins'] / (coach_home['wins'] + coach_home['draws'] + coach_home['losses']), 1)
    win_percentage_away = round(100 * coach_away['wins'] / (coach_away['wins'] + coach_away['draws'] + coach_away['losses']), 1)

    column_6_style = [
        {
            'if': {
                'row_index': 0,
                'column_id': f'{table_cols[5]}',
            },
            'backgroundColor': major_color if win_percentage_home > win_percentage_away else (mid_color if win_percentage_home == win_percentage_away else minor_color)
        },
        {
            'if': {
                'row_index': 1,
                'column_id': f'{table_cols[5]}',
            },
            'backgroundColor': major_color if win_percentage_home < win_percentage_away else (mid_color if win_percentage_home == win_percentage_away else minor_color)
        }
    ]

    # Format eighth column style
    if away_games_last_week != [] and home_games_last_week == []:
        date1 = datetime.strptime(away_games_last_week[0], '%d %b. %y')
        date2 = datetime.strptime('01 Jan. 00', '%d %b. %y')

    elif away_games_last_week == [] and home_games_last_week != []:
        date1 = datetime.strptime('01 Jan. 00', '%d %b. %y')
        date2 = datetime.strptime(home_games_last_week[0], '%d %b. %y')

    elif away_games_last_week == [] and home_games_last_week == []:
        date1 = datetime.strptime('01 Jan. 00', '%d %b. %y')
        date2 = datetime.strptime('01 Jan. 00', '%d %b. %y')

    else:
        date1 = datetime.strptime(away_games_last_week[0], '%d %b. %y')
        date2 = datetime.strptime(home_games_last_week[0], '%d %b. %y')

    column_8_style = [
        {
            'if': {
                'row_index': 0,
                'column_id': f'{table_cols[7]}',
            },
            'backgroundColor': major_color if date1 > date2 else (mid_color if date1 == date2 else minor_color)
        },
        {
            'if': {
                'row_index': 1,
                'column_id': f'{table_cols[7]}',
            },
            'backgroundColor': major_color if date1 < date2 else (mid_color if date1 == date2 else minor_color)
        }
    ]
  
    return column_2_style + column_3_style + column_4_style + column_6_style + column_8_style


"""
Style format
[[{'if': {'row_index': 0, 'column_id': 'Tabellplacering, Poäng, Målskillnad'}, 'backgroundColor': '#90EE90'}, {'if': {'row_index': 1, 'column_id': 'Tabellplacering, Poäng, Målskillnad'}, 'backgroundColor': '#FF474C'}, {'if': {'row_index': 0, 'column_id': 'Hemma/borta resultat, målskillnad'}, 'backgroundColor': '#90EE90'}, {'if': {'row_index': 1, 'column_id': 'Hemma/borta resultat, målskillnad'}, 'backgroundColor': '#FF474C'}, {'if': {'row_index': 0, 'column_id': 'Form senaste 5 matcherna'}, 'backgroundColor': '#90EE90'}, {'if': {'row_index': 1, 'column_id': 'Form senaste 5 matcherna'}, 'backgroundColor': '#FF474C'}, {'if': {'row_index': 0, 'column_id': 'Tränare'}, 'backgroundColor': '#90EE90'}, {'if': {'row_index': 1, 'column_id': 'Tränare'}, 'backgroundColor': '#FF474C'}, {'if': {'row_index': 0, 'column_id': 'Matcher som spelats senaste 7 dagarna'}, 'backgroundColor': '#90EE90'}, {'if': {'row_index': 1, 'column_id': 'Matcher som spelats senaste 7 dagarna'}, 'backgroundColor': '#FF474C'}], None]

Table is accessed as a list in a list so style[0] = list of styles for first table
Then each dict goes column first, so the two first dicts are the first column, row 0 and 1 respectively.
"""
        
def table_style_to_cell_map(style_data: list) -> list:
    """
    Turns style data which is a list of lists containing dicts to 
    a dict of Excel cell - background color key - value pairs.
    """

    excel_cols = {
        table_cols[0]: 0,
        table_cols[1]: 1,
        table_cols[2]: 2,
        table_cols[3]: 3,
        table_cols[4]: 4,
        table_cols[5]: 5,
        table_cols[6]: 6,
        table_cols[7]: 7,
        table_cols[8]: 8,
    }

    n_styles = len([_ for _ in style_data if _ != None])

    excel_style = np.array([[['#FFFFFF'] * 9 ] * 2] * n_styles)

    df_idx = 0
    # loop over each sublist
    for style_lst in style_data:
        if style_lst != None:
            # loop over each dict corresponding to a cell
            for dct in style_lst:
                cell_col = excel_cols[dct['if']['column_id']]
                cell_row = dct['if']['row_index']
                cell_background = dct['backgroundColor']
   
                excel_style[df_idx, cell_row, cell_col] = cell_background

            df_idx += 1

    return excel_style