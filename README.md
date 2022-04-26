# Replication: Causal Impact Analysis for App Releases in Google Play
This repository contains code for the replication of the paper [Causal Impact Analysis for App Releases in Google Play](http://www0.cs.ucl.ac.uk/staff/F.Sarro/resource/papers/Martin_FSE_Causal_PrePrint.pdf).

## Requirements

The easiest way to set up is creating a virtualenv and installing the requirements in it.  
Create a conda environment:

```
conda create --name myenv python=3.7
```

To install requirements:

```
pip install -r requirements.txt
```

## Getting Data
The dataset was provided by the course supervisor. We do not have permission to share the data. Besides, the data is too large for uploading on GitHub anyway (8GB). Assuming that you have access to the data, change the path on line 214 in `prepare_data.py` to the data folder.

```
root = "/path/to/kurtis_data/c"
```

To perform data preprocessing, feature selection, and feature generation, run this command:

```
python prepare_data.py
```

All the required data will be preprocessed and stored in the `/data` directory. The output will be as follows:  

- `/weekly_data`: contains 52 csv files, each containing app information for a particular week.
- `full_set.csv`: concatenation of all 52 files in a single csv file  
- `sorted_full_set.csv`: sorting items by week number, adding auto-incremented app id, and adding two attributes: "precise_rating" and "number_of_ratings_per_week".  
- `control_set.csv`: the apps that belong to control set  
- `target_set.csv`: the releases in the target set  
- `target_meta.csv`: release metadata (number of releases, median interval between releases, release week, pre-period, post-period)  
- `/control`: directory contains one csv file per each metric for apps in the control set  
- `/target`: directory contains one csv file per each metric for releases in the target set

You can also generate these files and folders separately (if needed) by passing the right argument in the command, for example:

```
python prepare_data.py --get_weekly_data
python prepare_data.py --get_full_set
python prepare_data.py --get_sorted_full_set
python prepare_data.py --get_release_stats
```

## Replication Results

Now that all the required data is generated, please refer to [this notebook](https://colab.research.google.com/drive/1xyhYa_FWktcyLxdPict5oCRvACyoSSNK?usp=sharing) which uses this data and presents the replication results.


> Thank You!
