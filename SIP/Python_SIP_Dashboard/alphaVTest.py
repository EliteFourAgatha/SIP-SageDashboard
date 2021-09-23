import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint
import requests
import json

api_key = "BPE6KMKXLWCGGQW1"
api_url = "https://www.alphavantage.co/query?function="

# currently works, plots graph
# figure out how to do similar
stock_intraday = requests.get(api_url + "TIME_SERIES_INTRADAY&interval=15min&symbol=IBM&apikey=" + api_key)
price_data = stock_intraday.json()
##price_data['4. close'].plot()
#plt.title('Intraday Times Series for the IBM stock (1 min)')
#plt.show()
pprint(price_data)

#stock_overview = requests.get(api_url + "OVERVIEW&symbol=MSFT&apikey=" + api_key)
#stock_overview = stock_overview.json()
#Dumps takes dict as input and returns string
#overview_to_string = json.dumps(stock_overview)
#Loads takes string as input and returns dict
#overview_json = json.loads(overview_to_string)
#pprint(stock_overview)

#stock = requests.get(api_url + "OVERVIEW&symbol=MSFT&apikey=" + api_key)
#data = stock.json()
#info_list = list(data)
#pprint(data['Name'])
