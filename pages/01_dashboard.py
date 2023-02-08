# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 20:56:41 2023

@author: phata
"""

import streamlit as st
import pandas as pd
import os
from scipy.stats import zscore

from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('rg', ['r', 'w', 'g'], N = 256)

st.set_page_config(
    page_title="Dashboard"
)

# Data
@st.experimental_memo
def fetch_and_clean_data():
    df = pd.read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_budget_disbursement.csv', 
                     index_col = 0, 
                     parse_dates = True)
    
    df = (df
          .drop(columns = 'carry-over', axis = 1)
          .rename(columns = {'current_current': 'Current Expenditure', 
                             'current_capital': 'Capital Expenditure'
                             }
                  )
          .pct_change(12)
          )*100
    # Format date
    df.index = df.index.format(formatter = lambda t: t.strftime("%b %y"))
    return df

df = fetch_and_clean_data()

# gmap functions
def gmap_column_q(gmap, column, q = .20):
    x_lower = gmap[column].quantile(q)
    x_upper = gmap[column].quantile(1-q)
    gmap[column] = gmap[column].map(lambda x: x / x_upper if x > 0 else x / abs(x_lower))
    gmap[column] = gmap[column].clip(upper = 1., lower = -1.)
    return gmap

# gmap
gmap = df.copy()
gmap = gmap_column_q(gmap, 'Current Expenditure')
gmap = gmap_column_q(gmap, 'Capital Expenditure')


# sidebar
st.sidebar.header("Dashboard")
st.sidebar.write("Dashboard")

# Contents

st.write("# Thai Economic Dashboard! 📊")

st.markdown(
    """
    Some text.
"""
)
col1, col2 = st.columns([1, 3])
n_months = col1.number_input('Number of months', min_value=1, max_value=36, value=6)

st.dataframe(data = df.tail(n_months)
             .applymap('{:.1f}'.format)
             .T
             .style
             .background_gradient(axis=None, gmap=gmap.tail(n_months).T, cmap=cmap)
             )

if __name__ == '__main__':
    pass