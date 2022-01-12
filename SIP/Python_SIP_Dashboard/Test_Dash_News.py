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
                [State('time-interval-radio', 'value')])

def return_dashboard(n_clicks, ticker, time_value):

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

    #News module
    news_response = requests.get('https://newsapi.org/v2/top-headlines?q='+str(stock_name)+'?sources="motley-fool, marketwatch"&apiKey=' + api_key)
    pretty_news_response = json.dumps(news_response.json(), indent=4)
    news_json = json.dumps(news_response.json())
    news_dict = json.loads(news_json)

    card_list = []

    #Iterate through first 3 articles in news_dict
    for artIndex in news_dict['articles'][:3]:
        card = return_news_card_test(news_dict['articles'][artIndex]['title'], 
            news_dict['articles'][artIndex]['description'],
            news_dict['articles'][artIndex]['url'],
            news_dict['articles'][artIndex]['urlToImage'])
        card_list.append(card)
    
    news_card_one = card_list[0]
    news_card_two = card_list[1]
    news_card_three = card_list[2]

    #beta_dict = return_industry_dict(ticker, stock_sector, stock_industry)

    beta_dict = return_industry_dict(ticker, stock_sector, stock_industry)
    bar_fig = px.bar(data_frame=beta_dict, x='symbols', y='betas')


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
    return stock_name, ticker, bar_fig, \
            news_card_one, news_card_two, news_card_three


if __name__ == '__main__':
    app.run_server(debug=True)
