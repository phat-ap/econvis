# Imports
import wbgapi as wb
import pandas as pd

# pd.Series of country names with ISO3 as indices
ser_countries = wb.economy.DataFrame(skipAggs=True).name

def get_df_structure_wb(str_country: str):
    df = wb.data.DataFrame(['NV.AGR.TOTL.ZS', 
                            'NV.IND.TOTL.ZS', 
                            'NV.SRV.TOTL.ZS'
                            ], 
                            economy=ser_countries[ser_countries == str_country].index[0], 
                            skipBlanks=True, 
                            columns='series'
                            ).dropna()
    df.index = (pd
                .to_datetime(df.index, format = 'YR%Y')
                .to_period('Y')
                .rename('year')
                )
    df['total'] = df.sum(axis=1)
    for col in df.columns:
        df[col] = df[col] / df['total']*100
    return (df
            .rename(columns = {'NV.AGR.TOTL.ZS': 'Agriculture', 
                            'NV.IND.TOTL.ZS': 'Industry (incl. construction)', 
                            'NV.SRV.TOTL.ZS': 'Services'
                            }
                    )
            .drop('total', 
                axis = 1
                )
            )