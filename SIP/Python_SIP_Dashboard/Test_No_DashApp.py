import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas import json_normalize
from pprint import pprint
import requests
import json
import alpha_vantage
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo

alpha_api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

finprep_api_key = "1882bbe25d0a9a496ee5a1e20433c3a4"

sector = 'Technology'
industry = 'Software'
exchange = 'NYSE'
marketcapmorethan = '1000000000'
number_of_companies = 10
#{} is empty dict
symbols = {}
keys = []
values = []

screener = requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?sector={sector}&industry={industry}&exchange={exchange}&limit={number_of_companies}&apikey={finprep_api_key}').json()
#append screener[i] values to lists
for item in screener:
    keys.append(item['symbol'])
    values.append(item['beta'])

#Add all key/value pairs into dictionary
for i in range(len(keys)):
    symbols[keys[i]] = values[i]

#Do alpha vantage api call here for most recent month (year1month1 slice)
ts = TimeSeries(key=alpha_api_key, output_format='csv')
data = ts.get_intraday_extended(symbol='FSLR',interval='60min',slice='year1month1')

#csv --> dataframe
df = pd.DataFrame(list(data[0]))
#set index column name
df.index.name = 'date'

#fig = pgo.Figure()
#fig.add_trace(pgo.Scatter(x=df[0], y=df[4]))

#fig.update_yaxes(tickprefix='$', tickformat=',.2f')

print(df.head(5))
print(symbols)

