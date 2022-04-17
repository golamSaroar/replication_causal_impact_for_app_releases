import os
from csv import writer
import pandas as pd
from pathlib import Path
import argparse

header = ['domain_name', 'app_name', 'developer', 'email', 'price', 'last_update', 'category', 'size',
          'number_of_installs', 'version', 'compatibility', 'maturity_rating', 'app_store_purchases', 'rating',
          'number_of_ratings', 'five_star', 'four_star', 'three_star', 'two_star', 'one_star', 'link', 'description',
          'release_text']


def read_txt(filename):
    with open(filename, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data


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
    df_full_set.sort_values(by=['id'], ascending=True, inplace=True)
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
        data_raw = data_raw[0:1000]
        data.append(header)
        for row in data_raw:
            x = row.split('\t')
            data.append(x)

        Path("data/weekly_data").mkdir(parents=True, exist_ok=True)

        with open('data/weekly_data/' + str(i) + '.csv', 'w') as fd:  # change this
            writer_object = writer(fd)
            for x in data:
                writer_object.writerow(x)
        i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--get_weekly_data", action="store_true", help="Get weekly data from the data source")
    parser.add_argument("--get_full_set", action="store_true", help="Get full set over all weeks")
    parser.add_argument("--get_sorted_full_set", action="store_true", help="Add id column, sort by it, and save to csv")
    args = parser.parse_args()

    if args.get_weekly_data:
        get_weekly_data()
    elif args.get_full_set:
        get_full_set()
    elif args.get_sorted_full_set:
        get_sorted_full_set()
    else:
        print("You have not passed any argument. Type --help or -h to see the accepted arguments.")
