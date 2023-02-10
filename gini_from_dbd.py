# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:42:46 2023

@author: phata
"""

import pandas as pd

df_dbd = (pd
          .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_firms_est_and_dis.csv', 
                    parse_dates = True)
          .drop(columns = ['obj_code', 'subsector'],
                axis = 1)
          )

df_established = df_dbd.query('type == "Established"').groupby(['date'])['type'].count().rename('n_established')
df_dissolved = df_dbd.query('type == "Dissolved"').groupby(['date'])['type'].count().rename('n_dissolved')
df_est_and_dis = pd.concat([df_established, df_dissolved], axis = 1)