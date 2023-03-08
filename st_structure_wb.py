import econvis as ev
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Economic Structure by Country"
)

'''
# Economic Structure by Country 
'''

col1, col2, col3 = st.columns(3)

str_country = col1.selectbox('Country', ev.ser_countries.sort_values())
df_structure_wb = ev.get_df_structure_wb(str_country)
min_year = df_structure_wb.index.astype('str').astype('int64').min()
max_year = df_structure_wb.index.astype('str').astype('int64').max()

start_year = col2.number_input('Start Year', min_value=min_year, max_value=max_year, value=min_year)
end_year = col3.number_input('End Year', min_value=start_year, max_value=max_year, value=max_year)

df_structure_wb = df_structure_wb[str(start_year):str(end_year)]

# Economic Structure Stacked Bar

fig = go.Figure(data=[
    go.Bar(name='Services',
           x=df_structure_wb.index.astype('str'), 
           y=df_structure_wb['Services'],
           hovertemplate="%{y:.1f}%",
           marker_color='#264b96'
           ),
    go.Bar(name='Industry (incl. construction)', 
           x=df_structure_wb.index.astype('str'), 
           y=df_structure_wb['Industry (incl. construction)'],
           hovertemplate="%{y:.1f}%",
           marker_color='#bf212f'
           ),
    go.Bar(name='Agriculture', 
           x=df_structure_wb.index.astype('str'), 
           y=df_structure_wb['Agriculture'],
           hovertemplate="%{y:.1f}%",
           marker_color='#27b376'
           ),
])

fig.update_layout(
    barmode='stack', 
    xaxis_tickangle=90,
    yaxis_title="% of Total Value Added", 
    font_family="Arial", 
    bargap=0,
    yaxis_range=[0,100],
    hovermode="x unified",
    title={'text': f"<b>{str_country}'s Economic Structure</b>",
            'x': 0.5,
            'xanchor': 'center'},
    )

fig.add_annotation(text="Source: World Bank's World Development Indicators",
                  xref="paper", yref="paper",
                  xanchor='left', x=-.1, y=-.25, showarrow=False)

st.plotly_chart(fig, use_container_width=True)

# Economic Structure Pie Chart: start_year

import plotly.graph_objects as go

fig = go.Figure(data=[
    go.Pie(labels=df_structure_wb.columns, 
           values=df_structure_wb.head(1).iloc[0],
           sort=False, 
           direction='clockwise', 
           marker=dict(colors=['#27b376', '#bf212f', '#264b96']),
           )
    ])

fig.update_layout(
    barmode='stack', 
    xaxis_tickangle=90,
    font_family="Arial",
    title={'text': f"<b>{str_country}'s Economic Structure in {start_year}</b>",
            'x': 0.5,
            'xanchor': 'center'},
    legend=dict(orientation="h",xanchor='center',y=0,x=0.5) 
    )

fig.update_traces(hoverinfo="label+percent")

fig.add_annotation(text="Source: World Bank's World Development Indicators",
                  xref="paper", yref="paper",
                  xanchor='left', x=0, y=-.3, showarrow=False)

col1, col2 = st.columns(2)
col1.plotly_chart(fig, use_container_width=True)

# Economic Structure Pie Chart: end_year

fig = go.Figure(data=[
    go.Pie(labels=df_structure_wb.columns, 
           values=df_structure_wb.tail(1).iloc[0],
           sort=False, 
           direction='clockwise', 
           marker=dict(colors=['#27b376', '#bf212f', '#264b96']),
           )
    ])

fig.update_layout(
    barmode='stack', 
    xaxis_tickangle=90,
    font_family="Arial",
    title={'text': f"<b>{str_country}'s Economic Structure in {end_year}</b>",
            'x': 0.5,
            'xanchor': 'center'},
    legend=dict(orientation="h",xanchor='center',y=0,x=0.5) 
    )

fig.update_traces(hoverinfo="label+percent")

fig.add_annotation(text="Source: World Bank's World Development Indicators",
                  xref="paper", yref="paper",
                  xanchor='left', x=0, y=-.3, showarrow=False)

col2.plotly_chart(fig, use_container_width=True)

# Economic Structure Changes

fig = go.Figure(go.Bar(
            y=df_structure_wb.columns,
            x=(df_structure_wb.tail(1) - df_structure_wb.head(1).values).iloc[0],
            marker=dict(color=['#27b376', '#bf212f', '#264b96']),
            orientation='h', 
            hoverinfo='none',
            text=(df_structure_wb.tail(1) - df_structure_wb.head(1).values).iloc[0],
            texttemplate='%{text:.1f} pp'))

fig.update_layout(
    xaxis_title="changes in percentage points", 
    title={'text': f"<b>Changes in {str_country}'s Economic Structure between {start_year} and {end_year}</b>",
            'x': 0.5,
            'xanchor': 'center'},    
    font_family="Arial",  yaxis={'categoryorder':'array', 'categoryarray':np.flip(df_structure_wb.columns.values)}
    )

fig.add_annotation(text="Source: World Bank's World Development Indicators",
                  xref="paper", yref="paper",
                  xanchor='left', x=-.25, y=-.25, showarrow=False)

st.plotly_chart(fig, use_container_width=True)