# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:42:46 2023

@author: phata
"""

import pandas as pd
import numpy as np

df_dbd = (pd
          # Try to change to github
          .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_firms_est_and_dis_2.csv', 
                    parse_dates = True)
          .drop(columns = ['obj_code', 'subsector'],
                axis = 1)
          )

df_established = df_dbd.query('type == "Established"').groupby(['date'])['type'].count().rename('n_established')
df_dissolved = df_dbd.query('type == "Dissolved"').groupby(['date'])['type'].count().rename('n_dissolved')
df_est_and_dis = pd.concat([df_established, df_dissolved], axis = 1)
print(df_est_and_dis)

# Add column: southern
li_southern = ['Chumphon', 'Krabi', 'Nakhon Si Thammarat', 'Narathiwat', 'Pattani', 'Phang Nga', 'Phatthalung', 'Phuket', 'Ranong', 'Satun', 'Songkhla', 'Surat Thani', 'Trang', 'Yala']
southern = []
for row in df_dbd['province']:
    if row in li_southern:
        southern.append(True)
    else:
        southern.append(False)
df_dbd['southern'] = southern

EST_ALL_WK = sorted(df_dbd.query('type == "Established"')['registered_capital'].to_list())
EST_ALL_SOUTH = sorted(df_dbd.query('southern == True & type == "Established" & province != "Songkhla"')['registered_capital'].to_list())
EST_ALL_SONG = sorted(df_dbd.query('type == "Established" & province == "Songkhla"')['registered_capital'].to_list())

DIS_ALL_WK = sorted(df_dbd.query('type == "Dissolved"')['registered_capital'].to_list())
DIS_ALL_SOUTH = sorted(df_dbd.query('southern == True & type == "Dissolved" & province != "Songkhla"')['registered_capital'].to_list())
DIS_ALL_SONG = sorted(df_dbd.query('type == "Dissolved" & province == "Songkhla"')['registered_capital'].to_list())

df = pd.concat([pd.DataFrame({'EST_ALL_WK': EST_ALL_WK}),
           pd.DataFrame({'EST_ALL_SOUTH': EST_ALL_SOUTH}),
           pd.DataFrame({'EST_ALL_SONG': EST_ALL_SONG}),
           pd.DataFrame({'DIS_ALL_WK': DIS_ALL_WK}),
           pd.DataFrame({'DIS_ALL_SOUTH': DIS_ALL_SOUTH}),
           pd.DataFrame({'DIS_ALL_SONG': DIS_ALL_SONG})
           ],
          axis = 1)

df.to_csv('C:\\Users\\phata\\Documents\\GitHub\\econvis\\gini_prep.csv', index=False)