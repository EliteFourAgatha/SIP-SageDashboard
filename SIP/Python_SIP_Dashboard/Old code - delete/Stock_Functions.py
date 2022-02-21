#start with function to verify ticker


#Necessary?

#Search through list of possible tickers. If found, return xxx. If not, return xx/error message
def verify_ticker(ticker):
    return 'Wrong Ticker', '#######', '$##.##', '##.##', \
		       {'width':'20%', 'display':'inline-block'}, '##.##%', \
		       {'width':'20%', 'display':'inline-block'}, \
		       'Error! Please try again.', {'data':None}, None

# Generate candlestick graph
# Can change this to a line plot later not that much different
def return_candlestick(dataFrame):
    data = []
    data.append(pgo.Candlestick(x=dataFrame['Date'], open=dataFrame['Open'],
                                high=dataFrame['High'], low=dataFrame['Low'],
                                close=dataFrame['Close']))
    layout = {'xaxis':{'title':'Date', 'rangeslider':{'visible': False}},
                'yaxis':{'title':'Price'}, 'hovermode': True}
    return{'data': data, 'layout': layout}

def return_industry_dict(ticker, sector, industry):
    exchange = 'NYSE'
    marketcapmorethan = '1000000000'
    number_of_companies = 10
    #{} is empty dict
    symbols = {}
    keys = []
    values = []

    screener = requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?sector={sector}&industry={industry}&exchange={exchange}&limit={number_of_companies}&apikey={finprep_api_key}').json()
    #append screener[i] values to lists
    for item in screener:
        keys.append(item['symbol'])
        values.append(item['beta'])
    
    [float (i) for i in values]

    #Add all key/value pairs into dictionary
    for i in range(len(keys)):
        symbols[keys[i]] = values[i]
        # If chosen stock in list, remove
        if keys[i] == ticker:
            del symbols[i]
    
    final_dict = {'symbols': keys, 'betas': values}
    
    return final_dict
