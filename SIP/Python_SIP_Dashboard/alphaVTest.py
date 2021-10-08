import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

@app.callback(Output('main-figure', 'figure'),
            [Input('input-button', 'n_clicks')])

def return_figure(n_clicks):
    df = pd.read_csv(api_url + 'TIME_SERIES_INTRADAY_EXTENDED&symbol=MSFT&interval=60min&slice=year1month2&apikey='+api_key+'&datatype=csv&outputsize=full')
    x_dates = df['date']

    df_size = len(df['time'])
    df['time'] = np.arange(start = 0, stop = df_size, step = 1, dtype = 'int')
    
    x_labels = []
    for l_date in x_labels:
    date_str = l_date.strftime('%b-%d')
    x_tick_labels.append(date_str)
    ax.set(xticks=loaded_data['date'], xticklabels=x_tick_labels)
    
    fig = pgo.Figure(data=[
                    pgo.Candlestick(x=df['time'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])
    fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.2f')
    return fig


#price_data['4. close'].plot()
#plt.title('Intraday Times Series for the IBM stock (1 min)')
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

