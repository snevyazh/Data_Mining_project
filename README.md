
# Finance.yahoo.com webscrapper

This is a code to scrap the news and prices from finance.yahoo.com for given ticker

## Code operation
The code runs with CLI parameters with the syntax described below.
User selects the number of news to scrape, the ticker and optionally: dates to gather prices from date...to date.
The code goes to finance.yahoo.com, searches for news for the given ticker, visits all the individual news pages and scrapes the data:
author, date, text of the news.
All scraped data are written to database (see below DB description).
If user chooses to gather price data, the code uses API to finance.yahoo.com and collects all the data for the dates' range provided.
Price data are also written to the database.
The future release will include also graphical comparison of prices vs news based on dates of both.

## Command line interface

The program run on Python interpreter with a command line interface in the following way:

python main.py (-a) <username> <password> <number_of_news> <ticker> (<start date> <stop date>)

where
* **-a** is option to work with API and gather the prices or not. Default is False.
* **username** is username for the MySQL database management system
* **password** is password for the MySQL database management system
* **number_of_news** is maximal number of news pages scraped for the specified company
* **ticker** is ticker name of the company (e.g. 'BMW.DE')
* **start date** , **stop date** define the range of dates to gather price data for the ticker


## Database description

The database yahoo consists of 4 tables.

Table news:
* ID: id number of the news article
* title: title of the news article
* author_id: id number of the article's author (see Table authors)
* news_date: datetime of the article's release
* news_text: text content of the article
* url: url to the article

Table authors:
* ID: id number of the author
* name: full name of the author

Table tickers:
* ID: id number of the ticker
* ticker_name: company ticker label, e.g. 'BMW.DE'

Table news_ticker:
* ID: id number of the relation news-ticker
* news_id: id number of the news article (see Table news)
* ticker_id: id number of ticker (see Table tickers)

Table price:
* ID: id number of the price entry
* price_date: date for the price entry
* close_price: the closure price for the ticker
* ticker_id: foreign key to ticker table, the ID of the ticker


## Tests
The code was tested vs. wrong tickers and mixture of wrong and correct ones. 
The code was tested vs wrong data types on input.
The code was tested vs start date greater than end date.
The code incorporates errors handling and exceptions catching to prevent it from failure in case of minor errors.
Code incorporates logging, where errors are printed to the screen and info and debug information to the file.



## Authors

- [@kuzmatsukanov] (https://github.com/kuzmatsukanov)
- [@snevyazh] (https://github.com/snevyazh/)


## API Reference 

#### Get all items for given ticker and dates

```http
  https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?&interval=1d&period1={start date}&period2={end date}
```

| Parameter  | Type       | Description                                                                 |
|:-----------|:-----------|:----------------------------------------------------------------------------|
| `ticker`   | `string`   | **Required**. ticker to search the prices for                               |
| `period1`  | `datetime` | **Required**. start date                                                    |
| `period2`  | `datetime` | **Required**. end date                                                      |
| `interval` | `int`      | **set by default to 1 day**. Hardcoded. We get prices with  day granularity |



## Appendix. Information about study assignments

# Milestone 1.

1) the program starts with scraper.py

2) it first opens the page and scraps all the news articles

3) the finance.yahoo.com has no paginator, but loads new content once the 
user is reaching the edge. So, the scrapper emulates this behaviour with
Selenium package

4) user inputs the ticker symbol (or list of tickers). The program returns 
the number of articles per ticker defined by user input, and prints them as a table

5) In the table for every news article we gets author, date and news text. Prints URLs 
for every article. 

6) In the future we plan to add API to enrich ticker data with finance info
about the company the ticker represents.

# Milestone 2.

1) The program scrapes the news related to specified company's ticker from finance.yahoo.com 
and records the data to the MySQL database yahoo.

# Milestone 3.
1) The program uses API calls to finance.yahoo.com to gather price data and writes it to the database.



