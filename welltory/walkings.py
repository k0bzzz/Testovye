import pandas as pd


def find_walkings(df, avg_step=0.71, walking_speed_min=2, walking_speed_max=7, max_walking_interval=900,
                  min_walking_time=300, pause_threshold=30) -> dict:
    # Функцию комментариями не загромождал, все описание в ноутбуке

    for col in ['time_start_local', 'time_end_local']:
        df[col] = pd.to_datetime(df[col])
        df[col] = df.apply(lambda x: x[col] - pd.Timedelta(seconds=x.time_offset), axis=1)

    df.drop_duplicates(inplace=True)

    df['time_diff'] = (df.time_end_local - df.time_start_local).apply(lambda x: x.total_seconds())
    df = df[df.time_diff >= 0].sort_values(by='time_start_local').reset_index(drop=True)

    df.drop(df[df.time_diff > max_walking_interval].index, inplace=True)

    df['is_walking_speed'] = (df.steps * avg_step / df.time_diff * 3.6).round(decimals=1)\
        .between(walking_speed_min, walking_speed_max)
    df = df.drop(df[~df.is_walking_speed].index)

    df['is_valid_pause'] = (df.time_start_local - df.shift().time_end_local).apply(
        lambda x: x.total_seconds()) <= pause_threshold

    interval_idxs_start = df[(~df.is_valid_pause) & (df.is_valid_pause.shift(-1))].index.to_list()
    interval_idxs_end = df[df.is_valid_pause & (df.is_valid_pause.shift(-1) == False)].index.to_list()

    df['num_interval'] = -1
    for i, (start, end) in enumerate(zip(interval_idxs_start, interval_idxs_end)):
        df.loc[start:end, 'num_interval'] = i

    walking_intervals_df = df[df.num_interval >= 0].groupby('num_interval').agg(
        {'time_diff': sum, 'time_start_local': min, 'time_end_local': max, 'steps': sum, 'time_offset': min})
    walking_intervals_df = walking_intervals_df[walking_intervals_df.time_diff > min_walking_time]

    walking_intervals_df['day'] = walking_intervals_df.time_start_local.dt.strftime('%Y-%m-%d')
    for col in ['time_start_local', 'time_end_local']:
        walking_intervals_df[col] = walking_intervals_df.apply(lambda x: (x[col] + pd.Timedelta(seconds=x.time_offset)),
                                                               axis=1)

    walking_intervals_df.drop(['time_diff', 'time_offset'], axis=1, inplace=True)

    result = {day: [] for day in walking_intervals_df.day.unique()}
    for row in walking_intervals_df.itertuples():
        result[row.day].append({'start': row.time_start_local.strftime('%Y-%m-%d %H:%M:%S'),
                                'end': row.time_end_local.strftime('%Y-%m-%d %H:%M:%S'),
                                'steps': row.steps})

    return result


