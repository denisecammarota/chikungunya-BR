# Cleaning data for all places of the country SINAN CHIKUNGUNYA
# only confirmed cases, assign year and week of first symptoms 
# years 2014 to 2024
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob

files = glob.glob('Data/processed/*.csv')
id_municip_real = '354850' # santos
id_municip_real = '355030' #sp
id_municip_real = '330455' #rj
data_total = pd.DataFrame()


for file in files:
    # reading data 
    data_test = pd.read_csv(file, 
                            delimiter = ';',
                            index_col=False,
                            parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
    data_test = data_test.drop(columns = ['Unnamed: 0'])
    data_test['ID_MN_RESI'] = data_test['ID_MN_RESI'].astype(str)
    filt_df1 = (data_test['ID_MN_RESI'] == id_municip_real)
    data_filtered_1 = data_test[filt_df1]
    data_filtered_1['YEAR_PRI'] = data_filtered_1['SEM_PRI'].str[0:4]
    data_filtered_1['WEEK_PRI'] = data_filtered_1['SEM_PRI'].str[4:]
    if data_filtered_1.empty == False:
        data_total = data_total.append(data_filtered_1)

data_total['CASES'] = 1
print(data_total['ID_MN_RESI'].unique())
data_total = data_total.groupby(['WEEK_PRI','YEAR_PRI'])['CASES'].sum()
data_total = data_total.reset_index(name = 'CASES')


data_total.to_csv('chik_rj.csv', sep=';')


