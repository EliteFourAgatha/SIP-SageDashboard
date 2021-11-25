import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas import json_normalize
from pprint import pprint
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mplfinance

from Dashboard_Layout import *
from Stock_Functions import *

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, FONT_AWESOME])

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

# App layout
app.layout = html.Div(
    [
       dbc.Row(dbc.Col(html.H1('Stock Dashboard', style={'text-align':'center'}))),
       dbc.Row(dbc.Col(html.Div(return_input_bar(), style={'margin':'auto'}))),
       dbc.Row(
           [
               dbc.Col(html.H3(id='stock-name')),
               dbc.Col(html.H3(id='stock-ticker'))
           ]
       ),
       dbc.Row(
           [
               dbc.Col(html.Table(id='stock-profile-table'), width=3),
               dbc.Col(
                   [
                        return_timeinterval(),
                        dcc.Graph(id='stock-graph'),
                   ],
                   width=8)
           ]
       )
    ])

# Input: State of time radio bar and searchbar (value entered)
#  Returns: Table, graph, and general info
#   Called: When input button is pressed
@app.callback(Output('stock-name', 'children'), # Stock Name
                Output('stock-ticker', 'children'), # Stock Ticker
                #Output('stock-profile-table', 'children'), # Basic info like industry etc.
                Output('stock-graph', 'figure'), # Price chart figure
                [Input('ticker-input-button', 'n_clicks')],
                [State('ticker-input-searchbar', 'value')],
                [State('time-interval-radio', 'value')])

def return_dashboard(n_clicks, ticker, time_value):
    if time_value == '1mo':
        #Do alpha vantage api call here for most recent month (year1month1 slice)
        ts = TimeSeries(key=api_key, output_format='csv')
        data = ts.get_daily_adjusted(symbol=ticker)
        
        #csv --> dataframe
        df = pd.DataFrame(list(data[0]))
        #set index column name
        df.index.name = 'date'
        # Use drop and tail to remove from dataframe
        #  (compact = 100 data points, only need 30 for 1-month query.
        #   (Drop 77 instead of 70 to account for weekends.)
        df.drop(df.tail(77).index, inplace=True)

        stock_name = 'success_name1'

        fig = pgo.Figure()
        fig.add_trace(pgo.Scatter(x=df[0], y=df[4], fill='tonexty'))



        fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.2f')

        # Get current date and set far-right x-axis marker. (October 21.)
        # Then, use datetime to calculate the date (1-month) ago, and set far-left x-axis marker
        # Do same for other dates (6-month, ytd, etc.)
        current_date = datetime.now()
        month_ago_date = current_date - relativedelta(month=1)
        #tick0 is first x-axis tick, dtick is interval between ticks (M1 = 1 month)
        fig.update_xaxes(tick0=month_ago_date, dtick='M1', tickmode='linear')
    else:
        stock_name = 'error1'
        fig = pgo.Figure(data=[])
    return stock_name, ticker, fig


if __name__ == '__main__':
    app.run_server(debug=True)


# If you just hard-code a ticker, df is a dataframe object.
#  If you try to pass a ticker, df becomes a "textfilereader" object and can't
#    be used as a dataframe, which means can't used read_csv
#      Need new method
#def return_dataframe(ticker):
#    df = pd.read_csv(api_url + 'TIME_SERIES_INTRADAY_EXTENDED&symbol='+ticker+'&interval=60min&slice=year1month2&apikey='+api_key+'&datatype=csv&outputsize=full')
