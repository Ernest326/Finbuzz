# Evaluating whether or not to 
last_price_diff = 0
def strategy_eval(ticker, data):

    if(len(data[ticker]['prices'])<2):
        return False

    stats = data[ticker]['stats']
    volatility = stats['volatility']
    avg_diff = stats['avg_diff']
    price_diff = stats['price_diff']
    current_price = stats['current_price']
    ema_short = stats['ema_short']
    ema_long = stats['ema_long']
    z_score = stats['z_score']

    if (z_score < -2 and short_ema > long_ema and last_price_diff < 0 and price_diff > 0):
        return True

    last_price_diff = current_price
    return False