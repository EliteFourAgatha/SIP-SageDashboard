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
app.config.suppress_callback_exceptions = True

api_key = alpha_vantage_api_key
api_url = "https://www.alphavantage.co/query?function="

news_api = news_api_key

# App layout
app.layout = html.Div(
    [
       dbc.Row(dbc.Col(html.H2('Stock Dashboard', style={'text-align':'center'}))),
       dbc.Row(dbc.Col(html.Div(return_input_bar(), style={'margin':'auto'}))),
       dbc.Row(),
       dbc.Row(
           [
               dbc.Col(
                   html.Div(
                       [
                            # Basic info card (name, price, etc.)
                            return_basic_info_card(),

                            # Metrics with links
                            dbc.Row([
                                dbc.Col([
                                    return_ebitda_with_hover(),
                                    return_peRatio_with_hover(),
                                    return_peGRatio_with_hover(),
                                ]),
                                dbc.Col([
                                    return_price_to_book_with_hover(),
                                    return_divYield_with_hover(),
                                ])
                            ])
                       ]), width=6), # End col
                dbc.Col(
                   [
                        # Time radio buttons
                        return_timeinterval(),
                        # Main price graph
                        dcc.Graph(id='stock-price-graph',
                            style={"width":"100%", "height":"80%"},
                            config={'displayModeBar': False})
                   ], width=6) # End col
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
                    ]), width=8),
                #Beta/industry graph
                dbc.Col(
                    [
                        dcc.Graph(id='bar-graph',
                            config={'displayModeBar': False}),
                        dcc.Graph(id='volume-graph',
                            config={'displayModeBar': False})
                    ], width=4), #End col
            ]) #End row
    ]
)           

#Input: State of time radio bar and searchbar (value entered)
# Called: When input button is pressed
#  Returns: Table, graph, and general info
@app.callback(Output('stock-name-and-ticker', 'children'), # Stock Name & (Ticker)
                Output('stock-analyst-price', 'children'), # Analyst stock price
                Output('price-book-test', 'children'), # Price-to-Book Ratio
                Output('ebitda-test', 'children'), # EBITDA
                Output('pe-ratio-test', 'children'), # P/E Ratio
                Output('peg-ratio-test', 'children'), # (P/E)/Growth Ratio
                Output('div-yield-test', 'children'), # Dividend yield %
                Output('stock-price-graph', 'figure'), # Price chart figure
                Output('bar-graph', 'figure'), # Price chart figure
                Output('volume-graph', 'figure'), # Price chart figure
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
    name_ticker_and_price = str(overview_json.get('Name')) + " (" + ticker + ")" + "    " + "CurrentPrice"
    stock_sector = 'Sector: ' + overview_json.get('Sector')
    stock_industry = 'Industry: ' + overview_json.get('Industry')
    stock_target_price = 'Analyst target: ' + str(overview_json.get('AnalystTargetPrice'))

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

    # Explained Metrics
    stock_pe_ratio = overview_json.get('PERatio')
    stock_peg_ratio = overview_json.get('PEGRatio')
    stock_div_yield = overview_json.get('DividendYield')
    stock_ebitda = overview_json.get('EBITDA')
    stock_priceBookRatio = overview_json.get('PriceToBookRatio')

    stock_yearly_high = overview_json.get('52WeekHigh')     #Make this green
    stock_yearly_low = overview_json.get('52WeekLow')    #Make this red

    if time_value == '1mo':
        #Do alpha vantage api call here for most recent month (year1month1 slice)
        ts = TimeSeries(key=api_key, output_format='csv')
        data = ts.get_intraday_extended(symbol=ticker,interval='60min',slice='year1month1')
        
        #csv --> dataframe
        df = pd.DataFrame(list(data[0]))
        #set index column name
        df.index.name = 'date'

        stockBar_fig = return_bar_graph()
        stockVolume_fig = return_volume_graph()
        
        stockPrice_fig = pgo.Figure()
        
        stockPrice_fig.add_trace(pgo.Scatter(x=df[0], y=df[4]))

        stockPrice_fig.update_yaxes(tickprefix='$', tickformat=',.2f', nticks=5)
        stockPrice_fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='black', ticklen=10)
    
    else:
        stockPrice_fig = pgo.Figure(data=[])
        stockBar_fig = pgo.Figure(data=[])
        stockVolume_fig = pgo.Figure(data=[])

    #Industry comparison module
    #Used to determine which exchange stock is in for industry comparison
    exchange = overview_json.get('Exchange')

    #Return these values to output, in order
    return name_ticker_and_price, stock_target_price, \
    stock_priceBookRatio, stock_ebitda,  \
    stock_pe_ratio, stock_peg_ratio, stock_div_yield, \
    stockPrice_fig, stockBar_fig, stockVolume_fig, \
    stock_sector, \
    stock_industry, \
    news_card_one, news_card_two, news_card_three
          
if __name__ == '__main__':
    app.run_server(debug=True)