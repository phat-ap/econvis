# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 20:06:33 2023

@author: phata
"""
import streamlit as st
import os
import pandas as pd

import plotly.graph_objects as go
import plotly.io as io
io.renderers.default='browser'

## Data Cleaning

# Only provincial for mock

os.chdir('C:\\Users\\phata\\Documents\\GitHub\\econvis')

df_data = (pd
           .read_excel(os.getcwd() + '\\Data\\NESDC\\GPP.xlsx')
           .dropna()
           .drop_duplicates()
           )

df_rename = (pd
             .read_excel(os.getcwd() + '\\Data\\NESDC\\Renames.xlsx')
             )

# Unpivot years
df_data = pd.melt(df_data,
                  df_data.columns[:5],
                  var_name='year',
                  value_name='value')

# Clean
df_data = (df_data
           .query('type == "Current Market Prices"')
           .drop(['region', 'province_code_nesdc', 'type'], axis = 1)
           .dropna()
           .merge(df_rename, left_on = 'province', right_on = 'province_en_NESDC')
           .drop(['province', 'province_en_NESDC'], axis = 1)
           .copy()
           )

# Data type
df_data.year = df_data.year.astype(int)
df_data.province_en = df_data.province_en.astype('category')
df_data.sector = df_data.sector.astype('category')

# Pivot
df_pv = df_data.pivot(index=['province_en','year'], columns='sector', values='value')

## for st
list_of_provinces = df_rename.province_en.to_list()
list_of_column_names = df_pv.columns.to_list()
list_of_years = df_data.year.unique()

# st
sb_province = st.selectbox('Province', list_of_provinces)
sb_from = st.selectbox('From', list_of_years)
sb_to = st.selectbox('To', list_of_years)

## color map
dict_color = {
    'Agriculture': 'green',
    'Industrial': 'yellow',
    'Services': 'blue'
    }

## goBar functions
def goBar_structure(y, name = None):
    if name is None: 
        name = y
    else:
        pass
    return (go.Bar(name = name, 
                   x = df.index, 
                   y = df[y]/df['Gross provincial product (GPP)'], 
                   hovertemplate = 'Year %{x}: %{y:.1%}', 
                   marker = {'color': dict_color[y]}
                   )
            )

# Query for plot
df = (df_pv
      .query('province_en == @sb_province & year >= @sb_from & year <= @sb_to')
      .droplevel(level=0)
      )

fig = go.Figure(
    data=[
        goBar_structure('Agriculture'),
        goBar_structure('Industrial'),
        goBar_structure('Services')],
    layout = go.Layout(yaxis=dict(tickformat=".0%"))
    )
# Change the bar mode
fig.update_layout(barmode='stack', bargap=0, yaxis_range=[0,1])

st.write(fig)

