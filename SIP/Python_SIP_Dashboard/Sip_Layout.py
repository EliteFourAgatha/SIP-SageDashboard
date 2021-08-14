import pandas as pd
from datetime import datetime
import plotly.graph_objects as pgo
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

##App Layout##

# Generate basic display, also includes search bar + button
def return_infobox_layout():
    return html.Div([
                html.Div([
                    html.Div(id='stock-price',
                                style={'width': '30%', 'display': 'inline-block',
                                    'font-size': '200%'})
                ],style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),
                    html.Div([
                        html.Div([
                            html.Div(dcc.Input(id='ticker-input-searchbar', value='', type='text'),
                                                style={'display': 'inline-block'}), #ticker searchbar style
                            html.Div(html.Button('Submit', id='ticker-input-button'),
                                            style={'display': 'inline-block'})
                                ]),
                        html.Div(id='input-error-message', style={'color': 'red'}, children='Error Box')
                    ], style={'width':'30%', 'display': 'inline-block'})
        ])

# Returns time interval radio buttons for date range
def return_timeinterval_layout():
    layout = html.Div(
        dcc.RadioItems(id='time-interval-radio',
                        options=[{'label':'5 years', 'value':'5y'},
                                {'label':'3 years', 'value': '3y'},
                                {'label': '1 year', 'value': '1y'},
                                {'label': '3 months', 'value': '3mo'},
                                {'label': '1 month', 'value': '1mo'},
                                {'label': 'YTD', 'value':'ytd'}
                        ],
                        value='ytd'),
                        style={'text-align':'center'})
    return layout

# Returns graph layout
def return_graph_layout():
    layout = html.Div([
        html.Br(), #html.line break
        get_timeinterval_layout(),
        dcc.Graph(id='main-graph')
    ])
    return layout

# Returns layout for basic stats (industry, sector, etc.)
# (Consider changing this to being more tabs/cards. Depends if this info needs explanation or not)
def return_table_layout():
    return html.Div([html.Br(), html.Br(), html.Table(id = 'basic-info-table')])

# Returns table and graph in same row. (Refer to reference image)
# (Change this later to different layout that makes more sense)
def return_table_graph_layout():
    return html.Div([
                html.Div(return_table_layout(),
                    style={'width': '30%', 'display':'inline-block', 'vertical-align':'top'}),
                html.Div(return_graph_layout(),
                    style={'width': '70%', 'display': 'inline-block', 'vertical-align':'top'})
    ])