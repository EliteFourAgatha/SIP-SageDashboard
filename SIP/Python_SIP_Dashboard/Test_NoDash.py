import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo
import requests
import json
import finnhub
import dataprep
from dataprep.eda import plot

import calendar
import datetime
import time
from dateutil.relativedelta import relativedelta

#for iterating through newsApi cards
import itertools

from newsapi import NewsApiClient

import plotly.express as px

import datetime
import mplfinance

from BasicInfo_Layout import *
from Dashboard_Layout import *
from Keys1 import *

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

news_api = '8ea69eabd7074f14a977d2f1541498f4'

stock_name = 'Facebook'

# datetime object containing current date and time
now = datetime.now().date()

current_year = now.year

first_day_of_year = datetime(current_year, 1, 1).date()
days_since_new_year = now - first_day_of_year
print(days_since_new_year.days)

finnhub_client = finnhub.Client(api_key=finnhub_api_key)

trends = finnhub_client.recommendation_trends('MSFT')
trend_df = pd.DataFrame.from_dict(trends)

buy = [trend_df['buy'][0]]
buy = (buy[0])
sell = [trend_df['sell'][0]]
sell = (sell[0])
hold = [trend_df['hold'][0]]
hold = (hold[0])
strongBuy = [trend_df['strongBuy'][0]]
strongBuy = (strongBuy[0])
strongSell = [trend_df['strongSell'][0]]
strongSell = [strongSell[0]]

#d = {'Sentiment score': [buy, sell, hold, strongBuy, strongSell]}
#index = ['Buy', 'Sell', 'Hold', 'Strong Buy', 'Strong Sell']
df = pd.DataFrame(np.empty((0, 5)))
#df['Buy'] = buy
#df['Sell'] = sell
#df['Hold'] = hold
#df['Strong Buy'] = strongBuy
#df['Strong Sell'] = strongSell
df.columns = [['Buy', 'Sell', 'Hold', 'Strong Buy', 'Strong Sell']]
df.loc[0] = [buy, sell, hold, strongBuy, strongSell]

data_dict = {'Buy': buy, 'Sell': sell, 'Hold': hold, 'Strong Buy': strongBuy, 'Strong Sell': strongSell}
columns = list(data_dict.keys())
values = list(data_dict.values())

columns2 = ['a', 'b', 'c']
values2 = [buy, sell, hold]

data = [pgo.Bar(
    x = columns2,
    y = values2
)]
figure = pgo.Figure(data = data)
figure.show(renderer = "browser")

#fig = px.bar(x = columns, y = values)
#fig.show(renderer= "browser")

#print(trend_df['buy'][0])
#print(df)
print(columns[1])
print(columns[2])
print(values)
print(values[1])
print(values[2])
