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