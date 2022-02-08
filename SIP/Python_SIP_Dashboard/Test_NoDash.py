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
now = datetime.now().date()

current_year = now.year

first_day_of_year = datetime(current_year, 1, 1).date()
ytd_calculated_date = now - first_day_of_year
print(ytd_calculated_date.days)


# dd/mm/YY
dt_string = now.strftime("%d/%m/%Y")
print("date and time =", dt_string)

finnhub_client = finnhub.Client(api_key=finnhub_api_key)

trends = finnhub_client.recommendation_trends('AAPL')
trend_df = pd.DataFrame.from_dict(trends)

#print(trend_df['buy'][0])
#print(trend_df.columns)

data_canada = px.data.gapminder().query("country == 'Canada'")
fig = px.bar(data_canada, x='year', y='pop')



print(now)

