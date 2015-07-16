import os
import numpy as np
import pandas as pd

directory = 'C:/Users/David/workspace/concerts/'

os.chdir(directory)

boData = pd.read_csv('data/BoxOfficeData.csv')