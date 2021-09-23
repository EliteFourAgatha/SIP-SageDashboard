import pandas as pd
from datetime import datetime
import plotly.graph_objects as pgo
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Make specific style changes here, general ones in style.css

# Basic Info Layout #

# Generate basic display, also includes search bar + button
def return_input_bar():
    return html.Div([
                html.Div([
                    html.Div(id='stock-price-input-bar', #change name later, just not 'stock-price'
                                style={'width': '30%', 'display': 'inline-block',
                                    'font-size': '200%'})
                ],style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),
                    html.Div([
                        html.Div([
                            #Stock input bar
                            html.Div(dcc.Input(id='ticker-input-searchbar', value='', type='text',
                                                    placeholder='Please enter stock symbol'),
                                                style={'display': 'inline-block', 'horizontal-align': 'center'}),
                            #Stock input button
                            html.Div(html.Button('Submit', id='ticker-input-button'),
                                            style={'display': 'inline-block'})
                                ]),
                        #Error box for incorrect input
                        html.Div(id='input-error-message', style={'color': 'red'}, children='Error Message Area')
                    ], style={'width':'30%', 'display': 'inline-block'})
        ])

# Returns layout for basic stats (industry, sector, etc.)
# (Consider changing this to being more tabs/cards. Depends if this info needs explanation or not)
def return_table():
    return html.Div([html.Br(), html.Br(), html.Table(id='basic-info-table')
                                                    #columns=[
                                                        #{'name': 'Column1', 'id': 'column1'},
                                                        #{'name': 'Column2', 'id': 'column2'},
                                                        #{'name': 'Column3', 'id': 'column3'},
                                                        #{'name': 'Column4', 'id': 'column4'},

                                                    #])
                                                    ])

# Generate Cards and Graphs #

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