import pandas as pd
from datetime import datetime
import plotly.graph_objects as pgo
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output

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
                                ])
                            ])
                    ])

def return_profile_table():
    return dt.DataTable(
        id='stock-profile-table',
        #style_cell={'whiteSpace':'pre-line'}, #Testing this currently try quick refresh
        style_header={'display':'none'}, #Hide headers
        columns=[{'name':'index', 'id': 'index-col'},
                  {'name':'value', 'id':'value-col'}],
        data=[{}]
        #style_data_conditional=[
            #{
                #'if':{

                #}
        #}]
    )
        
#Generate Cards and Graphs #

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
                        options=[{'label':'5 years', 'value':'5y'},
                                {'label': '2 years', 'value': '2y'},
                                {'label': '1 year', 'value': '1y'},
                                {'label': 'YTD', 'value': 'ytd'},
                                {'label':'6 months', 'value': '6mo'},
                                {'label': '1 month', 'value': '1mo'}
                        ],
                        value='ytd'), #Set default value
                        style={'text-align':'center'})
    return layout

# Returns graph layout
def return_graph():
    layout = html.Div([
        html.Br(), #html.line break
        return_timeinterval(),
        dcc.Graph(id='main-graph')
    ])
    return layout