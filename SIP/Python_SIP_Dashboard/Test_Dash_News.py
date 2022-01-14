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
import json

#for iterating through newsApi cards
import itertools

from newsapi import NewsApiClient

from Card_Layout import *
from Dashboard_Layout import *
from Stock_Functions import *

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, FONT_AWESOME])

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

news_api = '8ea69eabd7074f14a977d2f1541498f4'

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
               #News module
                dbc.Col(
                    dbc.Card([
                        html.Div(id='news-card-one'),
                        html.Div(id='news-card-two'),
                        html.Div(id='news-card-three')
                        #return_news_card_test(image_url, news_title, news_description, news_url),
                        #return_news_card_test(image_url, news_title, news_description, news_url),
                        #return_news_card_test(image_url, news_title, news_description, news_url),
                    ]),
                width=8),
           ]
       ),
       dbc.Row(
           [
               dbc.Col(
                   dcc.Graph(id='beta-graph'),
                   width=4
               )
           ]
       )
    ])

# Input: State of time radio bar and searchbar (value entered)
#  Returns: Table, graph, and general info
#   Called: When input button is pressed
@app.callback(Output('stock-name', 'children'), # Stock Name
                Output('stock-ticker', 'children'), # Stock Ticker
                Output('news-card-one', 'children'), #Industry
                Output('news-card-two', 'children'), #Industry
                Output('news-card-three', 'children'), #Industry
                [Input('ticker-input-button', 'n_clicks')],
                [State('ticker-input-searchbar', 'value')],
                prevent_initial_call = True)

def return_dashboard(n_clicks, ticker):

    #try:
    #Company Overview call to populate table and headers
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    #Basic stock info (top left of layout)
    stock_name = overview_json.get('Name')
    stock_ticker = ticker

    #Card info
    stock_pe_ratio = overview_json.get('PERatio')
    stock_sector = overview_json.get('Sector')
    stock_industry = overview_json.get('Industry')

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

    #beta_dict = return_industry_dict(ticker, stock_sector, stock_industry)

    beta_dict = return_industry_dict(ticker, stock_sector, stock_industry)
    bar_fig = px.bar(data_frame=beta_dict, x='symbols', y='betas')


    return stock_name, ticker, \
            news_card_one, news_card_two, news_card_three


if __name__ == '__main__':
    app.run_server(debug=True)
