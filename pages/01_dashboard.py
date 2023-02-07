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
df = pd.read_csv('https://raw.githubusercontent.com/phat-ap/econvis/main/data/tha_budget_disbursement.csv')

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

st.dataframe(df)

print(df)