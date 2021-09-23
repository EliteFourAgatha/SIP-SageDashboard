import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as pgo
import requests
import json
from datetime import datetime

from Info_Layout import *
from Graph_Layout import *
from Stock_Functions import *

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

# df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
# df.index = pd.to_datetime(df['Date'])

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
                            dbc.Col(html.H2(id='stock-name')),
                            dbc.Col(html.H2(id='stock-price'))
                        ]),
                        dbc.Row([
                            dbc.Col(html.H2(id='stock-ticker')),
                            dbc.Col(html.H2(id='stock-PE-ratio'))
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
                #Output('main-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')],
                [State('ticker-input-searchbar', 'value')])

#def verify_input():
    #ticker = verify_ticker('AAPL')
def return_stock_graph(n_clicks, ticker):
    
    #try:
    #Intraday call to populate graph
    stock_intraday = requests.get(api_url + "TIME_SERIES_INTRADAY&interval=15min&symbol=" + ticker + "&apikey=" + api_key)
    price_data = stock_intraday.json()#Maybe redundant, might be able return data in json form already

    #Company Overview call to populate table and headers
    stock_overview = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = stock_overview.json()#Maybe redundant, might be able return data in json form already

    stock_name = overview_json.get('Name')
    stock_ticker = ticker
    stock_price = price_data.get('4. Close')
    stock_pe_ratio = overview_json.get('PERatio')

    #fig = return_candlestick(price_data)
    #fig = pgo.Figure(data=[pgo.Scatter(x=[], y=[])])
        
    #except:
        #fig = pgo.Figure(data=[pgo.Scatter(x=[], y=[])])
        #return 'Sorry! Company Not Available', 'No ticker', fig
        #stock_name = 'idkman'
        #stock_ticker = 'unknownticker'

    #Return these values to output, in order
    return stock_name, stock_ticker, stock_price, stock_pe_ratio

    # Example except block from tutorial, returns 10 different values to outputs
    #   in callback. Try to figure out error message. Does it pop up? How would you do that?
    # except:
        # return 'Sorry! Company Not Available', '#######', '$##.##', '##.##', \
		        # {'width':'20%', 'display':'inline-block'}, '##.##%', \
		        # {'width':'20%', 'display':'inline-block'}, \
		        # 'Error! Please try again another Company.', {'data':None}, None
                    
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

