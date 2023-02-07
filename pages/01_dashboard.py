# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 20:56:41 2023

@author: phata
"""

import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Dashboard"
)

# Data
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

df = (df
      .style.background_gradient(axis=None)
      )

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

st.dataframe(df.drop_na())

if __name__ == '__main__':
    pass