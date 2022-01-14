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

#Consider putting these in another file
peRatio_Link = "https://www.forbes.com/advisor/investing/what-is-pe-price-earnings-ratio/"
divYield_Link = "https://www.simplysafedividends.com/intelligent-income/posts/1071-dividend-yield-guide-definition-formula-examples-risks"
peGRatio_Link = "https://www.investopedia.com/ask/answers/012715/what-considered-good-peg-price-earnings-growth-ratio.asp"

# Sector & Industry Cards
def return_sector_card():
    card = dbc.Card([
            dbc.CardHeader("Sector",
                style={'text-align':'center'}),
            dbc.CardBody(html.H2(className="card-title", id='stock-sector',
                style={'color': 'white', 'fontSize': '12'}))
    ])
    return card

def return_industry_card():
    card = dbc.Card([
            dbc.CardHeader("Industry",
                style={'text-align':'center'}),
            dbc.CardBody(html.H3(className="card-title", id='stock-industry',
                style={'color': 'white', 'fontSize': '11'}))
    ])
    return card

# Main metric cards

def return_peRatio_card():
    card = dbc.Card([
                dbc.CardHeader([
                    html.H6("Price / Earnings-to-growth Ratio",
                        style={'fontSize':'12', 'text-align':'center'})
                ]),
                dbc.CardBody([
                    html.H5(id='stock-pe-ratio',
                        style={'color': 'white', 'fontSize': '16', 'text-align':'center'}),
                    #Open url in new tab (target blank)
                    html.A(["P/E Ratio", html.Br(), "in-depth"], href=peRatio_Link, target="_blank")
                ])
            ])
    return card

def return_peGRatio_card():
    card = dbc.Card([
                dbc.CardHeader([
                    html.H6("Price / Earnings-to-growth Ratio",
                        style={'fontSize':'12', 'text-align':'center'})
                ]),
                dbc.CardBody([
                    html.H5(id='stock-peg-ratio',
                        style={'color': 'white', 'fontSize': '16', 'text-align':'center'}),
                    #Open url in new tab (target blank)
                    html.A(["PEG Ratio", html.Br(), "in-depth"], href=peGRatio_Link, target="_blank")
                ])
            ])
    return card

def return_divYield_card():
    card = dbc.Card([
                dbc.CardHeader([
                    html.H6("Dividend Yield (%)",
                        style={'fontSize':'12', 'text-align':'center'})
                ]),
                dbc.CardBody([
                    html.H5(id='stock-div-yield',
                        style={'color': 'white', 'fontSize': '16', 'text-align':'center'}),
                    #Open url in new tab (target blank)
                    html.A(["Dividend Yield", html.Br(), "in-depth"], href=divYield_Link, target="_blank",
                        style={'width':'100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'})
                ])
            ])
    return card

def return_metric_card():
    card = dbc.Card([
            dbc.CardHeader([
                html.H6("_______",
                    style={'fontSize':'12', 'text-align':'center'})
            ]),
            dbc.CardBody([
                html.H5(
                    style={'color': 'white', 'fontSize': '16', 'text-align':'center'}),
                #Open url in new tab (target blank)
                html.A("______ in-depth", href=divYield_Link, target="_blank")
            ])
        ])
    return card

# News cards
def return_news_card(image_source_url, news_title, news_description, news_url):

    card = dbc.CardGroup(
        [
            dbc.Card(
                html.Img(src=image_source_url), #URL Image
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.A(news_title, href=news_url, target="_blank",
                        style={'font-size':'16'}), #Card title (url hyperlink)
                        html.P(news_description,
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

def return_emptyNewsCard():
    card = html.Div()
    return card

def return_noNewsCard():
    card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H1('No breaking news')
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