# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:10:34 2023

@author: phata
"""

import pandas as pd

# Calculate Gini from list of values
def gini(li):
    y = pd.Series(li, copy = True).sort_values()
    n = len(y)
    gini = sum((y.index + 1) * y * 2) / n / sum(y) - (n + 1) / n
    return gini