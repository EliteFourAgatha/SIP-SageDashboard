import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo
import requests
import finnhub

import plotly.express as px

import datetime
import time
from dateutil.relativedelta import relativedelta

from BasicInfo_Layout import *
from Dashboard_Layout import *
from Stock_Functions import *
from Keys1 import *

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = alpha_vantage_api_key
api_url = "https://www.alphavantage.co/query?function="

ti = TechIndicators(key=api_key, output_format='pandas')

app.layout = html.Div(
    [
       dbc.Row(dbc.Col(html.H2('Stock Dashboard', style={'text-align':'center'}))),
       dbc.Row(dbc.Col(html.Div(return_input_bar(), style={'margin':'auto'}))),
       dbc.Row(
           [
               dbc.Col(
                   html.Div(
                       [
                            html.H3(id='stock-name'),
                            html.H3(id='stock-ticker'),
                            dcc.Graph(id='volume-graph', animate=True)
                       ]), 
                    width=6),
                dbc.Col(
                   [
                        dcc.Graph(id='stock-graph', animate=True),
                   ],
                    width=6)
            ]
       ),
       dbc.Row(
           dbc.Col(
               dcc.Graph(id='bar-graph', animate=True)
           )
       )
    ]
)           

@app.callback(Output('stock-graph', 'figure'), # Price chart figure
                Output('volume-graph', 'figure'),
                Output('bar-graph', 'figure'),
                [Input('ticker-input-button', 'n_clicks')], #Input button fires callback
                [State('ticker-input-searchbar', 'value')],
                prevent_initial_call = True) #Take input searchbar state

def return_dashboard(n_clicks, ticker):
    
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    #Basic stock info (top left of layout)
    stock_name = overview_json.get('Name')
    stock_ticker = ticker

    finnhub_client = finnhub.Client(api_key=finnhub_api_key)

    #data = finnhub_client.stock_candles(ticker, 'D', month_ago_unix, now_unix)
    data = finnhub_client.stock_candles(ticker, 'D', 1640050185, 1642728585)


    df = pd.DataFrame.from_dict(data)
    #Convert time column from UNIX to datetime
    df['t'] = pd.to_datetime(df['t'], unit='s')

    stock_fig = px.line(df, x='t', y='c', template="plotly_dark",
                        labels={ #Manual axis labels
                            't': 'Date',
                            'c': 'Close'
                        })
    
    stock_fig.update_yaxes(
        tickprefix = '$',
        tickformat = ',.2f'
    )
    stock_fig.update_xaxes(
        title = ''
    )

    volume_fig = return_volume_graph(df)

    bar_fig = return_bar_graph()

    #ts = TimeSeries(key=api_key, output_format='pandas')
    #data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    
    #df = data
    #df.reset_index(inplace=True)
    #df.set_index("date", inplace=True)
    
    #close = df['4. close']

    #df = df.sort_values(by="t")

    #stock_test = pgo.Figure(data=[pgo.Scatter(x = close_list, y = time_list)])

    #pxline_text = px.line(df, x = "t", y = "c")

    #stockPrice_fig = pgo.Figure(data=[dcc.Graph(
        #figure={
            #'data': [
               # {'x': df['t'], 'y': df['c'], 'type': 'line', 'name': ticker},
           # ],
       #     'layout':{
       #         'title': ticker
     #       }
    #    }
#    )

    return stock_fig, volume_fig, bar_fig

          
if __name__ == '__main__':
    app.run_server(debug=True)

