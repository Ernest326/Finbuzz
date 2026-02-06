import yfinance as yf
import time
import threading
from strategy import strategy_eval

testing = False

class Market:
    def __init__(self, bot, update_interval=60*20, window_size=72):
        self.watchlist=[]
        self.data={}

        self.bot = bot
        self.update_interval=update_interval
        self.window_size = window_size
        self.start()
        threading.Thread(target=self.market_loop, daemon=True).start()

    def market_loop(self):
        time.sleep(2) #Wait a lil so that the bot can start up
        while(True):
            print("!!!!UPDATING MARKET DATA!!!!")
            if testing:
                self.data['TSLA'] = {
                    "prices": [10, 20, 30],
                    "stats": {}
                }
                self.data['AMD'] = {
                    "prices": [20, 70, 100, 30, 5],
                    "stats": {}
                }
            else:
                self.fetch_prices()
            self.calculate_data()
            print(str(self.data)+"\n")
            
            for ticker in self.watchlist:
                if strategy_eval(ticker, self.data):
                    print("MARKET DROP ON " + ticker + " --> " + str(self.data[ticker]['stats']))
                    self.bot.broadcast_msg_sync("MARKET DROP ON " + ticker + " --> " + str(self.data[ticker]['stats']))
            
            time.sleep(self.update_interval)

    def fetch_prices(self):
        for ticker in self.watchlist:
            dataset = self.data[ticker]
            stock = yf.Ticker(ticker)
            price = stock.history()['Close'].iloc[-1]
            dataset['prices'].append(price)
            if len(dataset['prices']) > self.window_size:
                dataset.prices.pop(0)

    def calculate_data(self):
        for ticker in self.watchlist:
            dataset = self.data[ticker]
            avg_diff=0
            avg_price=0
            avg_price+=dataset['prices'][0]
            for i in range(1,len(dataset['prices'])):
                avg_diff+=dataset['prices'][i]-dataset['prices'][i-1]
                avg_price+=dataset['prices'][i]
            avg_diff/=len(dataset['prices'])
            avg_price/=len(dataset['prices'])
            self.data[ticker]['stats']['avg_diff']=avg_diff
            self.data[ticker]['stats']['avg_price']=avg_price
            self.data[ticker]['stats']['price_diff']=dataset['prices'][len(dataset['prices'])-1]-dataset['prices'][max(0,len(dataset['prices'])-2)]
            self.data[ticker]['stats']['current_price']=dataset['prices'][len(dataset['prices'])-1]
        
    
    def start(self):
        #Load all tickers we are watching
        if testing:
            self.watchlist.append('TSLA')
            self.watchlist.append('AMD')
        else:
            with open('stocks.txt', 'r') as f:
                for ticker in f.readlines():
                    self.watchlist.append(ticker.rstrip())
                    #Setup our structure
            for ticker in self.watchlist:
                self.data[ticker] = {
                    "prices": [],
                    "stats": {}
                }
