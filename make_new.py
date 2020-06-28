import requests
import datetime

URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=60min&outputsize=full&apikey=ADG1LY1B3G731LNC'

def makeNew(url):
    r = requests.get(url).json()
    print(r)
    if 'Time Series (60min)' in r:
        result = r['Time Series (60min)']
        keys = list(result.keys())
        values = list(result.values())

        new = {'_id': datetime.datetime.strptime(keys[0], '%Y-%m-%d %H:%M:%S'), 'open': values[0]['1. open'], 'high': values[0]['2. high'], 'low': values[0]['3. low'], 'close': values[0]['4. close'], 'volume': values[0]['5. volume']}
        
        return new
    else:
        return 'invalid response'


print(makeNew(URL))