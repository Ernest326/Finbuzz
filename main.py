import os
from dotenv import load_dotenv
from bot import Bot
from market import Market
import threading

load_dotenv()
secret = os.getenv('API_KEY')

def main():
    if not secret:
        print("Error: Please provide an api_key in a .env called \"API_KEY\"!")
        return
    bot = Bot(secret)
    market = Market(bot)
    bot.start_bot()

if __name__ == "__main__":
    main()