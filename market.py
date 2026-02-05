import yfinance as yf
import time
import threading

class Market:
    def __init__(self, bot, check_interval=60*60*8, per_diff=0.9):
        self.bot = bot
        self.check_interval=check_interval
        self.per_diff=per_diff
        threading.Thread(target=self.market_loop, daemon=True).start()
        threading.Thread(target=self.reset_loop, daemon=True).start()

    def market_loop(self):
        global bot
        while(True):
            time.sleep(10)
            self.bot.broadcast_msg_sync('Test')

    def reset_loop(self):
        while(True):
            time.sleep(3)
            print("Market reset!")

    def get_status(self):
        return "status"
