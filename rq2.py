# #RQ2
import numpy as np
import pandas as pd


from scipy import stats

data = pd.read_csv('data/release_stats.csv', delimiter=',')

raw_data = data[data.columns[3:7]]

[n, N] = np.shape(raw_data)
metrics = ['R', 'Delta R', 'N', 'Delta N']

for i in range(N):
  print("Spearman: Quantity vs {}".format(metrics[i]))
  print(stats.spearmanr(data.iloc[:, 1], raw_data.iloc[:, i]))
  print("Spearman: Median Interval vs {}".format(metrics[i]))
  print(stats.spearmanr(data.iloc[:, 2], raw_data.iloc[:, i]))

print('###########################Spearsman######################################')

for i in range(N):
  print("Pearson: Quantity vs {}".format(metrics[i]))
  print(stats.pearsonr(data.iloc[:, 1], raw_data.iloc[:, i]))
  print("Pearson: Median Interval vs {}".format(metrics[i]))
  print(stats.pearsonr(data.iloc[:, 2], raw_data.iloc[:, i]))


# release_count = ratings.groupby([0]).size().reset_index(name='count')

# group = ratings.groupby([0])

# ratings_per_app = group.apply(lambda x: x[56].unique())

# delta_r = group.apply(lambda x: x[57].unique())

# [n, N] = ratings.shape

# uval = np.unique(ratings.iloc[:, 0])

# median_interval = []
# for i in range(len(uval)):
#   x = list(ratings.loc[ratings[0] == ratings.iloc[i, 0], 2])
#   if len(x) == 1:
#     median_interval.append(0)
#   else:
#     median_interval.append(np.median([j-i for i, j in zip(x[:-1], x[1:])]))


# release_count = np.asfarray(release_count.iloc[:, 1])

# ratings_per_app = pd.DataFrame(ratings_per_app)

# rat = []
# for i in range(len(ratings_per_app)):
#   rat.append(float(ratings_per_app.iloc[i, 0]))
    
# ratings = np.asfarray(rat)

# delta_r = pd.DataFrame(delta_r)

# d = []
# for i in range(len(delta_r)):
#   d.append(float(delta_r.iloc[i, 0]))
    
# delta = np.asfarray(d)
# median_int = np.asfarray(median_interval)
    
# x = [release_count, ratings, delta]
# y = [median_int, ratings, delta]

# print(stats.pearsonr(x[0], x[1]))
# print(stats.pearsonr(x[0], x[2]))
# print(stats.pearsonr(y[0], y[1]))
# print(stats.pearsonr(y[0], y[2]))
# print('########################')
# print(stats.spearmanr(x[0], x[1]))
# print(stats.spearmanr(x[0], x[2]))
# print(stats.spearmanr(y[0], y[1]))
# print(stats.spearmanr(y[0], y[2]))