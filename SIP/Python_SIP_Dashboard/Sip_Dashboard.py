import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as pgo
from datetime import datetime

import yfinance as yf
import os

from Sip_Layout import *


import websocket
#TwelveData financial API https://twelvedata.com
import twelvedata
from twelvedata import TDClient


#Initialize Dash App
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

#Initialize TD Client
# tdc = TDClient(apikey='e691e3652b094ceeaae6d74239ea6cf9')

# dataframe = ts.as_pandas()

# Move all of these functions to separate file. Just here to start building functionality.

# Return all stocks currently listed in dictionary for dropdown menu
def get_stock_options(list_stocks):
    # Create a list of dictionaries, with "label" and "value" as keys
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})
    return dict_list

# Load stock data

# df = pd.read_csv('data/Nasdaq_Name&Symbol.csv', index_col=0)
# print(df["Symbol"][0])

df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

# App layout
app.layout = html.Div(children=[
                        # Define row element
                        html.Div(className='row',
                        children=[
                            html.Div(className='dropdown column',
                            children=[
                                html.H2('Stock Dashboard'),
                                html.P('Pick one or more stocks from the dropdown below'),
                                dcc.Dropdown(id='stock-dropdown',
                                            # Options are all possible selections in dropdown.
                                            # Supplying all (unique) stock symbols as options
                                            options=get_stock_options(df['stock'].unique()),
                                            # Can the user select more than one stock at a time?
                                            # Currently false. Search for 1 stock and populate data
                                            multi=False,
                                            value=[df['stock'].sort_values()[0]],
                                            style={'backgroundColor': '#1E1E1E'},
                                            className='stock-dropdown')
                                    ]),
                            html.Div(className='data visualization column',
                            children=[
                                html.H2('Data Visualization'),
                                dcc.Graph(id='timeseries-graph',
                                        config={'displayModeBar': False},
                                        animate=True)
                                    ])
                                ])
                            ])

# **Callbacks add interactivity between components
#  Called whenever user selects a stock from dropdown
#  It takes the selected dropdown value
@app.callback(Output('timeseries-graph','figure'), # (ID of output component, property of output component)
                [Input('stock-dropdown','value')]) # (ID of input component, property of input component)

def update_timeseries(selected_dropdown_value):
    # If x clicked in dropdown & no stock selected. Avoids callback error
    if selected_dropdown_value is None:
        selected_dropdown_value = df['stock'][0]
    trace1 = []
    dataFrame = df
    for stock in selected_dropdown_value:
        trace1.append(pgo.Scatter(x=dataFrame[dataFrame['stock'] == stock].index,
                                y = dataFrame[dataFrame['stock'] == stock]['value'],
                                mode='lines',
                                opacity=0.7,
                                name=stock,
                                textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': pgo.Layout(
                  template='plotly_dark',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'stock price', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [dataFrame.index.min(), dataFrame.index.max()]},
              ),
            }
    
    return figure
 
if __name__ == '__main__':
    app.run_server(debug=True)

