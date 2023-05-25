import pandas as pd

def append_new_user(user_id, user_name, nick_unite=0, code_unite=0, number_games_rps=0, number_wins_rps=0, history_battles='', balance=0):
    new_row = {'User_id': user_id,
               'User_name': user_name,
               'Nick in Pokemon Unite': nick_unite,
               'Friendship code in Pokemon Unite': code_unite,
               'Number of games in rps': number_games_rps,
               'Number of wins in rps': number_wins_rps,
               'History of battles': history_battles,
               'Balance': balance
              }
    return new_row

def append_value(df, user_id, user_name, type_values):
    user_id = int(user_id)
    if user_id not in list(df['User_id'].values):
        new_row = append_new_user(user_id, user_name)
        df = df.append(new_row, ignore_index=True)

    for i in type_values:
        df.loc[df['User_id'] == user_id, i] += type_values[i]
    df.loc[df['User_id'] == user_id, 'User_name'] = user_name

    history_battles = df.loc[df['User_id'] == user_id, 'History of battles'].values[0].split(';')

    if len(history_battles) > 11:
        history_battles.pop(0)
        df.loc[df['User_id'] == user_id, 'History of battles'] = ';'.join(history_battles)

    return df

def top_rps(df, self_id):
    self_id = int(self_id)
    res = df.sort_index().sort_values('Number of wins in rps', kind='mergesort').iloc[::-1].reset_index(drop=True)
    msg = str()
    for i in range(10):
        msg += f'{i + 1}. {res.iloc[i, 1]} сыграл {res.iloc[i, 4]}, имея {int(res.iloc[i, 5] / res.iloc[i, 4] * 100)}%\n'

    if self_id != -1:
        self_index = res.loc[res['User_id'] == self_id].index[0]
        msg += f'\n{self_index + 1}. {res.iloc[self_index, 1]} сыграл {res.iloc[self_index, 4]}, имея {int(res.iloc[self_index, 5] / res.iloc[self_index, 4] * 100)}%\n' + res.loc[res['User_id'] == self_id, ['History of battles']].values[0][0].replace(';', '\n')

    return msg

def get_top_rps(self_id):
    self_id = int(self_id)
    df = pd.read_csv('database/discord_user.csv')

    if self_id not in list(df['User_id'].values):
        self_id = -1

    return top_rps(df, self_id)

def game_over(game, game_result):
    df = pd.read_csv('database/discord_user.csv')
    player_id = [i for i in game]
    dict_game_result_0 = [{'Number of games in rps': 1,
                        'Number of wins in rps': 0,
                        'History of battles': f'{player_id[1]},{game[player_id[1]][3]},{0};',
                        'Balance': 0},
                        {'Number of games in rps': 1,
                        'Number of wins in rps': 0,
                        'History of battles': f'{player_id[0]},{game[player_id[0]][3]},{0};',
                        'Balance': 0}]
    dict_game_result_1 = [{'Number of games in rps': 1,
                        'Number of wins in rps': 1,
                        'History of battles': f'{player_id[1]},{game[player_id[1]][3]},{1};',
                        'Balance': 10},
                        {'Number of games in rps': 1,
                        'Number of wins in rps': 0,
                        'History of battles': f'{player_id[0]},{game[player_id[0]][3]},{-1};',
                        'Balance': 0}]
    dict_game_result_2 = [{'Number of games in rps': 1,
                        'Number of wins in rps': 0,
                        'History of battles': f'{player_id[1]},{game[player_id[1]][3]},{-1};',
                        'Balance': 0},
                        {'Number of games in rps': 1,
                        'Number of wins in rps': 1,
                        'History of battles': f'{player_id[0]},{game[player_id[0]][3]},{1};',
                        'Balance': 10}]

    if game_result == 0:
        for j, i in enumerate(player_id):
            df = append_value(df, i, game[i][3], dict_game_result_0[j])
    elif game_result == 1:
        for j, i in enumerate(player_id):
            df = append_value(df, i, game[i][3], dict_game_result_1[j])
    elif game_result == 2:
        for j, i in enumerate(player_id):
            df = append_value(df, i, game[i][3], dict_game_result_2[j])

    df.to_csv('database/discord_user.csv', index=False)
