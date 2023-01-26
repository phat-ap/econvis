# Need to convert data to numeric

# Libraries
import http.client
import json
import datetime as dt
import math
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

# API Key
api_key = "a1c8bc6c-a1e9-46fe-9ca7-6a7ddb688af3"

headers = {
    'X-IBM-Client-Id': api_key,
    'accept': "application/json"
    }
# Connection
conn = http.client.HTTPSConnection("apigw1.bot.or.th")
# BOT API

def input_api_key(api_key):
    headers['X-IBM-Client-Id'] = api_key

def date_formatter(date_string):
    # Yearly
    if len(date_string) == 4:
        return dt.datetime.strptime(date_string, '%Y')
    elif len(date_string) == 7:
        # Quarterly
        if date_string.find('Q') != -1:
            [year_str, quarter_str] = date_string.split('-Q')
            return dt.datetime(int(year_str), int(quarter_str)*3, 1)
        # Half-year
        elif date_string.find('H') != -1:
            [year_str, quarter_str] = date_string.split('-H')
            return dt.datetime(int(year_str), int(quarter_str)*6, 1)
        # Monthly
        else:
            return dt.datetime.strptime(date_string, '%Y-%m')
    # 2 types of daily
    # YYYY-MM-DD
    elif date_string.find('-') != -1:
        return dt.datetime.strptime(date_string, '%Y-%m-%d')
    # DD/MM/YYYY
    elif date_string.find('/') != -1:
        return dt.datetime.strptime(date_string, '%d/%m/%Y')
    # np.nan
    elif date_string != np.nan:
        return np.nan
    else:
        raise Exception("Unknown date format.")

def get_category_df():
    link = "/bot/public/categorylist/category_list/"
    conn.request("GET", link, headers = headers)
    res = conn.getresponse()
    data = res.read()
    li = json.loads(data.decode("utf-8"))['result']['category']
    df = pd.DataFrame(li)
    return df

def get_series_details_li_given_category(category: str):
    link = "/bot/public/categorylist/series_list/?category=" + str(category)
    conn.request("GET", link, headers = headers)
    res = conn.getresponse()
    data = res.read()
    # List of date details
    li = json.loads(data.decode("utf-8"))['result']['series']
    return li

def get_series_details_df_given_category(category: str):
    li = get_series_details_li_given_category(category)
    df = pd.DataFrame(li) # .drop('category', axis =   1)
    return df

def get_series_details_df():
    # Very API-intensive
    li = []
    category_df = get_category_df()
    n_category = category_df.shape[0]
    for idx, x in enumerate(category_df['category']):
        series_df = get_series_details_df_given_category(x)
        li = li + [series_df]
        print(str(idx + 1) + ' of ' + str(n_category))
    df = pd.concat(li, ignore_index=True)
    for col_name in ['observation_start', 'observation_end', 'last_update_date']:
        df[col_name] = df[col_name].map(date_formatter)
    return df

class BOTCategory():
    def __init__(self, category: str = None):
        self.category = category
        list_of_series_details = get_series_details_li_given_category(category)

        self.list_of_series_codes = [dict_of_a_series_details['series_code'] for dict_of_a_series_details in list_of_series_details]
        
        self.dict_of_series_details = {}
        for dict_of_a_series_details in list_of_series_details:
            self.dict_of_series_details[dict_of_a_series_details['series_code']] = dict_of_a_series_details
        
    def get_obs_df(self):
        for idx, series_code in enumerate(self.list_of_series_codes):
            
            try: 
                BOTSeries_instance = globals()[series_code]
            except KeyError: 
                globals()[series_code] = BOTSeries(series_code, self.category)
                BOTSeries_instance = globals()[series_code]
                
            if idx == 0:
                df = BOTSeries_instance.obs_df
            else:
                df = df.join(BOTSeries_instance.obs_df, 
                             on=df.index, 
                             how='outer'
                             ).drop('key_0', axis = 1)
        return df


class BOTSeries():
    def __init__(self, series_code: str = None, category: str = None):
        self.series_code = series_code
        self.category = category
        try: 
            BOTCategory_instance = globals()[self.category]
        except KeyError: 
            globals()[self.category] = BOTCategory(self.category)
            BOTCategory_instance = globals()[self.category]
        
        # Details from the category
        
        dict_of_a_series_details = BOTCategory_instance.dict_of_series_details[self.series_code]
        for key in dict_of_a_series_details.keys():
            setattr(self, 
                    key, 
                    dict_of_a_series_details[key])        
        for key in ['observation_start', 'observation_end', 'last_update_date']:
            date_string = dict_of_a_series_details[key]
            setattr(self, 
                    key, 
                    date_formatter(date_string))
        
        # Details from the series itself
        
        dict_of_more_a_series_details \
            = get_series_dict(self.series_code, 
                              self.observation_start, 
                              self.observation_start) 
        for key in ['unit_th', 'unit_eng', 'series_type', 'frequency']:
            setattr(self, 
                    key, 
                    dict_of_more_a_series_details[key])
        
        # Observations
        
        if self.frequency == 'Daily':
            dtime = relativedelta(months=+3)
        else: # Monthly or less
            dtime = relativedelta(years=+8)
        
        download_start = self.observation_start.replace(day = 1)
        download_end = download_start + dtime
        li = []
        while download_start <= self.observation_end:
            print(download_start, download_end)
            li += get_series_dict(self.series_code, download_start, download_end)['observations']
            download_start = download_start + dtime
            download_end = download_start + dtime
        df = pd.DataFrame.from_records(li)
        df['period_start'] = df['period_start'].map(date_formatter)
        df = df.rename(columns = {'period_start': 'date', 'value': self.series_code})
        df = df.set_index('date')
        self.obs_df = df

def get_series_dict(series_code, start_period, end_period):
    link = "/bot/public/observations/?series_code=" + series_code + \
    "&start_period=" + start_period.strftime("%Y-%m-%d") + \
    "&end_period=" + end_period.strftime("%Y-%m-%d") + \
    "&sort_by=asc"
    conn.request("GET", link, headers = headers)
    res = conn.getresponse()
    data = res.read()        
    return json.loads(data.decode("utf-8"))['result']['series'][0]


def get_bot(type: int, category: str = None, series_code: str = None, 
            start_period: str = None, end_period: str = None, 
            sort_by: str = None, keyword: str = None):
    headers = {
        'X-IBM-Client-Id': api_key,
        'accept': "application/json"
        }
    if type == 1:
        link = "/bot/public/observations/?series_code=" + str(series_code) + \
        "&start_period=" + str(start_period) + \
        "&end_period=" + str(end_period) + \
        "&sort_by=" + str(sort_by)
    elif type == 2:
        link = "/bot/public/search-series/?keyword=" + str(keyword)
    elif type == 3:
        link = "/bot/public/categorylist/category_list/"
    elif type == 4:
        link = "/bot/public/categorylist/series_list/?category=" + str(category)
        conn.request("GET", link, headers = headers)
        res = conn.getresponse()
        data = res.read()
        # List of date details
        return json.loads(data.decode("utf-8")) # ['result']['series']
    else: 
        link = None

    conn.request("GET", link, headers = headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8")) 

def print_api_key():
    print(api_key)

if __name__ == '__main__':
    pass

    