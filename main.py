from pymongo import MongoClient
import requests
import datetime
import json
import time
from bson.objectid import ObjectId


client = MongoClient()
db = client['stock_alpha']

API_KEY = 'ADG1LY1B3G731LNC'
SYMBOLS = ['IBM', 'MSFT', 'AMZN', 'AAPL', 'GOOG', 'NKE', 'KO', 'WMT', 'MCD', 'MERC']
INTERVAL = '60min'
OUTPUT_SIZE = 'full'


def getIntradayStockData(interval='60min', api_key=API_KEY, symbols=SYMBOLS, outputsize=OUTPUT_SIZE):
    counter = 0
    for symbol in symbols:
        if counter == 5:
            print('reached limit, sleeping for 1 min')
            time.sleep(60) # limit 5 requests per min 
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={api_key}'
        result = requests.get(url)
        data = result.json()
        print(data)
        with open(f'results/{symbol.lower()}_alpha_intraday.json', 'w') as f:
            json.dump(data, f)
        counter = counter + 1

def getHistoricalStockData(api_key=API_KEY, symbols=SYMBOLS, output_size=OUTPUT_SIZE):
    counter = 0
    for symbol in symbols:
        if counter == 5:
            print('reached limit sleeping for 1 min')
            time.sleep(60) # limit 5 requests per min 
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={output_size}&apikey={api_key}'
        result = requests.get(url)
        data = result.json()
        print(data)
        with open(f'results/{symbol.lower()}_alpha_historical.json', 'w') as f:
            json.dump(data, f)
        counter = counter + 1

def writeIntradayStockDataToDatabase(symbols=SYMBOLS, interval=INTERVAL):
    start = datetime.datetime.now()

    for symbol in symbols:
        final = []
        with open(f'results/{symbol.lower()}_alpha_intraday.json', 'r') as f:
            data = json.load(f)
            d = data[f'Time Series ({interval})']
        for key, value in d.items():
            tmp = {'_id': datetime.datetime.strptime(key, '%Y-%m-%d %H:%M:%S'), 'open': value['1. open'], 'high': value['2. high'], 'low': value['3. low'], 'close': value['4. close'], 'volume': value['5. volume']}
            final.append(tmp)
        collection = db[f'{symbol.lower()}_alpha']
        collection.delete_many({})
        collection.insert_many(final)

    finish = datetime.datetime.now()

    print(f'elapsed time: {finish - start}')

def writeHistoricalStockDataToDatabase(symbols=SYMBOLS):
    start = datetime.datetime.now()

    for symbol in symbols:
        final = []
        with open(f'results/{symbol.lower()}_alpha_historical.json', 'r') as f:
            data = json.load(f)
            d = data['Time Series (Daily)']
        for key, value in d.items():
            tmp = {'_id': datetime.datetime.strptime(key, '%Y-%m-%d'), 'open': value['1. open'], 'high': value['2. high'], 'low': value['3. low'], 'close': value['4. close'], 'volume': value['5. volume']}
            final.append(tmp)
        collection = db[f'{symbol.lower()}_alpha_historical']
        collection.delete_many({})
        collection.insert_many(final)

    finish = datetime.datetime.now()

    print(f'elapsed time: {finish - start}')





if __name__ == "__main__":

    getIntradayStockData()
    writeIntradayStockDataToDatabase()

    time.sleep(60)

    getHistoricalStockData()
    writeHistoricalStockDataToDatabase()


    
    # example of getting specific timestamp
    print(db['ibm_alpha'].find_one({'_id': datetime.datetime(2020, 6, 26, 14, 30)}))

    # insert one
    db['ibm_alpha'].insert_one({'_id': datetime.datetime(2021, 6, 26, 15, 30), 'test': 'test field'}) 

    # delete one
    #db['ibm_alpha'].delete_one({'_id': datetime.datetime(2021, 6, 26, 15, 30)})

    #example of getting imb database in desc order 
    res = []
    for doc in db['ibm_alpha'].find().sort('_id', -1):
        res.append(doc)

    print(res[0])
    print(res[1])
    print(res[-1])