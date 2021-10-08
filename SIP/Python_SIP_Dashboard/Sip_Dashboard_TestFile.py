from dash_html_components.Center import Center
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas import json_normalize
import requests
import json
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo
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
               dbc.Col(dcc.Graph(id='stock-graph'), width=8)
           ]
       )
    ])

#Callback for stock price and graph
@app.callback(Output('stock-name', 'children'), # Stock Name
                Output('stock-ticker', 'children'), # Stock Ticker
                #Output('stock-price', 'children'), # Current Stock Price
                #Output('stock-PE-ratio', 'children'),
                Output('basic-info-table', 'children'), # Basic info like industry etc.
                # Output('error-message', 'children'), # (Fill in which here____) Error Message
                Output('stock-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')],
                [State('ticker-input-searchbar', 'value')])

#Callback function. Takes inputs (in order), must return all outputs.
# Function is called whenever ANY included inputs are changed
#  State allows you to pass along extra values without firing the callback function
#   So this function is only called when the input (button) is pressed
def return_stock_graph(n_clicks, ticker):
    
    #try:
    #Intraday call to populate graph
    intraday_response = requests.get(api_url+"TIME_SERIES_INTRADAY&interval=15min&symbol="+ticker+"&apikey="+api_key)
    price_data = intraday_response.json()#Maybe redundant, might be able return data in json form already
    
    #Company Overview call to populate table and headers
    overview_response = requests.get(api_url+"OVERVIEW&symbol="+ticker+"&apikey="+api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    stock_name = overview_json.get('Name')
    stock_pe_ratio = overview_json.get('PERatio')
    stock_ticker = ticker
    #stock_price = price_data.get(['Time Series (15min)'][0][('4. Close')])
    stock_price = 'current_stock_price'

    fig = pgo.Figure(data=[
                        pgo.Line(x=df['time'],
                        y=df['close'])])
    #except:
        #fig = pgo.Figure(data=[pgo.Scatter(x=[], y=[])])

    #Return these values to output, in order
    return stock_name, stock_ticker
                    
if __name__ == '__main__':
    app.run_server(debug=True)

