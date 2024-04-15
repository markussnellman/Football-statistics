import pandas as pd
from .info import table_cols

def format_data_to_table(home_team: str, away_team: str, total_score: pd.DataFrame, home_score: pd.DataFrame, away_score: pd.DataFrame, last_five_games: dict, coach_home: dict, coach_away: dict, home_games_last_week: list[str], away_games_last_week: list[str]) -> pd.DataFrame:

    # Format first column
    col_1_home = 'Hemma:' + " " + home_team
    col_1_away = 'Borta:' + " " + away_team

    # Format second column
    # Position
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

    # Format third column
    # Home team result
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

    # Format fourth column
    col_4_home = str(last_five_games[home_team].count('win')) + "-" + str(last_five_games[home_team].count('draw')) + '-' + str(last_five_games[home_team].count('lose'))
    col_4_away = str(last_five_games[away_team].count('win')) + "-" + str(last_five_games[away_team].count('draw')) + '-' + str(last_five_games[away_team].count('lose'))

    # Format fifth column
    col_5_home = ''
    col_5_away = ''

    # Format sixth column
    col_6_home = coach_home['name'] + ", " + str(coach_home['wins']) + "-" + str(coach_home['draws']) + "-" + str(coach_home['losses'])
    col_6_away = coach_away['name'] + ", " + str(coach_away['wins']) + "-" + str(coach_away['draws']) + "-" + str(coach_away['losses'])

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

