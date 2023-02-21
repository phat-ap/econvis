# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:15:27 2023

@author: phata
"""
import pandas as pd
import numpy as np

def gini(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))

df = pd.read_excel("C:\\Users\\phata\\Desktop\\ratchaburi_dbd_for_gini.xlsx")

for col in df.columns:
    print(col, gini(df[col].dropna()))