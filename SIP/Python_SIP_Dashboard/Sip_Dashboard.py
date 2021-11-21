import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
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

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = "BPE6KMKXLWCGGQW1"
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
                            return_profile_table()
                       ]), 
                    width=4),
                dbc.Col(
                   [
                        return_timeinterval(),
                        dcc.Graph(id='stock-graph'),
                   ],
                    width=8)
            ]
       ),
       dbc.Row(
           [
                #dbc.Col(return_profile_table(), width=4),
                dbc.Col(dbc.Card(
                    [
                    dbc.CardHeader("P/E Ratio",
                                style={'fontSize':'20', 'text-align':'center'}),
                    dbc.CardBody(
                       [
                           html.H5(className="card-title", id='stock-pe-ratio',
                                style={'color': 'black', 'fontSize': '16'}),
                           html.P("Description goes here.", className="card-text",
                                style={'color': 'black', 'fontSize': '12'}),
                           #Open url in new tab (target blank)
                           html.A("P/E Ratio explained", href=peRatio_Link, target="_blank")
                       ]
                    )], className="mt-4 shadow", color="white"), width=3)
           ]
       )
    ])           

#Input: State of time radio bar and searchbar (value entered)
# Called: When input button is pressed
#  Returns: Table, graph, and general info

@app.callback(Output('stock-name', 'children'), # Stock Name
                Output('stock-ticker', 'children'), # Stock Ticker
                Output('stock-price', 'children'), # Current Stock Price
                Output('stock-pe-ratio', 'children'),
                Output('stock-graph', 'figure'), # Price chart figure
                Output('stock-profile-table', 'data'), # Company profile
                [Input('ticker-input-button', 'n_clicks')],
                [Input('time-interval-radio', 'value')],
                [State('ticker-input-searchbar', 'value')])

#Callback function. Takes inputs (in order), must return all outputs.
# Function is called whenever ANY included inputs are changed
#  State allows you to pass along extra values without firing the callback function
#   So this function is only called when the input (button) is pressed
def return_dashboard(n_clicks, time_value, ticker):
    
    #try:
    #Company Overview call to populate table and headers
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    stock_name = overview_json.get('Name')
    stock_pe_ratio = overview_json.get('PERatio')
    stock_ticker = ticker
    stock_ebitda = overview_json.get('EBITDA')
    stock_dividend_yield = overview_json.get('DividendYield')

    #
    #Return basic info table here
    table_sector = overview_json.get('Sector')
    table_industry = overview_json.get('Industry')
    table_yearly_high = overview_json.get('52WeekHigh')     #Make this green
    table_yearly_low = overview_json.get('52WeekLow')    #Make this red
    table_target_price = overview_json.get('AnalystTargetPrice')

    table_dataFrame = pd.DataFrame({
        # Values supplied from overview call
        'value':[table_sector, table_industry, table_yearly_high, table_yearly_low, table_target_price]},
        #Index column row titles instead of numbers
        index=['Sector', 'Industry', '52-Week High', '52-Week Low', 'Analyst Target Price'])
    table_data = table_dataFrame.to_dict(orient='records')

    #Intraday call to populate graph
    #intraday_response = requests.get(api_url + "TIME_SERIES_INTRADAY&interval=15min&symbol=" + ticker + "&apikey=" + api_key)
    #price_data = intraday_response.json()#Maybe redundant, might be able return data in json form already
    if time_value == '1mo':
        #Do alpha vantage api call here for most recent month (year1month1 slice)
        ts = TimeSeries(key=api_key, output_format='csv')
        data = ts.get_intraday_extended(symbol=ticker,interval='60min',slice='year1month1')
        
        #csv --> dataframe
        df = pd.DataFrame(list(data[0]))
        #set index column name
        df.index.name = 'date'
        
        
        #Use matplotlib/plotly/better than plotly express for this

        fig = pgo.Figure()
        fig.add_trace(pgo.Scatter(x=df[0], y=df[4]))

        # fig = px.line(data_frame=df, x=0, y=4)


        fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat='.2f')
        fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='black', ticklen=10)
    else:
        stock_name = ''
        fig = pgo.Figure(data=[])

    stock_price = 'current_stock_price'

    #Return these values to output, in order
    return stock_name, stock_ticker, stock_price, stock_pe_ratio, fig, table_data
          
if __name__ == '__main__':
    app.run_server(debug=True)

