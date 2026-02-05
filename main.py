import os
from dotenv import load_dotenv
from bot import Bot
from market import Market

load_dotenv()
secret = os.getenv('API_KEY')

def main():
    if not secret:
        print("Error: API_KEY not found in .env")
        return

    # 1. Initialize Bot
    bot_instance = Bot(secret)

    # 2. Initialize Market, injecting the bot instance
    # Market threads start immediately upon initialization
    market = Market(bot_instance)

    # 3. Start Bot (starts the polling loop, blocks main thread)
    bot_instance.start_bot()

if __name__ == "__main__":
    main()