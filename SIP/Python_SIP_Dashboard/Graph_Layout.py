import pandas as pd
from datetime import datetime
import plotly.graph_objects as pgo
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import yfinance as yf

from Info_Layout import *

# Make specific style changes here, general ones in style.css

# Returns time interval radio buttons for date range
def return_timeinterval():
    layout = html.Div(
        dcc.RadioItems(id='time-interval-radio',
                        options=[{'label':'5 years', 'value':'5y'},
                                {'label': '2 years', 'value': '2y'},
                                {'label': '1 year', 'value': '1y'},
                                {'label': 'YTD', 'value': 'ytd'},
                                {'label':'6 months', 'value': '6mo'},
                                {'label': '1 month', 'value': '1mo'}
                        ],
                        value='ytd'), #Set default value
                        style={'text-align':'center'})
    return layout

# Returns graph layout
def return_graph():
    layout = html.Div([
        html.Br(), #html.line break
        return_timeinterval(),
        dcc.Graph(id='main-graph')
    ])
    return layout

# Returns table and graph in same row. (Refer to reference image)
# (Change this later to different layout that makes more sense)
# *Graph on right side, radio buttons under it, maybe small table of basic info under that?*
# Also, would help if this wasn't exact copy of reference tutorial. Mix it up a bit.
def return_table_graph_layout():
    return html.Div([
                html.Div(return_table(),
                    style={'width': '30%', 'display':'inline-block', 'vertical-align':'top'}),
                html.Div(return_graph(),
                    style={'width': '70%', 'display': 'inline-block', 'vertical-align':'top'})
    ])
     
