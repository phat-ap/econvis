import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go

import api_bank_of_thailand_0_2 as ab
import api_moc as am

df_of_categories = ab.get_category_df()




add_sidebar = st.sidebar.selectbox('Select View', 
                                   ('Test', 
                                    'CPI',
                                    'Series List'
                                    )
                                   )
if add_sidebar == 'Test':
    col1, col2 = st.columns(2)
    EC_EI_020 = ab.BOTCategory('EC_EI_020')
    bot_df_EC_EI_020 = EC_EI_020.get_obs_df()
    with col1:
        st.line_chart(pd.to_numeric(bot_df_EC_EI_020['EIEXUSDM00159']))
    with col2:
        st.line_chart(pd.to_numeric(bot_df_EC_EI_020['EIIMUSDM00161']))
    st.line_chart(pd.to_numeric(bot_df_EC_EI_020['EIIMUSDM00160']))
    fig = go.Figure(data = [go.Scatter(x = bot_df_EC_EI_020.index, y = pd.to_numeric(bot_df_EC_EI_020['EIIMUSDM00160']), mode = 'lines')], layout = {'title': 'EIIMUSDM00160'})
    st.write(fig)
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
    st.write(fig)
if add_sidebar == 'Series List':
    pass