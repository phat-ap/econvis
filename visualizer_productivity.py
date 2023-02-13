# -*- coding: utf-8 -*-

import pandas as pd
pd.options.display.max_columns = None

df_gpp = (pd
           .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_gpp.csv'
                     )
           .drop_duplicates()
           )

for col in ['level', 'province_nesdc_en', 'type', 'sector']:
    df_gpp[col] = df_gpp[col].astype('category')

    
df_gpp = pd.melt(df_gpp, id_vars=['level', 'province_nesdc_en', 'type', 'sector'], value_vars=df_gpp.columns[4:], var_name = 'year')

df_gpp = (df_gpp
          .pivot(index = ['level', 'province_nesdc_en', 'type', 'year'], 
                 columns='sector', 
                 values='value'
                 )
          .reset_index()
          .rename_axis(None, axis=1)
          )

df_gpp['year'] = df_gpp['year'].astype('int64')


li_gpp_sectors = [
    'Accommodation and food service activities',
    'Administrative and support service activities', 
    'Agriculture',
    'Agriculture, forestry and fishing',
    'Arts, entertainment and recreation',
    'Construction',
    'Education',
    'Electricity, gas, steam and air conditioning supply',
    'Financial and insurance activities', 
    'GDP Per capita (Baht)',
    'GPP Per capita (Baht)', 
    'GRP Per capita (Baht)',
    'Gross domestic product (CVMs)', 
    'Gross domestic product (GDP)',
    'Gross provincial cluster product',
    'Gross provincial cluster product (CVMs)',
    'Gross provincial cluster product per capita (Baht)',
    'Gross provincial product (CVMs)', 
    'Gross provincial product (GPP)',
    'Gross regional product (CVMs)', 
    'Gross regional product (GRP)',
    'Human health and social work activities', 
    'Industrial',
    'Information and communication', 
    'Manufacturing',
    'Mining and quarrying', 
    'Non-Agriculture', 
    'Other service activities',
    'Population (1,000 persons)',
    'Professional, scientific and technical activities',
    'Public administration and defence; compulsory social security',
    'Real estate activities', 
    'Services', 
    'Transportation and storage',
    'Water supply; sewerage, waste management and remediation activities',
    'Wholesale and retail trade and repair of motor vehicles and motorcycle'
    ]

df_gpp.query('province_nesdc_en == "WESTERN" & type == "Chain Volume Measures"').set_index('year')['Accommodation and food service activities']

import numpy as np

df_lfs = (pd
           .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/lfs_ratchaburi_q4.csv'
                     )
           .replace('-', 0)
           .replace(np.nan, 0)
           .set_index('year')
           )

for col in ['level', 'province_en']:
    df_lfs[col] = df_lfs[col].astype('category')
    
li_lfs_sectors = [
    'Total Labor Force',
    'Agriculture, forestry and fishing',
    'Mining and quarrying',
    'Manufacturing',
    'Electricity, gas, steam and air conditioning supply',
    'Water supply; sewerage, waste management and remediation activities',
    'Construction',
    'Wholesale and retail trade and repair of motor vehicles and motorcycle',
    'Transportation and storage',
    'Accommodation and food service activities',
    'Information and communication',
    'Financial and insurance activities',
    'Real estate activities',
    'Professional, scientific and technical activities',
    'Administrative and support service activities',
    'Public administration and defence; compulsory social security',
    'Education',
    'Human health and social work activities',
    'Arts, entertainment and recreation',
    'Other service activities',
    'Activities of households as employers',
    'Activities of extraterritorial organizations and bodies',
    'Unknown'
    ]

def productivity():
    return (pd
            .concat([
                df_gpp
                .query('province_nesdc_en == "WESTERN" & type == "Chain Volume Measures"')
                .set_index('year')['Accommodation and food service activities'], 
                
                df_lfs
                .query('province_en == "Ratchaburi"')['Accommodation and food service activities']
                ], 
                axis = 1
                )
            )
