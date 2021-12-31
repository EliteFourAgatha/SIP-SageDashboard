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

import plotly.express as px

import datetime
import mplfinance

from Dashboard_Layout import *
from Stock_Functions import *
from Keys1 import *

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = alpha_vantage_api_key
api_url = "https://www.alphavantage.co/query?function="
peRatio_Link = "https://www.forbes.com/advisor/investing/what-is-pe-price-earnings-ratio/"

# App layout
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
                            html.H3(id='stock-price'),
                            dbc.Card(
                                [
                                    dbc.CardHeader("Sector",
                                        style={'text-align':'center'}),
                                    dbc.CardBody(html.H2(className="card-title", id='stock-sector',
                                        style={'color': 'black', 'fontSize': '14'}))
                                ]
                            ),
                            dbc.Card(                                
                                [
                                    dbc.CardHeader("Industry",
                                        style={'text-align':'center'}),
                                    dbc.CardBody(html.H3(className="card-title", id='stock-industry',
                                        style={'color': 'black', 'fontSize': '14'}))
                                ]
                            ),
                       ]), 
                    width=4),
                dbc.Col(
                   [
                        return_timeinterval(),
                        dcc.Graph(id='stock-graph'),
                   ],
                    width=8)
            ]
       ),
       dbc.Row(
           [
                dbc.Col(dbc.Card(
                    [
                    dbc.CardHeader(
                        [
                            html.H5("P/E Ratio",
                                style={'fontSize':'14', 'text-align':'center'}),
                            html.P("Price / Earnings",
                                style={'color': 'Purple', 'fontSize': '14', 'text-align':'center'})
                        ]),
                    dbc.CardBody(
                       [
                           html.H5(className="card-title", id='stock-pe-ratio',
                                style={'color': 'black', 'fontSize': '16'}),
                           html.P("High P/E ratio: Company experiencing growth or potentially overvalued.\
                               Compare company's P/E to others in same industry", className="card-text",
                                style={'color': 'white', 'fontSize': '12'}),
                           #Open url in new tab (target blank)
                           html.A("P/E Ratio explained", href=peRatio_Link, target="_blank")
                       ]
                    )], className="mt-4 shadow"), width=3)
           ]
       )
    ])           

#Input: State of time radio bar and searchbar (value entered)
# Called: When input button is pressed
#  Returns: Table, graph, and general info

@app.callback(Output('stock-name', 'children'), # Stock Name
                Output('stock-ticker', 'children'), # Stock Ticker
                Output('stock-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')], #Input button fires callback
                [State('time-interval-radio', 'value')], #Take radio value state
                [State('ticker-input-searchbar', 'value')]) #Take input searchbar state

#Callback function. Takes inputs (in order), must return all outputs.
# Function is called whenever ANY included inputs are changed
#  State allows you to pass along extra values without firing the callback function
#   So this function is only called when the input (button) is pressed
def return_dashboard(n_clicks, time_value, ticker):
    
    #try:
    #Company Overview call to populate table and headers
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    #Basic stock info (top left of layout)
    stock_name = overview_json.get('Name')
    stock_ticker = ticker

    #Intraday call to populate graph
    #intraday_response = requests.get(api_url + "TIME_SERIES_INTRADAY&interval=15min&symbol=" + ticker + "&apikey=" + api_key)
    #price_data = intraday_response.json()#Maybe redundant, might be able return data in json form already
    if time_value == '1mo':
        period = 60
        #Do alpha vantage api call here for most recent month (year1month1 slice)
        ts = TimeSeries(key=api_key, output_format='pandas')
        data = ts.get_intraday(symbol=ticker, interval='1min', outputsize= 'full')
        
        df = data

        # fig = px.line(data_frame=df, x=0, y=4)


        fig.update_yaxes(tickprefix='$', tickformat=',.2f', nticks=10)
        fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='black', ticklen=10)
    else:
        stock_name = ''
        fig = pgo.Figure(data=[])

    #Return these values to output, in order
    return stock_name, stock_ticker, fig
          
if __name__ == '__main__':
    app.run_server(debug=True)

