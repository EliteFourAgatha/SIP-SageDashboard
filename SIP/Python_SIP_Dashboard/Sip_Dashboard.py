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
import json
import itertools #for iterating through newsApi cards

from newsapi import NewsApiClient
import plotly.express as px
import datetime
import mplfinance

from Dashboard_Layout import *
from Card_Layout import *
from Stock_Functions import *
from Keys1 import *

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

api_key = alpha_vantage_api_key
api_url = "https://www.alphavantage.co/query?function="

news_api = news_api_key

# App layout
app.layout = html.Div(
    [
       dbc.Row(dbc.Col(html.H2('Stock Dashboard', style={'text-align':'center'}))),
       dbc.Row(dbc.Col(html.Div(return_input_bar(), style={'margin':'auto'}))),
       dbc.Row(
           [
               dbc.Col(
                   #Basic info (name, price, sector, industry)
                   html.Div(
                       [
                            html.H3(id='stock-name'),
                            html.H3(id='stock-ticker'),
                            html.H3(id='stock-price'),
                            html.H3(id='stock-analyst-price'),
                            return_sector_card(),
                            return_industry_card(),
                       ]), 
                    width=5),
                dbc.Col(
                   [
                       #Radio time buttons + Main graph
                        return_timeinterval(),
                        dcc.Graph(id='stock-price-graph',
                        style={}), #Main Chart
                   ],
                    width=7)
            ]
       ),
       #Row of cards
       dbc.Row(
           [
                dbc.Col(
                    return_peRatio_card(),
                    width=2),
                dbc.Col(
                    return_peGRatio_card(),
                    width=2),
                dbc.Col(
                    return_divYield_card(),
                    width=2),
                dbc.Col(
                    return_metric_card(),
                    width=2),
                dbc.Col(
                    return_metric_card(),
                    width=2),
                dbc.Col(
                    return_metric_card(),
                    width=2),
           ]
       ),
       dbc.Row(
           [
               #News module
                dbc.Col(
                    dbc.Card([
                        html.Div(id='news-card-one'),
                        html.Div(id='news-card-two'),
                        html.Div(id='news-card-three')
                    ]),
                width=8),
                #Beta/industry graph
                dbc.Col(
                    dcc.Graph(id='bar-graph',
                    figure={
                        'data': [
                            {'x': [1], 'y': [1.3], 'type': 'bar', 'name': 'Chosen Stock'},
                            {'x': [1], 'y': [1], 'type': 'bar', 'name': 'S&P Index'},
                            {'x': [1], 'y': [0.2], 'type': 'bar', 'name': 'Stock2'},
                            {'x': [1], 'y': [-0.5], 'type': 'bar', 'name': 'Stock5'},
                            {'x': [1], 'y': [0.4], 'type': 'bar', 'name': 'Stock3'},
                            {'x': [1], 'y': [1.3], 'type': 'bar', 'name': 'Stock6'},
                            ],
                        'layout': {'title': 'Beta'}
                    }),
                    width=4),
           ]
       )
    ]
)           

#Input: State of time radio bar and searchbar (value entered)
# Called: When input button is pressed
#  Returns: Table, graph, and general info
@app.callback(Output('stock-name', 'children'), # Stock Name
                Output('stock-ticker', 'children'), # Stock Ticker
                Output('stock-price', 'children'), # Current stock price
                Output('stock-analyst-price', 'children'), # Analyst stock price
                Output('stock-pe-ratio', 'children'), # P/E Ratio
                Output('stock-peg-ratio', 'children'), # (P/E)/Growth Ratio
                Output('stock-div-yield', 'children'), # Dividend yield %
                Output('stock-price-graph', 'figure'), # Price chart figure
                Output('stock-sector', 'children'), # Sector
                Output('stock-industry', 'children'), #Industry
                Output('news-card-one', 'children'), #Industry
                Output('news-card-two', 'children'), #Industry
                Output('news-card-three', 'children'), #Industry
                [Input('ticker-input-button', 'n_clicks')], #Input button fires callback
                [State('time-interval-radio', 'value')], #Take radio value state
                [State('ticker-input-searchbar', 'value')], #Take input searchbar state
                prevent_initial_call = True)

# Function is called whenever ANY included inputs are changed
#  State allows you to pass along extra values without firing the callback function
def return_dashboard(n_clicks, time_value, ticker):
    
    #try:
    #Company Overview call to populate table and headers
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    #Basic stock info (top left of layout)
    stock_name = overview_json.get('Name')
    stock_ticker = ticker

    news_client = NewsApiClient(api_key=news_api)
    news_dict = news_client.get_everything(qintitle=ticker, language="en")

    artOne_title = news_dict['articles'][0]['title']
    artOne_desc = news_dict['articles'][0]['description']
    artOne_url = news_dict['articles'][0]['url']
    artOne_urlImage = news_dict['articles'][0]['urlToImage']

    artTwo_title = news_dict['articles'][1]['title']
    artTwo_desc = news_dict['articles'][1]['description']
    artTwo_url = news_dict['articles'][1]['url']
    artTwo_urlImage = news_dict['articles'][1]['urlToImage']

    artThree_title = news_dict['articles'][2]['title']
    artThree_desc = news_dict['articles'][2]['description']
    artThree_url = news_dict['articles'][2]['url']
    artThree_urlImage = news_dict['articles'][2]['urlToImage']

    news_card_one = return_news_card_test(artOne_title, artOne_desc, artOne_url, artOne_urlImage)
    news_card_two = return_news_card_test(artTwo_title, artTwo_desc, artTwo_url, artTwo_urlImage)
    news_card_three = return_news_card_test(artThree_title, artThree_desc, artThree_url, artThree_urlImage) 

    #Card info
    stock_pe_ratio = overview_json.get('PERatio')
    stock_peg_ratio = overview_json.get('PEGRatio')
    stock_div_yield = overview_json.get('DividendYield')
    stock_sector = overview_json.get('Sector')
    stock_industry = overview_json.get('Industry')

    #Currently unused, use for cards
    stock_ebitda = overview_json.get('EBITDA')
    stock_dividend_yield = overview_json.get('DividendYield')
    stock_yearly_high = overview_json.get('52WeekHigh')     #Make this green
    stock_yearly_low = overview_json.get('52WeekLow')    #Make this red
    stock_target_price = 'Analyst target:' + str(overview_json.get('AnalystTargetPrice'))

    if time_value == '1mo':
        #Do alpha vantage api call here for most recent month (year1month1 slice)
        ts = TimeSeries(key=api_key, output_format='csv')
        data = ts.get_intraday_extended(symbol=ticker,interval='60min',slice='year1month1')
        
        #csv --> dataframe
        df = pd.DataFrame(list(data[0]))
        #set index column name
        df.index.name = 'date'
        
        stockPrice_fig = pgo.Figure()
        #df[0] is date column, df[4] is close column
        stockPrice_fig.add_trace(pgo.Scatter(x=df[0], y=df[4]))

        stockPrice_fig.update_yaxes(tickprefix='$', tickformat=',.2f', nticks=5)
        stockPrice_fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='black', ticklen=10)
    
    else:
        stock_name = ''
        stockPrice_fig = pgo.Figure(data=[])

    stock_price = 'current_stock_price'

    #Industry comparison module
    #Used to determine which exchange stock is in for industry comparison
    exchange = overview_json.get('Exchange')

    #Return these values to output, in order
    return stock_name, stock_ticker, stock_price, stock_target_price, \
    stock_pe_ratio, stock_peg_ratio, stock_div_yield, stockPrice_fig, stock_sector, \
    stock_industry, \
    news_card_one, news_card_two, news_card_three
          
if __name__ == '__main__':
    app.run_server(debug=True)