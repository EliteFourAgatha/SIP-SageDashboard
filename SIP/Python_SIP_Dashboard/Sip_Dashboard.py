import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo
import requests
import plotly.express as px
import datetime
from dateutil.relativedelta import relativedelta

import finnhub
from newsapi import NewsApiClient

from Dashboard_Layout import *
from BasicInfo_Layout import *
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
                                    return_marketcap_with_hover(),
                                    return_peRatio_with_hover(),
                                    return_peGRatio_with_hover(),
                                    return_price_to_book_with_hover(),
                                ]),
                                dbc.Col([
                                    return_eps_with_hover(),
                                    return_divYield_with_hover(),
                                    return_beta_with_hover(),
                                    return_ebitda_with_hover(),
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
                #Beta/industry graph
                dbc.Col(
                    [
                        dcc.Graph(id='bar-graph',
                            config={'displayModeBar': False}),

                    ], 
                    width=6), #End col
                dbc.Col(
                    [
                        dcc.Graph(id='volume-graph',
                            config={'displayModeBar': False})
                    ], 
                    width=6)
            ]), #End row
        dbc.Row(
            [
                #News module
                dbc.Col(
                    dbc.Card([
                        html.Div(id='news-card-one'),
                        html.Div(id='news-card-two'),
                        html.Div(id='news-card-three'),
                        html.Div(id='news-card-four')
                    ]), width=10),
            ]
        )
    ]
)           

#Input: State of time radio bar and searchbar (value entered)
# Called: When input button is pressed
#  Returns: Table, graph, and general info
@app.callback(Output('stock-name-and-ticker', 'children'), # Stock Name & (Ticker)
                Output('stock-analyst-price', 'children'), # Analyst stock price
                Output('market-cap', 'children'), # Market Cap
                Output('eps', 'children'), # EPS
                Output('price-book', 'children'), # Price-to-Book Ratio
                Output('ebitda', 'children'), # EBITDA
                Output('pe-ratio', 'children'), # P/E Ratio
                Output('peg-ratio', 'children'), # (P/E)/Growth Ratio
                Output('div-yield', 'children'), # Dividend yield %
                Output('beta', 'children'), # Beta
                Output('stock-sector', 'children'), # Sector
                Output('stock-industry', 'children'), #Industry
                Output('stock-price-graph', 'figure'), # Price graph
                Output('bar-graph', 'figure'), # Sentiment graph
                Output('volume-graph', 'figure'), # Volume graph
                Output('news-card-one', 'children'),
                Output('news-card-two', 'children'), 
                Output('news-card-three', 'children'),
                Output('news-card-four', 'children'),
                [Input('ticker-input-button', 'n_clicks')], #Input button fires callback
                [State('time-interval-radio', 'value')], #Take radio value state
                [State('ticker-input-searchbar', 'value')], #Take input searchbar state
                prevent_initial_call = True)

# Function is called whenever ANY included inputs are changed
#  State allows you to pass along extra values without firing the callback function
def return_dashboard(n_clicks, time_value, ticker):
    
    try:
        # News section
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

        artFour_title = news_dict['articles'][3]['title']
        artFour_desc = news_dict['articles'][3]['description']
        artFour_url = news_dict['articles'][3]['url']
        artFour_urlImage = news_dict['articles'][3]['urlToImage']

        news_card_one = return_news_card_test(artOne_title, artOne_desc, artOne_url, artOne_urlImage)
        news_card_two = return_news_card_test(artTwo_title, artTwo_desc, artTwo_url, artTwo_urlImage)
        news_card_three = return_news_card_test(artThree_title, artThree_desc, artThree_url, artThree_urlImage)
        news_card_four = return_news_card_test(artFour_title, artFour_desc, artFour_url, artFour_urlImage)
    except:
        return "news test1", "news test2", "news test3", "news test4"
        # Explained Metrics

    #try:
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + api_key)
    overview_json = overview_response.json()


    stock_market_cap = overview_json.get('MarketCapitalization')
    stock_market_cap = int(stock_market_cap)
    stock_market_cap = '${:,}'.format(stock_market_cap)
    stock_eps = overview_json.get('EPS')
    #stock_eps = int(stock_eps)
    #stock_eps = '${:,}'.format(stock_eps)
    stock_pe_ratio = overview_json.get('PERatio')
    stock_peg_ratio = overview_json.get('PEGRatio')
    stock_div_yield = overview_json.get('DividendYield')
    stock_div_yield = float(stock_div_yield)
    stock_div_yield = '{:.1%}'.format(stock_div_yield)
    stock_ebitda = overview_json.get('EBITDA')
    stock_ebitda = int(stock_ebitda)
    stock_ebitda = '${:,}'.format(stock_ebitda)
    stock_priceBookRatio = overview_json.get('PriceToBookRatio')
    stock_beta = overview_json.get('Beta')

    # Main price chart
    # Code common to all time periods:
    finnhub_client = finnhub.Client(api_key=finnhub_api_key)
    now = datetime.now()  # datetime object, current date/time
    now_unix = int(now.timestamp())

    # Time periods
    if time_value == '5D':
        
        five_days_ago_unix = now - relativedelta(days=5)
        five_days_ago_unix = int(five_days_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', five_days_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)        
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark",
                            labels={'t': 'Date', 'c': 'Close'}) #Manual axis labels

        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]   
    
    elif time_value == '1mo':

        month_ago_unix = now - relativedelta(months=1)
        month_ago_unix = int(month_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', month_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s')#Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark",
                            labels={'t': 'Date', 'c': 'Close'}) #Manual axis labels

        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1] 

    elif time_value == '6mo':

        six_month_ago_unix = now - relativedelta(months=6)
        six_month_ago_unix = int(six_month_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', six_month_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark",
                            labels={'t': 'Date', 'c': 'Close'}) #Manual axis labels

        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]

    elif time_value == '3mo':

        three_month_ago_unix = now - relativedelta(months=3)
        three_month_ago_unix = int(three_month_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', three_month_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark",
                            labels={'t': 'Date', 'c': 'Close'}) #Manual axis labels

        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]

    elif time_value == 'ytd':
        
        nowDate = now.date()
        current_year = nowDate.year
        first_day_of_year = datetime(current_year, 1, 1).date()
        days_since_new_year = nowDate - first_day_of_year

        ytd_unix = now - relativedelta(days=days_since_new_year.days)
        ytd_unix = int(ytd_unix.timestamp())

        data = finnhub_client.stock_candles(ticker, 'D', ytd_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark",
                            labels={'t': 'Date', 'c': 'Close'}) #Manual axis labels

        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]
    
    elif time_value == '1y':

        year_ago_unix = now - relativedelta(years=1)
        year_ago_unix = int(year_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', year_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark",
                            labels={'t': 'Date', 'c': 'Close'}) #Manual axis labels

        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]

        trends = finnhub_client.recommendation_trends(ticker)

        trend_df = pd.DataFrame.from_dict(trends)
        #trend_df = trend_df[trend_df.index == 0]
        bar_fig = return_sentiment_bar_graph(trend_df)      

    else:
        stock_fig = pgo.Figure(data=[])
        bar_fig = pgo.Figure(data=[])
        volume_fig = pgo.Figure(data=[])
        stock_price = '$Price_failed'
    
    stock_fig.update_yaxes(
        tickprefix = '$',
        tickformat = ',.2f',
        nticks=7)
    stock_fig.update_xaxes(
        title = '')
    stock_fig.update_layout(margin=dict(l=30, r=30, t=30, b=30)) # Remove white padding

    trends = finnhub_client.recommendation_trends(ticker)

    trend_df = pd.DataFrame.from_dict(trends)
    #trend_df = trend_df[trend_df.index == 0]
    bar_fig = return_sentiment_bar_graph(trend_df)
    #bar_fig = pgo.Figure(data=[])
    
    #Basic stock info (top left of layout)
    ticker.upper() 
    name_ticker_and_price = str(overview_json.get('Name')) + " (" + ticker + ")" + "        $" + str(stock_price)
    stock_sector = 'Sector: ' + str(overview_json.get('Sector'))
    stock_industry = 'Industry: ' + str(overview_json.get('Industry'))
    stock_target_price = 'Analyst target: $' + str(overview_json.get('AnalystTargetPrice'))

    #Return these values to output, in order
    return name_ticker_and_price, stock_target_price, \
    stock_market_cap, stock_eps, \
    stock_priceBookRatio, stock_ebitda,  \
    stock_pe_ratio, stock_peg_ratio, stock_div_yield, stock_beta, \
    stock_sector, stock_industry, \
    stock_fig, bar_fig, volume_fig, \
    news_card_one, news_card_two, news_card_three, news_card_four

    #except:
    #    return "Error retrieving stock", "$$", \
    #    "marketcap", "eps", \
    #    "price/book", "ebitda", \
    #    "p/e ratio", "peg ratio", "divyield", "beta", \
    #    "sector", "industry", pgo.Figure(data=[]), pgo.Figure(data=[]), pgo.Figure(data=[])

          
if __name__ == '__main__':
    app.run_server(debug=True)