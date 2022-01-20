from enum import auto
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import plotly.graph_objects as pgo
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output

finprep_api_key = "1882bbe25d0a9a496ee5a1e20433c3a4"

# Generate basic display, also includes search bar + button
def return_input_bar():
    return html.Div([
        dbc.Row([
            dbc.Col(width=4),
            dbc.Col(
                html.Div([
                    dcc.Input(id='ticker-input-searchbar', value='', type='text',
                                                placeholder='Enter stock symbol here',
                                                style={'display': 'inline-block', 'width':'70%'}),
                    html.Button('Submit', id='ticker-input-button',
                                        style={'display': 'inline-block', 'width':'30%'})
                        ]), width=4), #Column width
            dbc.Col(width=4),                      
                ]),
            ])
        
# Generate candlestick graph
# Can change this to a line plot later not that much different
def return_candlestick(dataFrame):
    data = []
    data.append(pgo.Candlestick(x=dataFrame['Date'], open=dataFrame['Open'],
                                high=dataFrame['High'], low=dataFrame['Low'],
                                close=dataFrame['Close']))
    layout = {'xaxis':{'title':'Date', 'rangeslider':{'visible': False}},
                'yaxis':{'title':'Price'}, 'hovermode': True}
    return{'data': data, 'layout': layout}

# Returns time interval radio buttons for date range
def return_timeinterval():
    layout = html.Div(
        dcc.RadioItems(id='time-interval-radio',
                        options=[{'label': '2 years', 'value': '2y'},
                                {'label': '1 year', 'value': '1y'},
                                {'label': 'YTD', 'value': 'ytd'},
                                {'label':'6 months', 'value': '6mo'},
                                {'label': '1 month', 'value': '1mo'}
                        ],
                        value='ytd'), #Set default value
                        style={'text-align':'center'})
    return layout

def return_bar_graph():
    figure = px.bar(
            x=['Index', 'A', 'B', 'C', 'D'],
            y=[1, 0.5, -1, 0.4, 0.7]
        )
    figure.update_layout(
        #Set graph margins, remove white padding
        margin=dict(l=25, r=25, t=25, b=25)
    )
    return figure

 #   figure={
  #  'data': [
  #      {'x': [1], 'y': [1.3], 'type': 'bar', 'name': 'Chosen Stock'},
  #      {'x': [1], 'y': [1], 'type': 'bar', 'name': 'S&P Index'},
   #     {'x': [1], 'y': [0.2], 'type': 'bar', 'name': 'Stock2'},
   #     {'x': [1], 'y': [-0.5], 'type': 'bar', 'name': 'Stock5'},
    #    {'x': [1], 'y': [0.4], 'type': 'bar', 'name': 'Stock3'},
 #       {'x': [1], 'y': [1.3], 'type': 'bar', 'name': 'Stock6'},
 #       ],
 #   'layout': {'title': 'Beta', 'y': ''}
 #   }


def return_volume_graph():
    figure = pgo.Figure(
            data=[pgo.Scatter(
                x=[1, 3.2, 5.4, 7.6, 9.8, 12.5],
                y=[1, 3.2, 5.4, 7.6, 9.8, 12.5],
                mode='markers',
                marker_size=[8, 16, 32, 40, 50, 60])
            ],
            layout={'title':'Volume Graph'})
    
    figure.update_layout(
        #Set graph margins, remove white padding
        margin=dict(l=25, r=25, t=25, b=25)
    )
    return figure


def return_industry_dict(ticker, sector, industry):
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
    
    [float (i) for i in values]

    #Add all key/value pairs into dictionary
    for i in range(len(keys)):
        symbols[keys[i]] = values[i]
        # If chosen stock in list, remove
        if keys[i] == ticker:
            del symbols[i]
    
    final_dict = {'symbols': keys, 'betas': values}
    
    return final_dict