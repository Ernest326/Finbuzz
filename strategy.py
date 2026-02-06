def strategy_eval(ticker, data):
    x = data[ticker]
    stats = x['stats']
    diff = stats['price_diff']
    avg_diff = stats['avg_diff']
    avg_price = stats['avg_price']
    price = stats['current_price']
    if(diff<=avg_diff and price<=avg_price-avg_diff*1.5 and len(x['prices'])>=5):
        return True
    return False
    