# -*- coding: utf-8 -*-

import pandas as pd

# Data
df_mots = (pd
           .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_mots_annual_by_province.csv'
                     )
           .drop(['province_th', 'variable_th'],
                 axis = 1
                 )
           )