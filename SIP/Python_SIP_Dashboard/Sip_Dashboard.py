import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.graph_objects as pgo
import plotly.express as px
# pd.options.plotting.backend = "plotly"

import yfinance as yf
import shutil, os


import websocket
#TwelveData financial API https://twelvedata.com
import twelvedata
from twelvedata import TDClient

#Initialize Dash App
app = dash.Dash(__name__)

#Initialize TD Client
tdc = TDClient(apikey='e691e3652b094ceeaae6d74239ea6cf9')

ts = tdc.time_series(
    symbol="AAPL",
    interval="1min", #Timeline to search for. Minutes? Days? Months?
    outputsize=10,
    timezone="America/New_York"
)

# Move all of these functions to separate file. Just here to start building functionality.

# Return all stocks currently listed in dictionary for dropdown menu
def get_stock_options(list_stocks):
    # Create a list of dictionaries, with "label" and "value" as keys
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})
    return dict_list

#def get_stock_report(symbol):

#gt.save_tickers(NASDAQ=True, NYSE=True, filename='tickerList.csv')
tickers = gt.get_tickers()
print(tickers)

dataframe = ts.as_pandas()

figure = dataframe.plot()

#ralphPrice = https://api.twelvedata.com/price?symbol=AAPL&apikey=apikey

#ralph = ralph.as_pandas()

#print(ralph)

#print("current price:" + ralphPrice)

# app.layout = html.Div(children=[
                        # Define row element
                        # html.Div(className='row',
                        #children=[
                            #html.Div(className='dropdown column',
                            #children=[
                                #html.H2('Stock Dashboard'),
                                #html.P('Pick one or more stocks from the dropdown below'),
                                #dcc.Dropdown(id='stockdropdown',
                                            #options=get_stock_options(dataframe['symbol'].unique()),
                                            #multi=True,
                                            #value=[dataframe['stock'].sort_values()[0]],
                                            #style={'backgroundColor': '#1E1E1E'},
                                            #className='stockdropdown')
                                    #]),
                            #html.Div(className='data visualization column',
                            #children=[
                                #fig.show(),
                                #html.H2('Data Visualization'),
                                #dcc.Graph(id='timeseriesgraph',
                                        #config={'displayModeBar': False},
                                        #animate=True)
                                    #])
                                #])
                            #])

# **Callbacks are how you add interactivity between components
#  Called whenever user selects a stock from dropdown
#  It takes the selected dropdown value
# @app.callback(Output('timeseriesgraph','figure'), # (ID of output component, property of output component)
                # [Input('stockdropdown','value')]) # (ID of input component, property of input component)

# def update_timeseries(selected_dropdown_value):
    # trace = []
    # dataframeVar = dataframe

if __name__ == '__main__':
    app.run_server(debug=True)

