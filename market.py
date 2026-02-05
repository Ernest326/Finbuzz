import yfinance as yf
import time
import threading

class Market:
    def __init__(self, bot, update_interval=60*20, window_size=10, per_diff=0.05):

        self.watchlist=[]
        self.data={}

        self.bot = bot
        self.update_interval=update_interval
        self.window_size = window_size
        self.per_diff=per_diff
        self.start()
        threading.Thread(target=self.market_loop, daemon=True).start()

    def market_loop(self):
        while(True):
            self.fetch_prices()
            self.calculate_data()
            print(self.data)
            time.sleep(self.update_interval)

    def fetch_prices(self):
        for ticker in self.watchlist:
            dataset = self.data[ticker]
            stock = yf.Ticker(ticker)
            price = stock.info['currentPrice'] # TODO: Figure out how to get the current price, this doesnt work
            price=69
            dataset['prices'].append(price)
            if len(dataset['prices']) > self.window_size:
                dataset.prices.pop(0)

    def calculate_data(self):
        for ticker in self.watchlist:
            dataset = self.data[ticker]
            avg=0
            for i in range(1,len(dataset['prices'])):
                avg+=dataset['prices'][i]-dataset['prices'][i-1]
            avg/=len(dataset['prices'])
            self.data[ticker]['stats']['avg']=avg

    
    def start(self):
        #Load all tickers we are watching
        with open('stocks.txt', 'r') as f:
            for ticker in f.readlines():
                self.watchlist.append(ticker.rstrip())

        #Setup our structure
        for ticker in self.watchlist:
            self.data[ticker] = {
                "prices": [],
                "stats": {}
            }
