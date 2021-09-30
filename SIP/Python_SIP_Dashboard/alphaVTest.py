import matplotlib.pyplot as plt
import pandas as pd
from pandas import json_normalize
from pprint import pprint
import requests
import json
import alpha_vantage
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

def return_candlestick(dataFrame):
    data = []
    data.append(pgo.Candlestick(x=dataFrame['Date'], open=dataFrame['Open'],
                                high=dataFrame['High'], low=dataFrame['Low'],
                                close=dataFrame['Close']))
    layout = {'xaxis':{'title':'Date', 'rangeslider':{'visible': False}},
                'yaxis':{'title':'Price'}, 'hovermode': True}
    return{'data': data, 'layout': layout}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div(children=[
    html.Div(html.Button('submit', id='input-button')),
    html.Div(className='figure-class'),
    dcc.Graph(id='main-figure')
])

@app.callback(Output('main-figure', 'children'),
            [Input('input-button', 'num_clicks')])

def return_figure(num_clicks):
    stock_intraday = requests.get(api_url + "TIME_SERIES_INTRADAY&symbol=MSFT&interval=15min&apikey=" + api_key)
    price_data = stock_intraday.json()
    df = json_normalize(price_data)

    fig = return_candlestick(df)
    return fig


#price_data['4. close'].plot()
#plt.title('Intraday Times Series for the IBM stock (1 min)')
#plt.show()

#ts = TimeSeries(key=api_key, output_format='pandas')
#price_data = ts.get_intraday(symbol='MSFT', interval='15min', outputsize='full')

#pprint(price_data[0])
#plt.plot(price_data['4. close'])
#plt.title('microsoft')
#plt.show()

#stock_overview = requests.get(api_url + "OVERVIEW&symbol=MSFT&apikey=" + api_key)
#stock_overview = stock_overview.json()
#Dumps takes dict as input and returns string
#overview_to_string = json.dumps(stock_overview)
#Loads takes string as input and returns dict
#overview_json = json.loads(overview_to_string)
#pprint(stock_overview)

if __name__ == '__main__':
    app.run_server(debug=True)

