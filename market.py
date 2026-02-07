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

        SHORT_EMA = 5
        LONG_EMA = 10

        def ema(prices, period):
            if(len(prices)==0):
                return 0
            alpha = 2/(period+1)
            ema_val = prices[0]

            for p in prices[1:]:
                ema_val = alpha * p + (1 - alpha) * ema_val
            
            return float(ema_val)
        
        for ticker in self.watchlist:
            dataset = self.data[ticker]
            prices = dataset['prices']

            if len(prices)<2:
                continue
                
            arr = np.array(prices)

            # Basic Stats
            avg_price = float(np.mean(arr))
            volatility = float(np.std(arr))

            # Momentum
            diffs = np.diff(arr)
            avg_diff = float(np.mean(diffs))
            price_diff = float(arr[-1] - arr[-2])

            current_price = float(arr[-1])

            # EMA
            ema_short = ema(prices, SHORT_EMA)
            ema_long = ema(prices, LONG_EMA)

            # Z Score
            if volatility > 0:
                z_score = (current_price - avg_price) / volatility
            else:
                z_score = 0.0

            # Trend Detection
            trend = "up" if ema_short > ema_long else "down"

            stats = self.data[ticker]['stats']
            stats['avg_price'] = avg_price
            stats['volatility'] = volatility
            stats['avg_diff'] = avg_diff
            stats['price_diff'] = price_diff
            stats['current_price'] = current_price
            stats['ema_short'] = ema_short
            stats['ema_long'] = ema_long
            stats['z_score'] = z_score
            stats['trend'] = trend

    
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
