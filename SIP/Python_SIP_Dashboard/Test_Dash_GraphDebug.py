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
import finnhub

import plotly.express as px

import datetime
import time
from dateutil.relativedelta import relativedelta

from Card_Layout import *
from Dashboard_Layout import *
from Stock_Functions import *
from Keys1 import *

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = alpha_vantage_api_key
api_url = "https://www.alphavantage.co/query?function="

ti = TechIndicators(key=api_key, output_format='pandas')

#CONSIDER REMOVING TIME VALUE ALTOGETHER. JUST PULL DATA AND GRAPH IT.

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
                            html.H3(id='stock-ticker')
                       ]), 
                    width=4),
                dbc.Col(
                   [
                        dcc.Graph(id='stock-graph', animate=True),
                   ],
                    width=8)
            ]
       ),
    ]
)           

@app.callback(Output('stock-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')], #Input button fires callback
                [State('ticker-input-searchbar', 'value')],
                prevent_initial_call = True) #Take input searchbar state

def return_dashboard(n_clicks, ticker):
    
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    #Basic stock info (top left of layout)
    stock_name = overview_json.get('Name')
    stock_ticker = ticker

    finnhub_client = finnhub.Client(api_key=finnhub_api_key)

    # datetime object containing current date and time
    now = datetime.now()
    current_unix = time.mktime(now.timetuple()) * 1000
    current_unix = int(current_unix)

    grab = 1642000725
    grab_light = 1618258721

    year_ago = datetime.now() - relativedelta(years=1)
    year_ago_unix = time.mktime(year_ago.timetuple()) * 1000
    year_ago_unix = int(year_ago_unix)
    #data = finnhub_client.stock_candles(ticker, 'D', 1618258721, grab)
    data = finnhub_client.stock_candles(ticker, 'D', 1590988249, 1591852249)


    #Works if you hard-code in string. Gives "scalar index" error 
    # if ticker supplied from callback ??
    df = pd.DataFrame.from_dict(data)

    #   Need to convert 't' column from unix timecodes to dates





    #df = pd.DataFrame.from_dict(data, orient='index')
    #close_list = df['c'].tolist()
    #time_list = df['t'].tolist()

    #dates_df = pd.to_datetime(df['t'], unit='s', origin='unix')
    df2 = px.data.gapminder().query("continent == 'Oceania'")

    fig = px.line(df, x='t', y='c')

    #ts = TimeSeries(key=api_key, output_format='pandas')
    #data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    
    #df = data
    #df.reset_index(inplace=True)
    #df.set_index("date", inplace=True)
    
    #close = df['4. close']

    #df = df.sort_values(by="t")

    #stock_test = pgo.Figure(data=[pgo.Scatter(x = close_list, y = time_list)])

    #pxline_text = px.line(df, x = "t", y = "c")

    #stockPrice_fig = pgo.Figure(data=[dcc.Graph(
        #figure={
            #'data': [
               # {'x': df['t'], 'y': df['c'], 'type': 'line', 'name': ticker},
           # ],
       #     'layout':{
       #         'title': ticker
     #       }
    #    }
#    )

    return fig

          
if __name__ == '__main__':
    app.run_server(debug=True)

