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

#Consider putting these in another file
peRatio_Link = "https://www.forbes.com/advisor/investing/what-is-pe-price-earnings-ratio/"
divYield_Link = "https://www.simplysafedividends.com/intelligent-income/posts/1071-dividend-yield-guide-definition-formula-examples-risks"

#News module test links
image_url = 'https://cdn.vox-cdn.com/thumbor/CKp0YjnwF88--mWg1kfPmspvfzY=/0x358:5000x2976/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/22988084/1234440443.jpg'
news_url = 'https://www.theverge.com/2021/11/5/22765098/kroger-bitcoin-cash-cryptocurrency-hoax-pump-dump'  
news_title = 'A fake press release claiming Kroger accepts crypto reached the retailer’s own webpage'
news_description = 'A crypto hoax claimed Kroger is accepting Bitcoin Cash. The fake press release was similar to one targeting Walmart earlier this year. The retailer quickly confirmed it’s fake, but not before the cryptocurrency’s price spiked by $30.'




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
                            html.H3(id='stock-analyst-price'),
                            dbc.Card(
                                [
                                    dbc.CardHeader("Sector",
                                        style={'text-align':'center'}),
                                    dbc.CardBody(html.H2(className="card-title", id='stock-sector',
                                        style={'color': 'black', 'fontSize': '12'}))
                                ]
                            ),
                            dbc.Card(                                
                                [
                                    dbc.CardHeader("Industry",
                                        style={'text-align':'center'}),
                                    dbc.CardBody(html.H3(className="card-title", id='stock-industry',
                                        style={'color': 'black', 'fontSize': '11'}))
                                ]
                            ),
                       ]), 
                    width=5),
                dbc.Col(
                   [
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
                dbc.Col(dbc.Card(
                    [
                    dbc.CardHeader(
                        [
                            html.H6("Price/Earnings (P/E) Ratio",
                                style={'fontSize':'12', 'text-align':'center'}),
                            #html.P("Price / Earnings",
                                #style={'color': 'Purple', 'fontSize': '14', 'text-align':'center'})
                        ]),
                    dbc.CardBody(
                       [
                           html.H5(id='stock-pe-ratio',
                                style={'color': 'black', 'fontSize': '16', 'text-align':'center'}),
                           #html.P("P/E explained here?", className="card-text",
                                #style={'color': 'white', 'fontSize': '12'}),
                           #Open url in new tab (target blank)
                           html.A("P/E Ratio explained", href=peRatio_Link, target="_blank")
                       ]
                    )], className="mt-4 shadow"), width=2),
                dbc.Col(dbc.Card(
                    [
                    dbc.CardHeader(
                        [
                            html.H6("Dividend Yield",
                                style={'fontSize':'12', 'text-align':'center'})
                        ]),
                    dbc.CardBody(
                       [
                           html.H5(id='stock-div-yield',
                                style={'color': 'black', 'fontSize': '16', 'text-align':'center'}),
                           #html.P("Div yield explained here?", className="card-text",
                                #style={'color': 'white', 'fontSize': '12'}),
                           #Open url in new tab (target blank)
                           html.A("Div Yield explained", href=divYield_Link, target="_blank")
                       ]
                    )], className="mt-4 shadow"), width=2),
           ]
       ),
       dbc.Row(
           [
                dbc.Col(
                    dbc.Card([
                        return_news_card_test(image_url, news_title, news_description, news_url),
                        return_news_card_test(image_url, news_title, news_description, news_url),
                        return_news_card_test(image_url, news_title, news_description, news_url),
                    ]),
                width=8),
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
                Output('stock-div-yield', 'children'), # Dividend yield %
                Output('stock-price-graph', 'figure'), # Price chart figure
                Output('stock-sector', 'children'), # Sector
                Output('stock-industry', 'children'), #Industry
                [Input('ticker-input-button', 'n_clicks')], #Input button fires callback
                [State('time-interval-radio', 'value')], #Take radio value state
                [State('ticker-input-searchbar', 'value')]) #Take input searchbar state

#Callback function. Takes inputs (in order), must return all outputs.
# Function is called whenever ANY included inputs are changed
#  State allows you to pass along extra values without firing the callback function
#   So this function is only called when the input (button) is pressed
def return_dashboard(n_clicks, time_value, ticker):
    
    #try:
    #Company Overview call to populate table and headers
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()#Maybe redundant, might be able return data in json form already

    #Basic stock info (top left of layout)
    stock_name = overview_json.get('Name')
    stock_ticker = ticker

    #Used to determine which exchange stock is in for industry comparison
    exchange = overview_json.get('Exchange')

    #Card info
    stock_pe_ratio = overview_json.get('PERatio')
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
    
    elif time_value == '2y':
        
        ts = TimeSeries(key=api_key, output_format='csv')
        data = ts.get_weekly_adjusted(symbol=ticker, datatype='csv')
    else:
        stock_name = ''
        stockPrice_fig = pgo.Figure(data=[])

    stock_price = 'current_stock_price'

    #Return these values to output, in order
    return stock_name, stock_ticker, stock_price, stock_target_price, \
    stock_pe_ratio, stock_div_yield, stockPrice_fig, stock_sector, stock_industry
          
if __name__ == '__main__':
    app.run_server(debug=True)

