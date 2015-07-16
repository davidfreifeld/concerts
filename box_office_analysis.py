import os
import numpy as np
import pandas as pd

directory = 'C:/Users/David/workspace/concerts/'

# read in the data
os.chdir(directory)
boData = pd.read_csv('data/BoxOfficeData.csv')

# convert string dates to datetime format
boData['Date'] = pd.to_datetime(boData['Date'])

# fix discrepancies in Sold Out / Total Shows
bZeroTS = boData['TotalShows'] == 0
bSORatioOne = boData['SoldRatio'] == 1
boData.ix[bZeroTS, 'TotalShows'] = 1
boData.ix[bZeroTS & bSORatioOne, "SoldOutShows"] = 1
boData.ix[bZeroTS & ~bSORatioOne, "SoldOutShows"] = 0

bGreaterSoldOut = boData['SoldOutShows'] > boData['TotalShows']
boData.ix[bGreaterSoldOut, 'SoldOutShows'] = \
    boData.ix[bGreaterSoldOut, 'TotalShows'] * boData.ix[bGreaterSoldOut, 'SoldRatio']

boData.ix[boData['TotalShows'] > 100, 'TotalShows'] = 1

# remove entries with zero for SoldRatio
boData = boData.ix[boData['SoldRatio'] != 0]

# remove entries with SoldRatio greater than one, after adjusting capacity for number of shows
bSuperSORatio = boData['SoldRatio'] > 1
boData.ix[bSuperSORatio, 'Capacity'] = boData.ix[bSuperSORatio, 'Capacity'] * boData.ix[bSuperSORatio, 'TotalShows']
boData['SoldRatio'] = boData['Sold'] / boData['Capacity']
boData = boData.ix[boData['SoldRatio'] <= 1.0]