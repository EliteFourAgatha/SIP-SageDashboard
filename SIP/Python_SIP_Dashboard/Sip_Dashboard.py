import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas import json_normalize
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
app.layout = html.Div(children=[
                        html.Div(className='main header',
                        children=[
                            html.H2('Stock Dashboard', style={'color':'white'}),
                            html.P('Descriptive Subtitle', style={'color':'white'})
                        ],
                        style={'width':'100%','margin':'auto'}),
                        html.Div(return_input_bar(),
                                    style={'width':'100%', 'margin':'auto'}
                        ),
                        dbc.Row([
                            dbc.Col(html.H3(id='stock-name')),
                            dbc.Col(html.H3(id='stock-price'))
                        ]),
                        dbc.Row([
                            dbc.Col(html.H3(id='stock-ticker')),
                            dbc.Col(html.H3(id='stock-PE-ratio'))
                        ]),
                        # Start of div for 2 column layout
                        html.Div(className='row',
                        children=[
                            dbc.Col(html.Div("Column 1")),
                            html.Div(className='data visualization column',
                            children=[
                                html.H2('Data Visualization'),
                                return_table_graph_layout(),
                                #dcc.Graph(id='main-graph',
                                        #config={'displayModeBar': False},
                                        #animate=True)
                                ])
                            ])
                        ])

#Callback for stock price and graph
@app.callback(Output('stock-name', 'children'), # Stock Name
                Output('stock-ticker', 'children'), # Stock Ticker
                Output('stock-price', 'children'), # Current Stock Price
                Output('stock-PE-ratio', 'children'),
                #Output('basic-info-table', 'children'), # Basic info like industry etc.
                #Output('basic-info-table', 'columns'),
                # Output('error-message', 'children'), # (Fill in which here____) Error Message
                Output('main-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')],
                [Input('time-interval-radio', 'value')],
                [State('ticker-input-searchbar', 'value')])

#Callback function. Takes inputs (in order), must return all outputs.
# Function is called whenever ANY included inputs are changed
#  State allows you to pass along extra values without firing the callback function
#   So this function is only called when the input (button) is pressed
def return_stock_graph(n_clicks, timeChoice, ticker):
    
    #try:
    #Company Overview call to populate table and headers
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    stock_name = overview_json.get('Name')
    stock_pe_ratio = overview_json.get('PERatio')
    stock_ticker = ticker
    #Return basic info table here

    #Intraday call to populate graph
    #intraday_response = requests.get(api_url + "TIME_SERIES_INTRADAY&interval=15min&symbol=" + ticker + "&apikey=" + api_key)
    #price_data = intraday_response.json()#Maybe redundant, might be able return data in json form already
    if timeChoice == '1mo':
        #Do alpha vantage api call here for most recent month (year1month1 slice)
        ts = TimeSeries(key=api_key, output_format='csv')
        data = ts.get_intraday_extended(symbol=ticker,interval='15min',slice='year1month1')
        
        #csv --> dataframe
        df = pd.DataFrame(list(data[0]))
        #set index column name
        df.index.name = 'date'
        stock_name = 'success_name1'
        
        #
        #Use matplotlib/plotly/better than plotly express for this

        fig = px.line(data_frame=df, x=0, y=4)
        #fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.2f')
    else:
        stock_name = 'error1'
        fig = pgo.Figure(data=[])

    #stock_price = price_data.get(['Time Series (15min)'][0][('4. Close')])
    stock_price = 'current_stock_price'

    #Return these values to output, in order
    return stock_name, stock_ticker, stock_price, stock_pe_ratio, fig
                    
    #Global lightweight call for current price and % change
    #
    #stock_global = requests.get(api_url + "GLOBAL_QUOTE&symbol=" + ticker + "&apikey=" + api_key)
    #global_json = stock_global.json() #Maybe redundant, might be able return data in json form already
    #stock_price = global_json.get('05. price')
    #percent_change = global_json.get('10. change percent')


    
#Callback to return candlestick chart if change graph button pressed
# Make sure to set graphtype variable to candlestick
# @app.callback([Output('main-graph', 'figure')],
                # [Input('candlestick-button')]

#
#Callback to return different time period on graph from radio buttons
# ..Might not be necessary, might not have time. I think this is polish.

if __name__ == '__main__':
    app.run_server(debug=True)

