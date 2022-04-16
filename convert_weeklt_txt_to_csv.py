
import os
from csv import writer
import random

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data
        

def main():
    i = 1
    root = 'path/to/your/data/files' # please change this directory
    files = sorted(os.listdir(root))
    for file in files:
        header = ['domain_name', 'app_name', 'developer', 'email', 'price', 'last_update', 'category', 'size', 'number_of_installs', 'version', 'compatibility', 'maturity_rating', 'app_store_purchases', 'rating', 'number_of_ratings', 'five_star', 'four_star', 'three_star', 'two_star', 'one_star', 'link','description', 'release_text']
        print('Analyzing {}, {}/{}'.format(file, i, len(files)))
        data = []
        current_week_data = os.path.join(root, file)
        data_raw = read_txt(current_week_data)
        data_raw = random.choices(data_raw, k=1000)
        data.append(header)
        for row in data_raw:
            x = row.split('\t')
            data.append(x)
        with open('./dataset/weekly_extracted/'+str(i)+'.csv', 'w') as fd:
            writer_object = writer(fd)
            for x in data:
                writer_object.writerow(x)
        i += 1

        

if __name__ == '__main__':
    main()
