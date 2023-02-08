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
    # Central government budget disbursement
    df_disb = (pd
               .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_budget_disbursement.csv', 
                         index_col = 0, 
                         parse_dates = True)
               .drop(columns = 'carry-over', axis = 1)
               .rename(columns = {'current_current': 'Current Expenditure', 
                                  'current_capital': 'Capital Expenditure'
                                  }
                       )
               .pct_change(12)
               ) * 100
    # Agriculture
    df_agri = (pd
               .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_agri_key_indicators.csv', 
                         index_col = 0, 
                         parse_dates = True)
               .rename(columns = {'agri_prod_index': 'Agricultural Production', 
                                  'agri_price_index': 'Agricultural Price'
                                  }
                       )
               )
    df_agri['Agricultural Income'] = df_agri['Agricultural Production'] * df_agri['Agricultural Price']
    df_agri = df_agri.pct_change(12) * 100
    
    # Manufacturing
    df_manu = (pd
               .read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_manu_key_indicators.csv', 
                         index_col = 0, 
                         parse_dates = True)
               .drop(columns = ['capu_sa', 'mpi_sa'], axis = 1)
               .rename(columns = {'mpi': 'Manufacturing Production', 
                                  'capu': 'Capacity Utilization'
                                  }
                       )
               )
    df_manu['Manufacturing Production'] = df_manu['Manufacturing Production'].pct_change(12) * 100
    df_manu = df_manu[['Manufacturing Production', 'Capacity Utilization']]
    
    
    
    # Merge
    df = pd.concat([df_disb, df_agri, df_manu], axis = 1)
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
gmap = gmap_column_q(gmap, 'Agricultural Production')
gmap = gmap_column_q(gmap, 'Agricultural Price')
gmap = gmap_column_q(gmap, 'Agricultural Income')
gmap = gmap_column_q(gmap, 'Manufacturing Production')
gmap = gmap_column_q(gmap, 'Capacity Utilization', q = .001)




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
n_months = col1.number_input('Number of months', min_value=1, value=6)

st.dataframe(data = df.tail(n_months)
             .applymap('{:.1f}'.format)
             .T
             .style
             .background_gradient(axis=None, gmap=gmap.tail(n_months).T, cmap=cmap)
             )

if __name__ == '__main__':
    pass