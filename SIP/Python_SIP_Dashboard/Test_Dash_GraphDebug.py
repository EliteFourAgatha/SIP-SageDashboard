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

import plotly.express as px

import datetime
import mplfinance

from Card_Layout import *
from Dashboard_Layout import *
from Stock_Functions import *
from Keys1 import *

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = alpha_vantage_api_key
api_url = "https://www.alphavantage.co/query?function="

ti = TechIndicators(key=api_key, output_format='pandas')

#CONSIDER REMOVING TIME VALUE ALTOGETHER. JUST PULL DATA AND GRAPH IT.

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
                            html.H3(id='stock-ticker')
                       ]), 
                    width=4),
                dbc.Col(
                   [
                        dcc.Graph(id='stock-graph', animate=True),
                   ],
                    width=8)
            ]
       ),
    ]
)           

@app.callback(Output('stock-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')], #Input button fires callback
                [State('ticker-input-searchbar', 'value')]) #Take input searchbar state

def return_dashboard(n_clicks, ticker):
    
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    #Basic stock info (top left of layout)
    stock_name = overview_json.get('Name')
    stock_ticker = ticker

    #Do alpha vantage api call here for most recent month (year1month1 slice)
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    
    df = data
    df.reset_index(inplace=True)
    df.set_index("date", inplace=True)
    
    close = df['4. close']

    stockPrice_fig = dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': close, 'type': 'line', 'name': ticker},
            ],
            'layout':{
                'title': ticker
            }
        }
    )

    stockPrice_fig.update_yaxes(tickprefix='$', tickformat=',.2f', nticks=5)
    stockPrice_fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='black', ticklen=10)

    return stockPrice_fig

          
if __name__ == '__main__':
    app.run_server(debug=True)

