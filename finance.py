import yfinance as yf

""" this is only to check the data acquired through API, as this package is reliable"""

content = yf.Ticker("AAPL")
ticker_info=content.info

# print(apple)
# # print('\n\n\n\n\n\n', apple_info)
print(ticker_info['country'])

# Using the history() method we can get the share price of the stock over a certain period of time.
# Using the period parameter we can set how far back from the present to get data.
# The options for period are 1 day (1d), 5d, 1 month (1mo) , 3mo, 6mo, 1 year (1y), 2y, 5y, 10y, ytd, and max.

ticker_share_price_data = content.history(period="max")
print(ticker_share_price_data.head())

print(ticker_info['sector'])


