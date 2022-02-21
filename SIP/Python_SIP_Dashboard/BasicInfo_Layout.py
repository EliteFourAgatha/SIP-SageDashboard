from enum import auto
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import plotly.graph_objects as pgo
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output

from Metric_Links import *

# Basic info card
def return_basic_info_card():
    card = dbc.Card([
            dbc.CardHeader("",
                id="stock-name-and-ticker",
                style={'text-align':'center'}),
            dbc.CardBody([
                html.Div([
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H6(id='stock-ticker')),
                            dbc.Col(
                                html.H6(id='stock-price'))                             
                        ]
                    ),
                    dbc.Row(
                            dbc.Col(
                                html.H6(id="stock-analyst-price"))
                    ),
                    dbc.Row(
                            dbc.Col(
                                html.H6(id="stock-sector"))
                    ),
                    dbc.Row(
                            dbc.Col(
                                html.H6(id="stock-industry"))
                    )
                ])
            ])
        ])
    return card
# End basic info card


# Main metric functions

def return_marketcap_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "Market Cap: ",
                            id="market-cap-anchor",
                            href=marketcap_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]), #End html.P
            dbc.Tooltip(
            "Basic explanation of market cap goes here",
            target="market-cap-anchor"
                )
            ], className="col-md-5",), #End dbc.Col
            dbc.Col([
                html.P(
                    "",
                    id="market-cap",
                    style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ]) #End dbc.Row
    ]) #End html.Div
    return div

def return_eps_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "EPS: ",
                            id="eps-anchor",
                            href=eps_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]), #End html.P
            dbc.Tooltip(
            "Basic explanation of EPS goes here",
            target="eps-anchor"
                )
            ], className="col-md-5",), #End dbc.Col
            dbc.Col([
                html.P(
                    "",
                    id="eps",
                    style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ]) #End dbc.Row
    ]) #End html.Div
    return div

def return_ebitda_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "EBITDA: ",
                            id="ebitda-ratio-anchor",
                            href=peRatio_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]), #End html.P
            dbc.Tooltip(
            "Basic explanation of ebitda goes here",
            target="ebitda-ratio-anchor"
                )
            ], className="col-md-5",), #End dbc.Col
            dbc.Col([
                html.P(
                    "",
                    id="ebitda",
                    style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ]) #End dbc.Row
    ]) #End html.Div
    return div

def return_peRatio_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "P/E Ratio: ",
                            id="pe-ratio-anchor",
                            href=peRatio_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]), #End html.P
            dbc.Tooltip(
            "Basic explanation of pe goes here",
            target="pe-ratio-anchor"
                )
            ], className="col-md-5",), #End dbc.Col
            dbc.Col([
                html.P(
                    "",
                    id="pe-ratio",
                    style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ]) #End dbc.Row
    ]) #End html.Div
    return div

def return_peGRatio_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "PEG Ratio: ",
                            id="peg-ratio-anchor",
                            href=peGRatio_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]), #End html.P
            dbc.Tooltip(
            "Basic explanation of peg goes here",
            target="peg-ratio-anchor"
                )
            ], className="col-md-5",), #End dbc.Col
            dbc.Col([
                html.P(
                    "",
                    id="peg-ratio",
                    style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ]) #End dbc.Row
    ]) #End html.Div
    return div

def return_divYield_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "Dividend Yield: ",
                            id="div-yield-ratio-anchor",
                            href=divYield_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]), #End html.P
            dbc.Tooltip(
            "Basic explanation of div yield goes here",
            target="div-yield-ratio-anchor"
                )
            ], className="col-md-5",), #End dbc.Col
            dbc.Col([
                html.P(
                    "",
                    id="div-yield",
                    style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ]) #End dbc.Row
    ]) #End html.Div
    return div
def return_price_to_book_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "Price-to-Book Ratio: ",
                            id="price-book-ratio-anchor",
                            href=priceToBook_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]), #End html.P
            dbc.Tooltip(
            "Basic explanation of price to book goes here",
            target="price-book-ratio-anchor"
                )
            ], className="col-md-5",), #End dbc.Col
            dbc.Col([
                html.P(
                    "",
                    id="price-book",
                    style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ]) #End dbc.Row
    ]) #End html.Div
    return div
    
def return_beta_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "Beta: ",
                            id="beta-anchor",
                            href=beta_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]), #End html.P
            dbc.Tooltip(
            "Basic explanation of beta goes here",
            target="beta-anchor"
                )
            ], className="col-md-5",), #End dbc.Col
            dbc.Col([
                html.P(
                    "",
                    id="beta",
                    style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ]) #End dbc.Row
    ]) #End html.Div
    return div

# End metric cards

# News cards
def return_empty_news_card():

    card = dbc.CardGroup(
        [
            dbc.Card(
                html.Img(alt="Picture failed to load.."), #URL Image
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.P("article headline",
                        style={'font-size':'16'}),
                        html.P("article description",
                        style={'font-size':'14'})
                    ]
                )
            )
        ]
    )

    return card
    
def return_news_card_test(news_title, news_description, news_url, image_source_url):

    card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(news_title, href=news_url, target="_blank",
                        style={'font-size':'16', 'text-align':'center'}), #Card title (url hyperlink)
                        dbc.CardImg(
                        src=image_source_url,
                        style={'text-align':'center'}
                        )
                    ],
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.P(news_description,
                                style={'font-size':'12'}
                            )
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    #style={"maxWidth": "540px"},
    )

    return card