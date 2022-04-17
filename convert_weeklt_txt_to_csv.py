
import os
from csv import writer
import pandas as pd
import numpy as np

headers = ['domain_name', 'app_name', 'developer', 'email', 'price', 'last_update', 'category', 'size', 'number_of_installs', 'version', 'compatibility', 'maturity_rating', 'app_store_purchases', 'rating', 'number_of_ratings', 'five_star', 'four_star', 'three_star', 'two_star', 'one_star', 'link','description', 'release_text']

full_headers = ['domain_name', 'app_name', 'developer', 'email', 'price', 'last_update', 'category', 'size', 'number_of_installs', 'version', 'compatibility', 'maturity_rating', 'app_store_purchases', 'rating', 'number_of_ratings', 'five_star', 'four_star', 'three_star', 'two_star', 'one_star', 'link','description', 'release_text', 'week_number']

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

def concat_data():
    root = '/path/to/weekly_extracted/data' # change this
    files = sorted(os.listdir(root))
    i = 1
    x = []
    x.append(full_headers)
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

    with open('./dataset/fullset.csv', 'w') as fd: # change this
        writer_object = writer(fd)
        for item in x:
            writer_object.writerow(item)

def main():
    i = 1
    root = "" # path to kurtis data
    files = sorted(os.listdir(root))
    for file in files: 
        print('Analyzing {}, {}/{}'.format(file, i, len(files)))
        data = []
        current_week_data = os.path.join(root, file)
        data_raw = read_txt(current_week_data)
        data_raw = data_raw[0:1000]
        data.append(headers)
        for row in data_raw:
            x = row.split('\t')
            data.append(x)
        with open('./dataset/weekly_extracted/'+str(i)+'.csv', 'w') as fd: # change this
            writer_object = writer(fd)
            for x in data:
                writer_object.writerow(x)
        i += 1

        

if __name__ == '__main__':
    #main()
    #concat_data()
