import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo
import requests
import json
import finnhub

import calendar
from datetime import datetime
import time

#for iterating through newsApi cards
import itertools

from newsapi import NewsApiClient

import plotly.express as px

import datetime
import mplfinance

from Card_Layout import *
from Dashboard_Layout import *
from Stock_Functions import *
from Keys1 import *

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

news_api = '8ea69eabd7074f14a977d2f1541498f4'

stock_name = 'Facebook'

#News module
news_response = requests.get('https://newsapi.org/v2/top-headlines?q='+str(stock_name)+'?sources="motley-fool, marketwatch"&apiKey=' + api_key)
pretty_news_response = json.dumps(news_response.json(), indent=4)
news_json = json.dumps(news_response.json())
news_dict = json.loads(news_json)

news_client = NewsApiClient(api_key=news_api)
dict_test = news_client.get_top_headlines(q=stock_name)

card_list = []

artOne_title = dict_test['articles'][0]['title']
artOne_desc = dict_test['articles'][0]['description']
artOne_url = dict_test['articles'][0]['url']
artOne_urlImage = dict_test['articles'][0]['urlToImage']

artTwo_title = dict_test['articles'][1]['title']
artTwo_desc = dict_test['articles'][1]['description']
artTwo_url = dict_test['articles'][1]['url']
artTwo_urlImage = dict_test['articles'][1]['urlToImage']

artThree_title = dict_test['articles'][2]['title']
artThree_desc = dict_test['articles'][2]['description']
artThree_url = dict_test['articles'][2]['url']
artThree_urlImage = dict_test['articles'][2]['urlToImage']

news_card_one = return_news_card_test(artOne_title, artOne_desc, artOne_url, artOne_urlImage)
news_card_two = return_news_card_test(artTwo_title, artTwo_desc, artTwo_url, artTwo_urlImage)
news_card_three = return_news_card_test(artThree_title, artThree_desc, artThree_url, artThree_urlImage)

print(dict_test)

# datetime object containing current date and time
now = datetime.now()
nowUnixValue = time.mktime(now.timetuple()) * 1000


# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M")
print("date and time =", dt_string)

finnhub_client = finnhub.Client(api_key=finnhub_api_key)

data = finnhub_client.stock_candles('msft', 'D', 1590988249, 1591852249)

df = pd.DataFrame(data, index=['c'])
#new_df = pd.to_datetime(df['t'], unit='s', origin='unix')

#stock_test = pgo.Figure(data=[pgo.Scatter(x = df['c'], y = df['t'])])

#pxline_text = px.line(df, x = "t", y = "c")
#pxline_text.show()

print(df)
#print(new_df)

#print(dict_test)
#print(article_title)

