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

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

#Do alpha vantage api call here for most recent month (year1month1 slice)
ts = TimeSeries(key=api_key, output_format='csv')
data = ts.get_intraday_extended(symbol='FSLR',interval='60min',slice='year1month1')

#csv --> dataframe
df = pd.DataFrame(list(data[0]))
#set index column name
df.index.name = 'date'

#fig = pgo.Figure()
#fig.add_trace(pgo.Scatter(x=df[0], y=df[4]))

#fig.update_yaxes(tickprefix='$', tickformat=',.2f', nticks=8)
#fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='black', ticklen=10)

print(df.head(25))

