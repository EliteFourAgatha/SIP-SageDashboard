import plotly.graph_objects as pgo
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from Keys1 import *

# Generate basic display, includes search bar + button
def return_input_bar():
    return html.Div([
        dbc.Row([
            dbc.Col(width=4),
            dbc.Col(
                html.Div([
                    dcc.Input(id='ticker-input-searchbar', value='', type='text',
                                                placeholder='Enter stock symbol',
                                                style={'display': 'inline-block', 'width':'70%'}),
                    html.Button('Submit', id='ticker-input-button',
                                        style={'display': 'inline-block', 'width':'30%'})
                        ]), width=4), #Column width
            dbc.Col(width=4),                      
                ]),
            ])
        
# Returns time interval radio buttons for date range
def return_timeinterval():
    layout = html.Div(
        dcc.RadioItems(id='time-interval-radio',
                        options=[{'label': '1 year', 'value': '1y'},
                                {'label': 'YTD', 'value': 'ytd'},
                                {'label':'6 months', 'value': '6mo'},
                                {'label':'3 months', 'value': '3mo'},
                                {'label': '1 month', 'value': '1mo'},
                                {'label':'5 days', 'value': '5D'},
                        ],
                        value='1mo'), #Set default value
                        style={'text-align':'center'})
    return layout

def return_sentiment_bar_graph(dataFrame):
    # List objects from dataframe
    buy = [dataFrame['buy'][0]]
    sell = [dataFrame['sell'][0]]
    hold = [dataFrame['hold'][0]]
    strongBuy = [dataFrame['strongBuy'][0]]
    strongSell = [dataFrame['strongSell'][0]]

    # Get first (and only) list element
    buy = (buy[0])
    sell = (sell[0])
    hold = (hold[0])
    strongBuy = (strongBuy[0])
    strongSell = [strongSell[0]]

    data_dict = {'Buy': buy, 'Sell': sell, 'Hold': hold, 'Strong Buy': strongBuy, 'Strong Sell': strongSell}
    columns = list(data_dict.keys())
    values = list(data_dict.values())
    bar_colors = ('limegreen', 'indianred', 'gray', 'darkgreen', 'maroon')

    data = [pgo.Bar(
        x = columns,
        y = values
    )]
    figure = pgo.Figure(
        data=data,
        title="Analyst Sentiment")
    figure.update_layout(
        #Set graph margins, remove white padding
        margin=dict(l=30, r=30, t=30, b=30),
        template= "plotly_dark",
        title_x = 0.5,
        title_font_size = 16)
    figure.update_traces(
        marker_color = bar_colors
    )
    figure.update_yaxes(title= '')
    return figure

def return_volume_graph(dataFrame):

    figure = pgo.Figure(
            data=[pgo.Scatter(
                x=dataFrame['t'],
                y=dataFrame['v'],
                mode='markers',
                marker=dict(
                    size= 0.000001 * dataFrame['v'], 
                    sizemin= 8,
                    color= dataFrame['v'], 
                    colorscale= [[0, 'red'], [1, 'green']],
                    showscale= True)
                )
            ],
            layout={
                'title':'Volume'
                })
    
    figure.update_layout(
        #Set graph margins, remove white padding
        margin=dict(l=30, r=30, t=30, b=30),
        template= "plotly_dark",
        title_x= 0.5,
        title_font_size = 20)
    figure.update_yaxes(title= '')
    figure.update_xaxes(title= '')
    return figure