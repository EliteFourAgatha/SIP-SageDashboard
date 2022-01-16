    #News module with requests API call
    
    #news_response = requests.get('https://newsapi.org/v2/top-headlines?q='+str(stock_name)+'?sources="motley-fool, marketwatch"&apiKey=' + api_key)
    #pretty_news_response = json.dumps(news_response.json(), indent=4)
    #news_json = json.dumps(news_response.json())
    #news_dict = json.loads(news_json)

    #card_list = []

    #Iterate through first 3 articles in news_dict
    #for artIndex in news_dict['articles'][:3]:
        #card = return_news_card_test(news_dict['articles'][artIndex]['title'], 
            #news_dict['articles'][artIndex]['description'],
            #news_dict['articles'][artIndex]['url'],
            #news_dict['articles'][artIndex]['urlToImage'])
        #card_list.append(card)
    
    #news_card_one = card_list[0]
    #news_card_two = card_list[1]
    #news_card_three = card_list[2]

#Old metric cards, too big/clunky, doesn't look good.

#def return_peRatio_card():
#    card = dbc.Card([
#                dbc.CardHeader([
 #                   html.H6("Price / Earnings-to-growth Ratio",
  #                      style={'fontSize':'12', 'text-align':'center'})
   #             ]),
    #            dbc.CardBody([
     #               html.H5(id='stock-pe-ratio',
      #                  style={'color': 'white', 'fontSize': '16', 'text-align':'center'}),
       #             #Open url in new tab (target blank)
        #            html.A(["P/E Ratio", html.Br(), "in-depth"], href=peRatio_Link, target="_blank")
         #       ]),
                
          #  ])
   # return card

  #                         html.Div([
        #                       dbc.Row([
            #                       dbc.Col(
            #                            html.H5(id='stock-name-test'),
             #                      ),
              #                     dbc.Col(
              #                          html.H6(id='stock-ticker-test'),
              #                     ),
               #                     dbc.Col(
                #                        html.H6(id='stock-price-test'),
                 #                  )                             
                 #              ])
                  #         ]),

#Sector/industry cards. Took up too much space on screen.
#def return_industry_card():
  #  card = dbc.Card([
   #         dbc.CardHeader("Industry",
    #            style={'text-align':'center'}),
     #       dbc.CardBody(html.H3(className="card-title", id='stock-industry',
     #           style={'color': 'white', 'fontSize': '11'}))
  #  ])
  #  return card