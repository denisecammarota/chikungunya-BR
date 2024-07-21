import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import geopandas as gpd
import geobr
import os
import glob
import imageio   

map_br = geobr.read_municipality()
map_br['code_muni'] = map_br['code_muni'].astype(str).str[0:6]

pop_br = pd.read_csv('D:/Code/Dengue_BR/Data/municipalities.csv')
pop_br = pop_br[['municipio','pop_21']]
pop_br['municipio'] = pop_br['municipio'].astype(str).str[0:6]


map_br = map_br.merge(pop_br, how = 'left', left_on = 'code_muni', right_on = 'municipio')

max_scale = []
min_scale = []


years = np.arange(2015,2025,1)

files = glob.glob('Data/processed/*.csv')


# Plotting ocurrence maps #####################################################

ind = 0

for file in files:
    df_year = pd.read_csv(file, delimiter = ';')
    if(years[ind] >= 2007):
        df_year['YEAR'] = df_year['SEM_PRI'].astype(str).str[0:4]
    else:
        df_year['YEAR'] = df_year['SEM_PRI'].astype(str).str[2:]
    df_year['ID_MN_RESI'] = df_year['ID_MN_RESI'].astype(str).str[0:6]
    df_year['YEAR'] = df_year['YEAR'].astype(int)
    df_year = df_year[df_year['YEAR'] == years[ind]]
    df_year['CASES'] = 1
    df_year_grouped = df_year.groupby(['ID_MN_RESI'])['CASES'].sum()
    df_year_grouped = df_year_grouped.reset_index(name = 'CASES')
    map_year = map_br.copy()
    map_year = map_year.merge(df_year_grouped, how = 'left', left_on = 'code_muni', right_on = 'ID_MN_RESI')
    map_year['CASES_100K'] = (10**5)*(map_year['CASES']/map_year['pop_21'])
    map_year['OCURRENCE'] = np.where(map_year['CASES'] >= 1, 1, 0)
    missing_kwds = dict(color='grey', label='No Data')
    fig, axs = plt.subplots(figsize = (12,12))
    map_year.plot(
                 ax=axs, 
                 column='OCURRENCE', 
                 missing_kwds=missing_kwds,
                 edgecolor = 'black',
                 linewidth = 0.10,
                 cmap = 'Reds',
             )
    axs.set_title(
            str(years[ind]),
            fontdict={"fontsize": 25},
        )
    axs.axis("off") 
    plt.tight_layout()
    max_scale.append(np.nanmax(map_year['CASES_100K']))
    min_scale.append(np.nanmin(map_year['CASES_100K']))
    plt.savefig('Figs/ocurrence_'+str(years[ind])+'.png',bbox_inches='tight')
    ind = ind + 1

max_total = np.nanmax(np.array(max_scale)) # 30218.205862905
min_total = np.nanmin(np.array(min_scale)) # 0.06700032830160867


files_plots = glob.glob('Figs/ocurrence/*.png')

with imageio.get_writer('ocurrence_time.gif', fps=1) as writer:    # inputs: filename, frame per second
    for filename in files_plots:
        image = imageio.imread(filename)                         # load the image file
        writer.append_data(image)                                # append the image file
print('Gif saved!\n')


# Doing the same for the southern states ######################################


ind = 0

for file in files:
    df_year = pd.read_csv(file, delimiter = ';')
    if(years[ind] >= 2007):
        df_year['YEAR'] = df_year['SEM_PRI'].astype(str).str[0:4]
    else:
        df_year['YEAR'] = df_year['SEM_PRI'].astype(str).str[2:]
    df_year['ID_MN_RESI'] = df_year['ID_MN_RESI'].astype(str).str[0:6]
    df_year['YEAR'] = df_year['YEAR'].astype(int)
    df_year = df_year[df_year['YEAR'] == years[ind]]
    df_year['CASES'] = 1
    df_year_grouped = df_year.groupby(['ID_MN_RESI'])['CASES'].sum()
    df_year_grouped = df_year_grouped.reset_index(name = 'CASES')
    map_year = map_br.copy()
    map_year = map_year.merge(df_year_grouped, how = 'left', left_on = 'code_muni', right_on = 'ID_MN_RESI')
    map_year['CASES_100K'] = (10**5)*(map_year['CASES']/map_year['pop_21'])
    map_year['OCURRENCE'] = np.where(map_year['CASES'] >= 1, 1, 0)
    map_year = map_year[map_year['abbrev_state'].isin(['PR','SC','RS'])]
    missing_kwds = dict(color='grey', label='No Data')
    fig, axs = plt.subplots(figsize = (12,12))
    map_year.plot(
                 ax=axs, 
                 column='OCURRENCE', 
                 missing_kwds=missing_kwds,
                 edgecolor = 'black',
                 linewidth = 0.10,
                 cmap = 'Reds',
             )
    axs.set_title(
            str(years[ind]),
            fontdict={"fontsize": 25},
        )
    axs.axis("off") 
    plt.tight_layout()
    #max_scale.append(np.nanmax(map_year['CASES_100K']))
    #min_scale.append(np.nanmin(map_year['CASES_100K']))
    plt.savefig('D:/Code/Dengue_BR/Figs/ocurrence-south/ocurrence_south_'+str(years[ind])+'.png',bbox_inches='tight')
    ind = ind + 1


files_plots = glob.glob('D:/Code/Dengue_BR/Figs/ocurrence-south/*.png')

with imageio.get_writer('ocurrence_time_south.gif', fps=1) as writer:    # inputs: filename, frame per second
    for filename in files_plots:
        image = imageio.imread(filename)                         # load the image file
        writer.append_data(image)                                # append the image file
print('Gif saved!\n')


# Plotting incidence maps #####################################################
# incidence with scale year by year, by log

ind = 0

for file in files:
    df_year = pd.read_csv(file, delimiter = ';')
    if(years[ind] >= 2007):
        df_year['YEAR'] = df_year['SEM_PRI'].astype(str).str[0:4]
    else:
        df_year['YEAR'] = df_year['SEM_PRI'].astype(str).str[2:]
    df_year['ID_MN_RESI'] = df_year['ID_MN_RESI'].astype(str).str[0:6]
    df_year['YEAR'] = df_year['YEAR'].astype(int)
    df_year = df_year[df_year['YEAR'] == years[ind]]
    df_year['CASES'] = 1
    df_year_grouped = df_year.groupby(['ID_MN_RESI'])['CASES'].sum()
    df_year_grouped = df_year_grouped.reset_index(name = 'CASES')
    map_year = map_br.copy()
    map_year = map_year.merge(df_year_grouped, how = 'left', left_on = 'code_muni', right_on = 'ID_MN_RESI')
    map_year['CASES_100K'] = (10**5)*(map_year['CASES']/map_year['pop_21'])
    map_year['CASES_100K_LOG'] = np.log(map_year['CASES_100K'])
    map_year['CASES_100K_LOG'] = map_year['CASES_100K_LOG'].fillna(-3)
    map_year['OCURRENCE'] = np.where(map_year['CASES'] >= 1, 1, 0)
    missing_kwds = dict(color='grey', label='No Data')
    fig, axs = plt.subplots(figsize = (12,12))
    map_year.plot(
                 ax=axs, 
                 column='CASES_100K_LOG', 
                 missing_kwds=missing_kwds,
                 edgecolor = 'black',
                 linewidth = 0.10,
                 cmap = 'Reds',
             )
    axs.set_title(
            str(years[ind]),
            fontdict={"fontsize": 25},
        )
    cax = fig.add_axes(
        [
            0.82,    # posicao x (entre 0.0 e 1.0)
            0.18,    # posicao y (entre 0.0 e 1.0)
            0.03,    # largura x
            0.40,    # altura y
        ]
    )
    sm = plt.cm.ScalarMappable(
        cmap="Reds",                                       
        norm=plt.Normalize(
            vmin=np.log(min_total),  
            vmax=np.log(max_total),  
        ),
    )
    fig.colorbar(
    sm,
    cax=cax)
    cax.set_ylabel('Incidence per 100.000 inhabitants (Log)', rotation=90, fontsize = 14)
    axs.axis("off") 
    plt.tight_layout()
    plt.savefig('Figs/incidence/incidence_'+str(years[ind])+'.png',bbox_inches='tight')
    ind = ind + 1

files_plots = glob.glob('Figs/incidence/*.png')

with imageio.get_writer('incidence_time.gif', fps=1) as writer:    # inputs: filename, frame per second
    for filename in files_plots:
        image = imageio.imread(filename)                         # load the image file
        writer.append_data(image)                                # append the image file
print('Gif saved!\n')

# Plotting incidence maps for the south #######################################

ind = 0

for file in files:
    df_year = pd.read_csv(file, delimiter = ';')
    if(years[ind] >= 2007):
        df_year['YEAR'] = df_year['SEM_PRI'].astype(str).str[0:4]
    else:
        df_year['YEAR'] = df_year['SEM_PRI'].astype(str).str[2:]
    df_year['ID_MN_RESI'] = df_year['ID_MN_RESI'].astype(str).str[0:6]
    df_year['YEAR'] = df_year['YEAR'].astype(int)
    df_year = df_year[df_year['YEAR'] == years[ind]]
    df_year['CASES'] = 1
    df_year_grouped = df_year.groupby(['ID_MN_RESI'])['CASES'].sum()
    df_year_grouped = df_year_grouped.reset_index(name = 'CASES')
    map_year = map_br.copy()
    map_year = map_year.merge(df_year_grouped, how = 'left', left_on = 'code_muni', right_on = 'ID_MN_RESI')
    map_year['CASES_100K'] = (10**5)*(map_year['CASES']/map_year['pop_21'])
    map_year['CASES_100K_LOG'] = np.log(map_year['CASES_100K'])
    map_year['CASES_100K_LOG'] = map_year['CASES_100K_LOG'].fillna(-3)
    map_year['OCURRENCE'] = np.where(map_year['CASES'] >= 1, 1, 0)
    map_year = map_year[map_year['abbrev_state'].isin(['PR','SC','RS'])]
    missing_kwds = dict(color='grey', label='No Data')
    fig, axs = plt.subplots(figsize = (12,12))
    map_year.plot(
                 ax=axs, 
                 column='CASES_100K_LOG', 
                 missing_kwds=missing_kwds,
                 edgecolor = 'black',
                 linewidth = 0.10,
                 cmap = 'Reds',
             )
    axs.set_title(
            str(years[ind]),
            fontdict={"fontsize": 25},
        )
    cax = fig.add_axes(
        [
            0.82,    # posicao x (entre 0.0 e 1.0)
            0.18,    # posicao y (entre 0.0 e 1.0)
            0.03,    # largura x
            0.40,    # altura y
        ]
    )
    sm = plt.cm.ScalarMappable(
        cmap="Reds",                                       
        norm=plt.Normalize(
            vmin=np.log(min_total),  
            vmax=np.log(max_total),  
        ),
    )
    fig.colorbar(
    sm,
    cax=cax)
    cax.set_ylabel('Incidence per 100.000 inhabitants (Log)', rotation=90, fontsize = 14)
    axs.axis("off") 
    plt.tight_layout()
    plt.savefig('D:/Code/Dengue_BR/Figs/incidence-south/incidence_south_'+str(years[ind])+'.png',bbox_inches='tight')
    ind = ind + 1

files_plots = glob.glob('D:/Code/Dengue_BR/Figs/incidence-south/*.png')

with imageio.get_writer('incidence_south_time.gif', fps=1) as writer:    # inputs: filename, frame per second
    for filename in files_plots:
        image = imageio.imread(filename)                         # load the image file
        writer.append_data(image)                                # append the image file
print('Gif saved!\n')

