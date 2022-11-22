
# Finance.yahoo.com webscrapper

This is a code to scrap the news from finance.yahoo.com

# Milestone 2.

The program scrapes the news related to specified company's ticker from finance.yahoo.com and record the data to the MySQL database yahoo.

## Database description

The database yahoo consists of 4 tables.

Table news:
* id: id number of the news article
* title: title of the news article
* author_id: id number of the article's author (see Table authors)
* news_date: datetime of the article's release
* news_text: text content of the article
* url: url to the article

Table authors:
* id: id number of the author
* name: full name of the author

Table tickers:
* id: id number of the ticker
* ticker_name: company ticker label, e.g. 'BMW.DE'

Table news_ticker
* id: id number of the relation news-ticker
* news_id: id number of the news article (see Table news)
* ticker_id: id number of ticker (see Table tickers)


## Command line interface

The program run on Python interpretator with a command line interface in the following way:

python main.py <username>, <password>, <number_of_news>, <ticker>

where
* <username> is user name for the MySQL database management system
* <password> is password for the MySQL database management system
* <number_of_news> is maximal number of news pages scraped for the specified company
* <ticker> is ticker name of the company (e.g. 'BMW.DE')


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


## Tests
the code was tested vs. wrong tickers and mixture of wrong and correct ones. 
the code is not failing, just no info received


## Authors

- [@kuzmatsukanov] (https://github.com/kuzmatsukanov)
- [@snevyazh] (https://github.com/snevyazh/)


## API Reference for future use in the project

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.


## Appendix

Any additional information goes here
