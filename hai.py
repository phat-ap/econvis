# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 21:24:46 2023

@author: phata
"""

import pandas as pd

# Data
df_hai = (pd
          .read_csv('C:\\Users\\phata\\Documents\\GitHub\\econvis\\data\\tha_human_achievement_index.csv'
                    )
          .drop('name_th', 
                axis = 1
                )
          .melt(id_vars = ['level', 'name_en'],
                var_name='year',
                value_name = 'hai'
                )
          )

# Function to get provincial/regional data quickly
def hai_pv(area):
    return df_hai.query('name_en == @area').set_index('year')['hai']

# List of all areas
li_regions = sorted(df_hai.query('level == "Regional"')['name_en'].unique().tolist())
li_provinces = sorted(df_hai.query('level == "Provincial"')['name_en'].unique().tolist())

from plotly.offline import plot

import plotly.graph_objects as go
fig = go.Figure(
    layout=go.Layout(
        template='plotly_white', 
        width=600, 
        height=400
        ))

# Create and style traces
fig.add_trace(go.Scatter(x=hai_pv('Whole Kingdom').index, y=hai_pv('Whole Kingdom'), name='Whole Kingdom',
                         line=dict(color='black', width=4)))
fig.add_trace(go.Scatter(x=hai_pv('Central (Except Bangkok)').index, y=hai_pv('Central (Except Bangkok)'), name='Central Region<br>(Except Bangkok)',
                          line=dict(color='gray', width=4)))
fig.add_trace(go.Scatter(x=hai_pv('Ratchaburi').index, y=hai_pv('Ratchaburi'), name='Ratchaburi',
                          line=dict(color='firebrick', width=4)))
fig.update_layout(title='Human Achievement Index<br><sup>Source: NESDC</sup>',
                  hovermode=False)
plot(fig, {'staticPlot': True})