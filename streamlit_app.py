import streamlit as st
import pandas as pd

import api_bank_of_thailand as api_bot

api_key = "a1c8bc6c-a1e9-46fe-9ca7-6a7ddb688af3"
df_of_categories = api_bot.df_of_categories(api_key)
list_of_categories_and_names = api_bot.list_of_categories_and_names(api_key)



add_sidebar = st.sidebar.selectbox('Select View', 
                                   ('Dashboard', 
                                    'Table List',
                                    'Series List'
                                    )
                                   )
if add_sidebar == 'Dashboard':
    pass
if add_sidebar == 'Table List':
    st.table(data = df_of_categories) #
if add_sidebar == 'Series List':
    st.selectbox('Table', list_of_categories_and_names)
    st.dataframe(data = api_bot.df_of_series_in_a_category(api_key, 'EC_MB_012_S3').replace("_", " ", regex=True), use_container_width  = True)