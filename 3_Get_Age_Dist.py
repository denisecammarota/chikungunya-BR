# Cleaning data for all places of the country SINAN CHIKUNGUNYA
# only confirmed cases, assign year and week of first symptoms 
# years 2014 to 2024, to get age distribution
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob


# decoficando a idade do SINAN, pego do pySUS
@np.vectorize
def decodifica_idade_SINAN(idade, unidade: str = "Y"):
    """
    Em tabelas do SINAN frequentemente a idade é representada como um inteiro que precisa ser parseado
    para retornar a idade em uma unidade cronológica padrão.
    :param unidade: unidade da idade: 'Y': anos, 'M' meses, 'D': dias, 'H': horas
    :param idade: inteiro ou sequencia de inteiros codificados.
    :return:
    """
    fator = {"Y": 1.0, "M": 12.0, "D": 365.0, "H": 365 * 24.0}
    idade = int(idade)
    if idade >= 4000:  # idade em anos
        idade_anos = idade - 4000
    elif idade >= 3000 and idade < 4000:  # idade em meses
        idade_anos = (idade - 3000) / 12.0
    elif idade >= 2000 and idade < 3000:  # idade em dias
        idade_anos = (idade - 2000) / 365.0
    elif idade >= 1000 and idade < 2000:  # idade em horas
        idade_anos = (idade - 1000) / (365 * 24.0)
    else:
        idade_anos = np.nan
    idade_dec = idade_anos * fator[unidade]
    return idade_dec


def process_age_serotype():
    years = np.arange(2015,2024,1)
    data_total = pd.DataFrame()
    for year in years:
        file_path = 'Data/processed/chik_BR_'+str(year)+'.csv'
        data_test = pd.read_csv(file_path, 
                                delimiter = ';',
                                index_col=False,
                                parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
        data_test['ANO'] = pd.DatetimeIndex(data_test['DT_SIN_PRI']).year 
    
        # filtering the death cases (19/07)    
        # data_test = data_test[data_test['EVOLUCAO'].isin([2,'2'])]
        print(year)
        print(data_test.shape)
        #data_test = data_test[data_test['ID_MN_RESI'] == ]
        
        # first column is read differently
        df = data_test.copy()
        
        # decodificar idade SINAN
        df['NU_IDADE_N'] = decodifica_idade_SINAN(df['NU_IDADE_N'])
        
        # group by age, serotype and separate by age groups
        df = df[['NU_IDADE_N','ANO','ID_MN_RESI']]
        #a = df[df['ID_MN_RESI'] == 355030]
        #print(sum(a['ANO'] == year))
        data_total = pd.concat([data_total,df])
    return data_total

data_total = process_age_serotype()
data_total = data_total.reset_index()
age_groups = np.array([0,4,9,14,19,29,39,49,59,69,79,120]) # age groups of tabnet datasus
data_total['age_range'] = data_total.groupby(['ANO','ID_MN_RESI','NU_IDADE_N'])[['NU_IDADE_N']].transform(lambda x: pd.cut(x, bins = age_groups).astype(str))
print('here')
data_total.to_csv('Data/chik_BR_ageclasses.csv', sep = ';')
print('here')
