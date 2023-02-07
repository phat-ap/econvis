# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:22:55 2023

@author: phata
"""
# Import libraries
import pandas as pd
import numpy as np

df = pd.read_csv('C:\\Users\\phata\\Desktop\\Data\\DBD\\for python.csv')

def gini(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))

def lorenz_curve(col):
    q = np.array([round(i,4) for i in np.linspace(0.001, 99.999, 99999)])
    data = df[col].dropna()
    nrow = data.shape[0]
    cumsum_to_total = data.cumsum()/data.sum()
    perc = np.percentile(cumsum_to_total, q)
    # gini = sum(q/100-perc)/99999
    return pd.DataFrame({col: perc}), gini(data)

df = pd.concat([lorenz_curve(col)[0] for col in df.columns], axis=1)
df.to_csv('gini_results.csv')
print([lorenz_curve(col)[1] for col in df.columns])

import plotly.graph_objects as go
fig = go.Figure(
    layout=go.Layout(
        template='plotly_white', 
        width=600, 
        height=400
        ))
# Create and style traces
q = np.array([round(i,4) for i in np.linspace(0.001, 99.999, 99999)])/100
fig.add_trace(go.Scatter(x=q, y=df['EST_ALL_WK'], name='Whole Kingdom',
                         line=dict(color='black', width=4)))
fig.add_trace(go.Scatter(x=q, y=df['EST_ALL_SOUTH'], name='Southern Region',
                          line=dict(color='gray', width=4)))
fig.add_trace(go.Scatter(x=q, y=df['EST_ALL_SONG'], name='Songkhla',
                          line=dict(color='firebrick', width=4)))
fig.show()

fig = go.Figure(
    layout=go.Layout(
        template='plotly_white', 
        width=600, 
        height=400
        ))
# Create and style traces
q = np.array([round(i,4) for i in np.linspace(0.001, 99.999, 99999)])/100
fig.add_trace(go.Scatter(x=q, y=df['DIS_ALL_WK'], name='Whole Kingdom',
                         line=dict(color='black', width=4)))
fig.add_trace(go.Scatter(x=q, y=df['DIS_ALL_SOUTH'], name='Southern Region',
                          line=dict(color='gray', width=4)))
fig.add_trace(go.Scatter(x=q, y=df['DIS_ALL_SONG'], name='Songkhla',
                          line=dict(color='firebrick', width=4)))
fig.show()