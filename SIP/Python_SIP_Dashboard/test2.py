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
import plotly.express as px
import datetime
import mplfinance

from Dashboard_Layout import *
from Stock_Functions import *

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

# App layout
app.layout = html.Div(
    [
       dbc.Row(dbc.Col(html.H1('Stock Dashboard', style={'text-align':'center'}))),
       dbc.Row(dbc.Col(html.Div(return_input_bar(), style={'margin':'auto'}))),
       dbc.Row(
           [
               dbc.Col(html.H3(id='stock-name')),
               dbc.Col(html.H3(id='stock-ticker'))
           ]
       ),
       dbc.Row(
           [
               dbc.Col(html.Table(id='stock-profile-table'), width=3),
               dbc.Col(
                   [
                        return_timeinterval(),
                        dcc.Graph(id='stock-graph'),
                   ],
                   width=8)
           ]
       )
    ])

#Callback for stock price and graph
@app.callback(Output('stock-name', 'children'), # Stock Name
                Output('stock-ticker', 'children'), # Stock Ticker
                #Output('stock-profile-table', 'children'), # Basic info like industry etc.
                Output('stock-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')],
                [State('ticker-input-searchbar', 'value')],
                [State('time-interval-radio', 'value')])

def return_something(n_clicks, ticker, radio_value):
    if radio_value == '1mo':
        #Do alpha vantage api call here for most recent month (year1month1 slice)
        ts = TimeSeries(key=api_key, output_format='csv')
        data = ts.get_intraday_extended(symbol=ticker,interval='15min',slice='year1month1')
        
        #csv --> dataframe
        df = pd.DataFrame(list(data[0]))
        #set index column name
        df.index.name = 'date'
        stock_name = 'success_name1'

        fig = px.line(data_frame=df, x=0, y=4)
        #fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.2f')
    else:
        stock_name = 'error1'
        fig = pgo.Figure(data=[])
    return stock_name, ticker, fig


#Function to supply ticker to api call
# If you just hard-code a ticker, df is a dataframe object.
#  If you try to pass a ticker, df becomes a "textfilereader" object and can't
#    be used as a dataframe then which defeats the purpose of pd.read_csv.
#      Need new method
#def return_dataframe(ticker):
#    df = pd.read_csv(api_url + 'TIME_SERIES_INTRADAY_EXTENDED&symbol='+ticker+'&interval=60min&slice=year1month2&apikey='+api_key+'&datatype=csv&outputsize=full')

if __name__ == '__main__':
    app.run_server(debug=True)