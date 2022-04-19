import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


control_number_of_rating_per_week = pd.read_csv('data/control/number_of_ratings_per_week.csv', delimiter=',')
control_number_of_ratings = pd.read_csv('data/control/number_of_ratings.csv', delimiter=',')
control_precise_rating = pd.read_csv('data/control/precise_rating.csv', delimiter=',')

control_description_length = pd.read_csv('data/control/description_length.csv') 

target_number_of_rating_per_week = pd.read_csv('data/target/number_of_ratings_per_week.csv', delimiter=',')
target_number_of_ratings = pd.read_csv('data/target/number_of_ratings.csv', delimiter=',')
target_precise_rating = pd.read_csv('data/target/precise_rating.csv', delimiter=',')

target_description_length = pd.read_csv('data/target/description_length.csv') 


print("control_number_of_rating_per_week: {}".format(control_number_of_rating_per_week.shape))
print("control_number_of_ratings: {}".format(control_number_of_ratings.shape))
print("control_precise_rating: {}".format(control_precise_rating.shape))
print("target_number_of_rating_per_week: {}".format(target_number_of_rating_per_week.shape))
print("target_number_of_ratings: {}".format(target_number_of_ratings.shape))
print("target_precise_rating: {}".format(target_precise_rating.shape))

# control_number_of_rating_per_week = control_number_of_rating_per_week.iloc[:, : 10000]
# control_number_of_ratings = control_number_of_ratings.iloc[:, : 10000]
# control_precise_rating = control_precise_rating.iloc[:, : 10000]

# target_number_of_rating_per_week = target_number_of_rating_per_week.iloc[:, : 20000]
# target_number_of_ratings = target_number_of_ratings.iloc[:, : 20000]
# target_precise_rating = target_precise_rating.iloc[:, : 20000]

# full_set = pd.concat([target_precise_rating, control_precise_rating], axis=1)

########################################AVERAGE RATING#############################################

full_set = pd.concat([target_precise_rating, control_precise_rating], axis=1)

full_set_std = np.std(full_set, axis=0)
full_set_std = pd.DataFrame(full_set_std, columns=['Full set'])

targets_std = np.std(target_precise_rating, axis=0)
targets_std = pd.DataFrame(targets_std, columns=['Target set'])

controls_std = np.std(control_precise_rating, axis=0)
controls_std = pd.DataFrame(controls_std,  columns=['Control set'])

full_set_std = full_set_std.reset_index(drop=True)
targets_std = targets_std.reset_index(drop=True)
controls_std = controls_std.reset_index(drop=True)

data_std = pd.concat([full_set_std, controls_std, targets_std], axis=0)

df = pd.DataFrame(data=data_std)

fig, ax = plt.subplots()
boxplot = sns.boxplot(data=df, notch=True, showfliers = False, ax=ax, palette="Blues")
boxplot.set_ylabel("Standard deviation of ratings", fontsize=14)
plt.savefig('results/RQ1/R.png')

#######################################NUMBER OF RATINGS##############################################

full_set = pd.concat([target_number_of_ratings, control_number_of_ratings], axis=1)

full_set_std = np.std(full_set, axis=0)
full_set_std = pd.DataFrame(full_set_std, columns=['Full set'])

targets_std = np.std(target_number_of_ratings, axis=0)
targets_std = pd.DataFrame(targets_std, columns=['Target set'])

controls_std = np.std(control_number_of_ratings, axis=0)
controls_std = pd.DataFrame(controls_std,  columns=['Control set'])

full_set_std = full_set_std.reset_index(drop=True)
targets_std = targets_std.reset_index(drop=True)
controls_std = controls_std.reset_index(drop=True)

data_std = pd.concat([full_set_std, controls_std, targets_std], axis=0)

df = pd.DataFrame(data=data_std)

fig, ax = plt.subplots()
boxplot = sns.boxplot(data=df, notch=True, showfliers = False, ax=ax, palette="Blues")
boxplot.set_ylabel("Standard deviation of number of ratings", fontsize=14)
plt.savefig('results/RQ1/N.png')

#######################################NUMBER OF RATINGS PER WEEK##############################################

full_set = pd.concat([target_number_of_rating_per_week, control_number_of_rating_per_week], axis=1)

full_set_std = np.std(full_set, axis=0)
full_set_std = pd.DataFrame(full_set_std, columns=['Full set'])

targets_std = np.std(target_number_of_rating_per_week, axis=0)
targets_std = pd.DataFrame(targets_std, columns=['Target set'])

controls_std = np.std(control_number_of_rating_per_week, axis=0)
controls_std = pd.DataFrame(controls_std,  columns=['Control set'])

full_set_std = full_set_std.reset_index(drop=True)
targets_std = targets_std.reset_index(drop=True)
controls_std = controls_std.reset_index(drop=True)

data_std = pd.concat([full_set_std, controls_std, targets_std], axis=0)

df = pd.DataFrame(data=data_std)

fig, ax = plt.subplots()
boxplot = sns.boxplot(data=df, notch=True, showfliers = False, ax=ax, palette="Blues")
boxplot.set_ylabel("Standard deviation of number of ratings per week", fontsize=14)
plt.savefig('results/RQ1/NW.png')

#######################################DESCRIPTION LENGTH##############################################

full_set = pd.concat([target_description_length, control_description_length], axis=1)

full_set_std = np.std(full_set, axis=0)
full_set_std = pd.DataFrame(full_set_std, columns=['Full set'])

targets_std = np.std(target_description_length, axis=0)
targets_std = pd.DataFrame(targets_std, columns=['Target set'])

controls_std = np.std(control_description_length, axis=0)
controls_std = pd.DataFrame(controls_std,  columns=['Control set'])

full_set_std = full_set_std.reset_index(drop=True)
targets_std = targets_std.reset_index(drop=True)
controls_std = controls_std.reset_index(drop=True)

data_std = pd.concat([full_set_std, controls_std, targets_std], axis=0)

df = pd.DataFrame(data=data_std)

fig, ax = plt.subplots()
boxplot = sns.boxplot(data=df, notch=True, showfliers = False, ax=ax, palette="Blues")
boxplot.set_ylabel("Standard deviation of description length", fontsize=14)
plt.savefig('results/RQ1/L.png')