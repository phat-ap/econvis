# -*- coding: utf-8 -*-

import pandas as pd
pd.options.display.max_columns = None

# Data
df_mots = (pd
           .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_mots_annual_by_province.csv'
                     )
           .drop(['province_th', 'variable_th'],
                 axis = 1
                 )
           )

for col in ['level', 'province_en', 'variable_en']:
    df_mots[col] = df_mots[col].astype('category')

df_mots = (df_mots
           .pivot(index = ['level', 'province_en', 'year'], 
                  columns='variable_en', 
                  values='value'
                  )
           .reset_index()
           .rename_axis(None, axis=1)
           )

# Plot
from plotly.offline import plot
import plotly.graph_objects as go

fig = go.Figure(
    layout=go.Layout(
        template='plotly_white', 
        width=600, 
        height=400
        ))

x = [2019, 2020, 2021, 2022]

novwk = df_mots.query('province_en == "Whole Kingdom"').set_index('year')['Number of Visitors']
novcen = df_mots.query('province_en == "Central"').set_index('year')['Number of Visitors']
novrbr = df_mots.query('province_en == "Ratchaburi"').set_index('year')['Number of Visitors']

# Create and style traces
fig.add_trace(go.Scatter(x=x, y=novwk/novwk.iloc[0]*100, name='Whole Kingdom',
                         line=dict(color='black', width=4)))
fig.add_trace(go.Scatter(x=x, y=novcen/novcen.iloc[0]*100, name='Central',
                         line=dict(color='gray', width=4)))
fig.add_trace(go.Scatter(x=x, y=novrbr/novrbr.iloc[0]*100, name='Ratchaburi',
                          line=dict(color='firebrick', width=4)))
fig.update_layout(title='Number of Visitors',
                  hovermode=False)
plot(fig)