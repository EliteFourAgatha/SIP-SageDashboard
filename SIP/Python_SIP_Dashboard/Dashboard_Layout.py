from enum import auto
import pandas as pd
from datetime import datetime
import plotly.graph_objects as pgo
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output

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



#Most likely unneeded, delete later
#
#
#def return_profile_table():
    #return dt.DataTable(
        #id='stock-profile-table',
        #style_cell={'whiteSpace':'pre-line'}, #Testing this currently try quick refresh
        #style_header={'display':'none'}, #Hide headers
        #columns=[{'name':'index', 'id': 'index-value'},
                  #{'name':'value', 'id':'value-col'}],
        #data=[{}]
        #style_data_conditional=[
            #{
                #'if':{

                #}
        #}]
    #)
        
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

#Use beautifulsoup to scrape yahoo finance for alpha/beta of stock, given searched ticker
# Compare to index funds which are always 0.
#  Positive alpha: beat index by (alpha)%. Opposite for negative alpha.
def return_alpha_beta_graph():
    alpha_graph = dcc.Graph(
        figure={
            'layout':{
                'title':'Alpha (risk coefficient)'
            }
        }
    )
    return alpha_graph