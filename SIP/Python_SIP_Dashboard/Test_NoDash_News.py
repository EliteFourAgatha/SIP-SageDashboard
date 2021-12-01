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

#for iterating through newsApi cards
import itertools

from newsapi import NewsApiClient

import plotly.express as px

import datetime
import mplfinance

from Dashboard_Layout import *
from Stock_Functions import *

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

article_title = dict_test['articles'][0]['title']

#Iterate through first 3 articles in news_dict
#for artIndex in news_dict['articles'][:3]:
#    card = return_news_card_test(news_dict['articles'][artIndex]['title'], 
#        news_dict['articles'][artIndex]['description'],
#        news_dict['articles'][artIndex]['url'],
#        news_dict['articles'][artIndex]['urlToImage'])
#    card_list.append(card)

#news_card_one = card_list[0]
#news_card_two = card_list[1]
#news_card_three = card_list[2]

print(dict_test)
print(article_title)

