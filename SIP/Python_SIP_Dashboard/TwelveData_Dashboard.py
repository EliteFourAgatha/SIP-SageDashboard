import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as pgo
import matplotlib
import mplfinance
from datetime import datetime

import twelvedata
from twelvedata import TDClient

from Info_Layout import *
from Graph_Layout import *
from Stock_Functions import *

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = "e691e3652b094ceeaae6d74239ea6cf9"
td = TDClient(apikey=api_key)

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
                [State('ticker-input-searchbar', 'value')])

#Callback function. Takes inputs (in order), must return all outputs.
def return_stock_graph(n_clicks, ticker):
    
    ts = td.time_series(
        symbol=ticker,
        outputsize=75,
        interval="1day"
    )
    fig = ts.as_pyplot_figure()
    stock_name = "Name: " + ticker
    stock_ticker = ticker
    stock_price = "Price: $0.00"
    stock_pe_ratio = "PERatio: 00"

    #Return these values to output, in order
    return stock_name, stock_ticker, stock_price, stock_pe_ratio, fig


    
#Callback to return candlestick chart if change graph button pressed
# Make sure to set graphtype variable to candlestick
# @app.callback([Output('main-graph', 'figure')],
                # [Input('candlestick-button')]

#
#Callback to return different time period on graph from radio buttons
# ..Might not be necessary, might not have time. I think this is polish.

if __name__ == '__main__':
    app.run_server(debug=True)

