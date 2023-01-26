import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go

import api_bank_of_thailand_0_2 as ab
import api_moc as am





add_sidebar = st.sidebar.selectbox('Select View', 
                                   ('CPI',
                                    'Series List'
                                    )
                                   )
if add_sidebar == 'CPI':
    
    fig = go.Figure(data = [go.Scatter(name='CPI',
                                       x = am.df_ctg_12m.index,
                                       y = am.df_ctg_12m['CPI'],
                                       text = am.df_ctg_12m['CPI'].round(1),
                                       textposition = 'top center',
                                       mode = "lines+markers+text"),
                            go.Bar(name = 'Core CPI', 
                                   x = am.df_ctg_12m.index, 
                                   y = am.df_ctg_12m['Core CPI']),
                            go.Bar(name = 'Energy', 
                                   x = am.df_ctg_12m.index, 
                                   y = am.df_ctg_12m['Non Core CPI Energy']),
                            go.Bar(name = 'Raw Food', 
                                   x = am.df_ctg_12m.index, 
                                   y = am.df_ctg_12m['Non Core CPI Raw Food'])
                            ]
                    )
    fig.update_layout(barmode='stack')
    st.plotly_chart(fig, use_container_width=True)
if add_sidebar == 'Series List':
    pass