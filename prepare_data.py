import os
from csv import writer
import pandas as pd
import numpy as np
from pathlib import Path
import argparse

full_header = ['domain_name', 'app_name', 'developer', 'email', 'price', 'last_update', 'category', 'size',
               'number_of_installs', 'version', 'compatibility', 'maturity_rating', 'app_store_purchases', 'rating',
               'number_of_ratings', 'five_star', 'four_star', 'three_star', 'two_star', 'one_star', 'link',
               'description', 'release_text']

header = ['domain_name', 'price', 'last_update', 'version', 'rating', 'number_of_ratings', 'five_star', 'four_star',
          'three_star', 'two_star', 'one_star', 'description_length']


def read_txt(filename):
    with open(filename, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data


def string_to_int(s):
    # converts a comma separated string to int, i.e "1,500" to 1500
    try:
        number_string = s.replace(',', '')
        return int(number_string)
    except AttributeError:
        return 0


def get_precise_rating(df):
    return df.apply(
        lambda row: round((string_to_int(row.five_star) * 5 + string_to_int(row.four_star) * 4 + string_to_int(
            row.three_star) * 3 + string_to_int(row.two_star) * 2 + string_to_int(row.one_star) * 1) / string_to_int(
            row.number_of_ratings), 4) if string_to_int(row.number_of_ratings) else 0, axis=1)


def get_number_of_ratings_per_week(df):
    df['number_of_ratings'] = df['number_of_ratings'].apply(lambda x: string_to_int(x))
    return df.groupby('id')['number_of_ratings'].diff().fillna(0)


def get_mean_difference_in_list(_list):
    if len(_list) == 1:
        return 0

    diffs = np.diff(np.array(sorted(_list)))
    return round(sum(diffs) / len(diffs), 4)


def get_release_stats():
    target_metadata = pd.read_csv("data/target_meta.csv")
    target_set = pd.read_csv("data/target_set.csv")

    unique_apps_df = pd.DataFrame({'app_id': target_metadata.app_id.unique()})

    unique_apps_df['number_of_releases'] = \
        target_metadata.groupby("app_id")["release_id"].count().to_frame(name="number_of_releases").reset_index()[
            ["number_of_releases"]]

    unique_apps_df['release_weeks'] = [
        list(set(target_metadata['release_week'].loc[target_metadata['app_id'] == x['app_id']]))
        for _, x in unique_apps_df.iterrows()]
    unique_apps_df['median_release_interval'] = unique_apps_df['release_weeks'].apply(get_mean_difference_in_list)

    unique_apps_df[["rating_start", "number_of_ratings_start"]] = target_set.groupby('app_id').first().reset_index()[
        ["precise_rating", "number_of_ratings"]]
    unique_apps_df[["rating_end", "number_of_ratings_end"]] = target_set.groupby('app_id').last().reset_index()[
        ["precise_rating", "number_of_ratings"]]
    unique_apps_df["rating_change"] = unique_apps_df['rating_end'] - unique_apps_df['rating_start']
    unique_apps_df["number_of_ratings_change"] = unique_apps_df['number_of_ratings_end'] - unique_apps_df[
        'number_of_ratings_start']

    release_stats_df = unique_apps_df.drop(['release_weeks', 'rating_start', 'number_of_ratings_start'], axis=1)
    release_stats_df.to_csv("data/release_stats.csv", index=False)


def get_pre_and_post_period(df):
    u_app_id = df['app_id'].value_counts().to_dict()

    mem = u_app_id.copy()

    for k, v in mem.items():
        mem[k] = 0

    f = []
    for i in range(len(df)):
        if u_app_id[df.iloc[i, 1]] > 1:
            mem[df.iloc[i, 1]] += 1
            # last case
            if mem[df.iloc[i, 1]] == u_app_id[df.iloc[i, 1]]:
                x = df.iloc[i, :].tolist()
                x.append(df.iloc[i - 1, 2])
                x.append(52)
            # first case
            elif mem[df.iloc[i, 1]] == 1:
                x = df.iloc[i, :].tolist()
                x.append(1)
                x.append(df.iloc[i + 1, 2] - 1)
            else:
                x = df.iloc[i, :].tolist()
                x.append(df.iloc[i - 1, 2])
                x.append(df.iloc[i + 1, 2] - 1)
            f.append(x)
        else:
            x = df.iloc[i, :].tolist()
            x.append(1)
            x.append(52)
            f.append(x)
    return pd.DataFrame(f, columns=['release_id', 'app_id', 'release_week', 'pre_period', 'post_period'])


def create_control_set_for_each_metric(df):
    Path("data/control").mkdir(parents=True, exist_ok=True)

    metrics = ['precise_rating', 'number_of_ratings', 'number_of_ratings_per_week']

    for metric in metrics:
        pivoted = df.pivot(index='week_number', columns='id', values=metric).reset_index()
        pivoted.columns.name = None

        pivoted.to_csv(f"data/control/{metric}.csv", index=False)


def create_target_set_for_each_metric(df):
    Path("data/target").mkdir(parents=True, exist_ok=True)

    metrics = ['precise_rating', 'number_of_ratings', 'number_of_ratings_per_week']

    for metric in metrics:
        pivoted = df.pivot(index='week_number', columns='release_id', values=metric).reset_index()
        pivoted.columns.name = None

        pivoted.to_csv(f"data/target/{metric}.csv", index=False)


def create_control_set(df, target_app_ids):
    columns = ['id', 'week_number', 'precise_rating', 'number_of_ratings', 'number_of_ratings_per_week',
               'description_length']
    control_apps = df[~df['id'].isin(target_app_ids)]
    control_df = control_apps[columns].sort_values(["id", "week_number"])
    control_df.to_csv("data/control_set.csv", index=False)

    create_control_set_for_each_metric(control_df)


def create_target_set(df, target_app_ids):
    columns = ['id', 'week_number', 'last_update', 'precise_rating', 'number_of_ratings', 'number_of_ratings_per_week',
               'description_length']
    target_apps = df[df['id'].isin(target_app_ids)]
    target_apps = target_apps[columns].sort_values('week_number')

    target_df = target_apps.groupby(['id', 'last_update']).first().reset_index().rename(
        columns={'id': 'app_id', 'week_number': 'release_week'}).sort_values(['app_id', 'release_week'])

    # releases in week 1-3 and 50-52 don't have enough pre_period and post_period data respectively
    target_df = target_df[(target_df.release_week > 3) & (target_df.release_week < 50)]
    target_df = target_df[target_df["release_week"].diff() > 3]  # removing releases that are between three weeks
    target_df.insert(0, 'release_id', np.arange(1, target_df.shape[0] + 1))

    target_meta_df = target_df[['release_id', 'app_id', 'release_week']]
    target_meta_df = get_pre_and_post_period(target_meta_df)
    target_meta_df.to_csv("data/target_meta.csv", index=False)

    target_metrics_df = pd.merge(target_meta_df, target_apps, left_on='app_id', right_on='id', how='left')
    target_metrics_df = target_metrics_df[
        ["release_id", "app_id", "week_number", "precise_rating", "number_of_ratings", "number_of_ratings_per_week",
         "description_length"]]
    target_metrics_df.to_csv("data/target_set.csv", index=False)

    create_target_set_for_each_metric(target_metrics_df)


def get_full_set():
    full_set_header = header + ['week_number']

    root = 'data/weekly_data'
    files = sorted(os.listdir(root))
    i = 1
    x = [full_set_header]
    for file in files:
        v = file.split('.')
        print('Analyzing {}, {}/{}'.format(file, i, len(files)))
        current_week_data = os.path.join(root, file)
        data = pd.read_csv(current_week_data)
        for j in range(len(data)):
            c = data.iloc[j, :].tolist()
            c.append(int(v[0]))
            x.append(c)
        i += 1

    with open('data/full_set.csv', 'w') as fd:
        writer_object = writer(fd)
        for item in x:
            writer_object.writerow(item)


def get_sorted_full_set():
    df_full_set = pd.read_csv("data/full_set.csv")

    df_full_set.insert(0, 'id', pd.factorize(df_full_set.domain_name)[0] + 1)
    df_full_set.sort_values(by=['id', 'week_number'], ascending=True, inplace=True)

    df_full_set["precise_rating"] = get_precise_rating(df_full_set)
    df_full_set["number_of_ratings_per_week"] = get_number_of_ratings_per_week(df_full_set)

    df_full_set.to_csv("data/sorted_full_set.csv", index=False)
    print("Added ID column to the full set, sorted by ID, and saved to csv")


def get_weekly_data():
    i = 1
    root = "/path/to/kurtis_data/c"  # change this to path to kurtis data
    files = sorted(os.listdir(root))
    for file in files:
        print('Analyzing {}, {}/{}'.format(file, i, len(files)))
        data = []
        current_week_data = os.path.join(root, file)
        data_raw = read_txt(current_week_data)
        for row in data_raw:
            x = row.split('\t')
            data.append(x)

        Path("data/weekly_data").mkdir(parents=True, exist_ok=True)

        data = pd.DataFrame(data, columns=full_header)

        data['description_length'] = data['description'].str.len()

        data = data[header]
        data.to_csv('data/weekly_data/' + str(i) + '.csv', index=False)
        i += 1


def get_control_and_target_sets():
    df = pd.read_csv("data/sorted_full_set.csv")
    releases = df.groupby('id').apply(lambda x: x['last_update'].unique()).reset_index()
    target_app_ids = releases.loc[releases[0].str.len() > 1, 'id'].tolist()

    create_control_set(df, target_app_ids)
    create_target_set(df, target_app_ids)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--get_weekly_data", action="store_true", help="Get weekly data from the data source")
    parser.add_argument("--get_full_set", action="store_true", help="Get full set over all weeks")
    parser.add_argument("--get_sorted_full_set", action="store_true", help="Add id column, sort by it, and save to csv")
    parser.add_argument("--get_release_stats", action="store_true", help="Release count and median interval")
    args = parser.parse_args()

    if args.get_weekly_data:
        get_weekly_data()
    elif args.get_full_set:
        get_full_set()
    elif args.get_sorted_full_set:
        get_sorted_full_set()
    elif args.get_release_stats:
        get_release_stats()
    else:
        get_weekly_data()
        get_full_set()
        get_sorted_full_set()
        get_control_and_target_sets()
        get_release_stats()
