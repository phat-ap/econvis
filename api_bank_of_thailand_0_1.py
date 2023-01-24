# Libraries
import http.client
import json
import datetime
import math
import pandas as pd

# BOT API

def get_bot(api_key: str, type: int, series_code: str = None, 
            start_period: str = None, end_period: str = None, 
            sort_by: str = None, keyword: str = None, category: str = None):
    
    conn = http.client.HTTPSConnection("apigw1.bot.or.th")

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
        return json.loads(data.decode("utf-8"))['result']['series']
    else: 
        link = None

    conn.request("GET", link, headers = headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8")) 

def df_of_categories(api_key):
    return pd.DataFrame.from_records(get_bot(api_key, type = 3)['result']['category']).set_index('category')

def list_of_categories_and_names(api_key):
    list_of_categories = df_of_categories(api_key).index.to_list()
    list_of_category_names_en = df_of_categories(api_key)['description_th'].to_list()
    return [str1+' '+str2 for (str1, str2) in zip(list_of_categories, list_of_category_names_en)]

def df_of_series_in_a_category(api_key, category):
    try: 
        BOTCategory_instance = globals()[category]
    except KeyError: 
        globals()[category] = BOTCategory(api_key, category)
        BOTCategory_instance = globals()[category]
    return pd.DataFrame.from_records(BOTCategory_instance.dict_of_series_details).transpose().drop(['category', 'series_code'], axis = 1)


class BOTCategory():
    def __init__(self, api_key, category: str = None):
        self.category = category
        list_of_series_details = get_bot(api_key, type = 4, category = category)

        self.list_of_series_codes = [dict_of_a_series_details['series_code'] for dict_of_a_series_details in list_of_series_details]
        
        self.dict_of_series_details = {}
        for dict_of_a_series_details in list_of_series_details:
            self.dict_of_series_details[dict_of_a_series_details['series_code']] = dict_of_a_series_details

    # Method to create df

class BOTSeriesMonthly():
    # BOTCategory_instance: BOTCategory = None
    # category: str = None
    def __init__(self, api_key, series_code: str = None, category: str = None): 
        # Create BOTCategory_instance if not exist
        try: 
            BOTCategory_instance = globals()[category]
        except KeyError: 
            globals()[category] = BOTCategory(api_key, category)
            BOTCategory_instance = globals()[category]
        
        # Details from category
        self.category = BOTCategory_instance.category
        self.series_code = series_code
        dict_of_a_series_details = BOTCategory_instance.dict_of_series_details[self.series_code]
        self.series_name_th = dict_of_a_series_details['series_name_th']
        self.series_name_eng = dict_of_a_series_details['series_name_eng']
        self.start_period = datetime.datetime.strptime(
            dict_of_a_series_details['observation_start'], 
            "%Y-%m"
            ).date()
        self.end_period = datetime.datetime.strptime(
            dict_of_a_series_details['observation_end'], 
            "%Y-%m"
            ).date()
        self.last_update_date = datetime.datetime.strptime(
            dict_of_a_series_details['last_update_date'], 
            "%Y-%m-%d"
            ).date()
        
        # Details from series
        dict_of_more_series_details = get_bot(api_key, 
                                              type = 1, 
                                              series_code = self.series_code, 
                                              start_period = self.start_period.strftime("%Y-%m-%d"),
                                              end_period = self.end_period.strftime("%Y-%m-%d"),
                                              sort_by = 'asc')['result']['series'][0]
        self.series_type = dict_of_more_series_details['series_type']
        self.frequency = dict_of_more_series_details['frequency']
        self.list_of_obs = dict_of_more_series_details['observations']
        # Preparation for obs download
        self.n_months = (self.end_period.year - self.start_period.year) * 12 + self.end_period.month - self.start_period.month
        self.n_years = math.ceil(self.n_months / 12)
        ## Download data as a list of dict
        ## Probably only work for monthly data, where the start date is 1
        list_of_obs = []
        for i in range(self.n_years):
            start_period = self.start_period.replace(year = self.start_period.year + i)
            end_period = start_period.replace(year = start_period.year + 1)
            list_of_obs += get_bot(type = 1, 
                                   series_code = self.series_code, 
                                   start_period = start_period.strftime("%Y-%m-%d"),
                                   end_period = end_period.strftime("%Y-%m-%d"),
                                   sort_by = 'asc')['result']['series'][0]['observations']
        
        ## Store data as pd.Series
        df = pd.DataFrame.from_records(list_of_obs)
        df = df.rename({'period_start': 'date', 'value': self.series_code}, 
                       axis=1
                       )
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        self.obs = df[self.series_code].astype(float)
        
if __name__ == '__main__':
    api_key = "a1c8bc6c-a1e9-46fe-9ca7-6a7ddb688af3"