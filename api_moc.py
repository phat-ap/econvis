# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:58:37 2023

@author: phata
"""

import pandas as pd
import requests

dict_cpi_series_code = {"CPI": "0000000000000000",
        "CPI Food & Non Alcoholic Beverages": "1000000000000000",
        "CPI Clothing & Footwears": "2000000000000000",
        "CPI Housing & Furnishing": "3000000000000000",
        "CPI Medical & Personal Care": "4000000000000000",
        "CPI Transport & Communication": "5000000000000000",
        "CPI Recreation, Reading, Education and Religion": "6000000000000000",
        "CPI Tobacco & Alcoholic Beverages": "7000000000000000",
        "CPI Non Food & Beverages": "8000000000000000",
        "Non Core CPI Raw Food and Energy": "9000000000000000",
        "Non Core CPI Raw Food": "9100000000000000",
        "Non Core CPI Energy": "9200000000000000",
        "Core CPI": "9300000000000000"}

dict_cpi_weights = {"CPI": 1.0000,
        "CPI Food & Non Alcoholic Beverages": 0.4035,
        "CPI Clothing & Footwears": 0.0223,
        "CPI Housing & Furnishing": 0.2317,
        "CPI Medical & Personal Care": 0.0568,
        "CPI Transport & Communication": 0.2267,
        "CPI Recreation, Reading, Education and Religion": 0.0451,
        "CPI Tobacco & Alcoholic Beverages": 0.0139,
        "CPI Non Food & Beverages": 0.5965,
        "Non Core CPI Raw Food and Energy": 0.3294,
        "Non Core CPI Raw Food": 0.2055,
        "Non Core CPI Energy": 0.1239,
        "Core CPI": 0.6706}

def get_cpi_series(series_name = "CPI", series_id = "0000000000000000", from_year = 2001, to_year = 2100):
    data = requests.get("https://dataapi.moc.go.th/cpig-indexes?region_id=5&index_id=" + 
                        series_id +
                        "&from_year=" + str(from_year) +
                        "&to_year=" + str(to_year)
                        )
    df = pd.DataFrame(data.json())
    df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str)
    df.index = pd.to_datetime(df['date'])
    return df['price_index'].rename(series_name)

def get_cpi_df(dict_cpi_series_code = dict_cpi_series_code, from_year = 2001, to_year = 2100):
    li = []
    for series_name, series_id in dict_cpi_series_code.items():
        li.append(get_cpi_series(series_name, series_id, from_year = from_year, to_year = to_year))
    df=pd.concat(li,axis=1)
    return df

data = get_cpi_df()

df_yoy_12m = (data/data.shift(12)*100-100).tail(12)

df_ctg_12m = df_yoy_12m.copy()
for key in dict_cpi_weights.keys(): 
    df_ctg_12m[key] = df_ctg_12m[key] * dict_cpi_weights[key]