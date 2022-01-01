import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
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
                        dcc.Graph(id='stock-graph', animate=True),
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

ts = TimeSeries(key=api_key, output_format='pandas')
ti = TechIndicators(key=api_key, output_format='pandas')

#Input: State of time radio bar and searchbar (value entered)
# Called: When input button is pressed
#  Returns: Table, graph, and general info

@app.callback(Output('stock-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')], #Input button fires callback
                [State('time-interval-radio', 'value')], #Take radio value state
                [State('ticker-input-searchbar', 'value')]) #Take input searchbar state

def return_dashboard(n_clicks, time_value, ticker):
    
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    #Basic stock info (top left of layout)
    stock_name = overview_json.get('Name')
    stock_ticker = ticker

    #if time_value == '1mo':
    period = 60

    data_ts, meta_data_ts = ts.get_intraday(symbol=ticker.upper(), interval='1min', outputsize='full')
    data_ti, meta_data_ti = ti.get_rsi(symbol=ticker, interval='1min', time_period=period)
    df = data_ts[0]

    df.index = pd.Index(map(lambda x: str(x)[:-3], df.index))

    df2 = data_ti

    total_df = pd.concat([df, df2], axis=1, sort=True)

    #Break down dataframes
    openList = []
    for o in total_df['1. open']:
        openList.append(float (o))
    highList = []
    for h in total_df['2. high']:
        highList.append(float (h))
    lowList = []
    for l in total_df['3. low']:
        lowList.append(float (l))
    closeList = []
    for c in total_df['4. close']:
        closeList.append(float (c))
    
    rsi_offset = []
    
    #zip two lists together ('RSI' column from ti and 'low' column)
    # for each value 'r' from RSI and 'l' from low, append to new list
    for r, l in zip(total_df['RSI'], lowList):
        rsi_offset.append(l - (l / r))
    
    #scatter plot for buy / sell / color coding part.
    scatter = pgo.Scatter(

    )
    #actual fig
    mainGraph = pgo.Candlestick(
        x = total_df.index,
        open = openList,
        high = highList,
        low = lowList,
        close = closeList,
        increasing={'line': {'color': '#00CC94'}},
        decreasing={'line': {'color': '#F50030'}},            
        name = 'candlestick'
    )
    data = [mainGraph]

    layout = pgo.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        xaxis = dict(type='category'),
        yaxis = dict(range=[min(rsi_offset), max(highList)]),
        font = dict(color='white'),
    )

        #mainGraph.update_yaxes(tickprefix='$', tickformat=',.2f', nticks=10)
        #mainGraph.update_xaxes(ticks="outside", tickwidth=2, tickcolor='black', ticklen=10)
    #else:
        #stock_name = ''
        #mainGraph = pgo.Figure(data=[])

    #Return these values to output, in order
    return {'data': data, 'layout': layout}
          
if __name__ == '__main__':
    app.run_server(debug=True)

