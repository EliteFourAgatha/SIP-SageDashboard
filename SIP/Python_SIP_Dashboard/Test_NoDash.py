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

from Card_Layout import *
from Dashboard_Layout import *
from Stock_Functions import *
from Keys1 import *

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

news_api = '8ea69eabd7074f14a977d2f1541498f4'

stock_name = 'Facebook'

# datetime object containing current date and time
now = datetime.now()
nowUnixValue = time.mktime(now.timetuple()) * 1000


# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M")
print("date and time =", dt_string)

# datetime object containing current date and time
now = datetime.now()
now_unix = int(now.timestamp())

#Works, having hard time finding month ago. 
# Might need to convert from datetime object
now_time = int(time.time())

#month_ago_time = now_time - 


month_ago_unix = now - relativedelta(months=1)
month_ago_unix = int(month_ago_unix.timestamp())

finnhub_client = finnhub.Client(api_key=finnhub_api_key)

data = finnhub_client.stock_candles('msft', 'D', 1590988249, 1591852249)

df = pd.DataFrame.from_dict(data)
df['t'] = pd.to_datetime(df['t'], unit='s')
#plot(df)

df2 = px.data.gapminder().query("continent == 'Oceania'")
#fig = px.bar(df, x='year', y='pop',
           #  hover_data=['lifeExp', 'gdpPercap'], color='country',
            # labels={'pop':'population of Canada'})

#print(df.info(verbose=True))
#print(df)

print(now_time)
print(now_unix)
print(month_ago_unix)
#print(month_ago_unix)

