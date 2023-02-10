# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:42:46 2023

@author: phata
"""

import pandas as pd

df_dbd = (pd
          # Try to change to github
          .read_csv('C:\\Users\\phata\\Documents\\GitHub\\econvis\\data\\tha_firms_est_and_dis.csv', 
                    parse_dates = True)
          .drop(columns = ['obj_code', 'subsector'],
                axis = 1)
          )

df_established = df_dbd.query('type == "Established"').groupby(['date'])['type'].count().rename('n_established')
df_dissolved = df_dbd.query('type == "Dissolved"').groupby(['date'])['type'].count().rename('n_dissolved')
df_est_and_dis = pd.concat([df_established, df_dissolved], axis = 1)
print(df_est_and_dis)

li_southern = ['Chumphon', 'Krabi', 'Nakhon Si Thammarat', 'Narathiwat', 'Pattani', 'Phang Nga', 'Phatthalung', 'Phuket', 'Ranong', 'Satun', 'Songkhla', 'Surat Thani', 'Trang', 'Yala']
southern = []
for row in df_dbd['province']:
    if row in li_southern:
        southern.append(True)
    else:
        southern.append(False)
df_dbd['southern'] = southern
print(df_dbd)         

df_dbd.query('southern == True')['province'].unique()

