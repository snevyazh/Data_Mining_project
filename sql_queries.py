# USER = 'root'
# PASSWORD = 'barmaglot'

DATABASE_TO_USE = 'use yahoo;'
DB_CREATE = """create database if not exists yahoo;"""
DB_CREATE_TABLE_TICKERS = """CREATE TABLE IF NOT EXISTS tickers (
          ID INT NOT NULL AUTO_INCREMENT,
          ticker_name VARCHAR(45) NULL DEFAULT NULL,
          company_name VARCHAR(100),
          PRIMARY KEY (ID))
            ;"""
DB_CREATE_TABLE_AUTHORS = """CREATE TABLE IF NOT EXISTS authors (
          ID INT NOT NULL AUTO_INCREMENT,
          name VARCHAR(100),
          PRIMARY KEY (ID)
          )
            ;"""

DB_CREATE_TABLE_NEWS = """CREATE TABLE IF NOT EXISTS news (
          ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
          title VARCHAR(255) NULL DEFAULT NULL,
          author_id INT NULL DEFAULT NULL,
          news_date DATETIME NULL DEFAULT NULL,
          news_text MEDIUMTEXT NULL DEFAULT NULL,
          url VARCHAR(500) NULL DEFAULT NULL,
            FOREIGN KEY (author_id)
            REFERENCES authors (ID)
            )
            ;"""

DB_CREATE_TABLE_NEWS_TICKERS = """CREATE TABLE IF NOT EXISTS news_ticker (
          ID INT NOT NULL AUTO_INCREMENT
          PRIMARY KEY,
          news_id INT,
          ticker_id INT,
            FOREIGN KEY(news_id) 
            REFERENCES yahoo.news (ID),
            FOREIGN KEY(ticker_id)
            REFERENCES yahoo.tickers (ID)
            )
            ; """

DB_CREATE_TABLE_PRICE = """
        CREATE TABLE IF NOT EXISTS price
        (
          ID INT NOT NULL AUTO_INCREMENT,
          close_price INT NULL,
          price_date DATETIME NULL,
          ticker_id INT,
          PRIMARY KEY (ID),
            FOREIGN KEY (ticker_id)
            REFERENCES tickers(ID)
        )
        ;"""

DB_FIND_TICKER_URL = """select ID from news where ticker_id = (select ID from ticker where ticker_name = {ticker}) "
               "and url = {url};"""



DB_INSERT_TICKER = """INSERT INTO tickers (ticker_name) SELECT * FROM (SELECT '{ticker}' AS ticker_name) AS temp 
            WHERE NOT EXISTS (SELECT ticker_name FROM tickers WHERE ticker_name = '{ticker}') LIMIT 1;"""

DB_INSERT_AUTHORS = """INSERT INTO authors (name) SELECT * FROM (SELECT '{author}') AS temp WHERE NOT EXISTS 
            (SELECT name FROM authors WHERE name = '{author}') LIMIT 1;"""

CREATE_TEMP_TABLE_NEWS = 'CREATE TEMPORARY TABLE temp_table LIKE news;'

DB_INSERT_NEWS = """
                INSERT INTO news
                (title, author_id, news_date, news_text, url)
                SELECT
                title, author_id, news_date, news_text, url
                FROM temp_table
                WHERE NOT EXISTS (
                  SELECT *
                  FROM news
                  WHERE news.url = temp_table.url
                );
                """

CREATE_TEMP_TABLE_TICKERS = 'CREATE TEMPORARY TABLE temp_table LIKE news_ticker; '

DB_INSERT_NEWS_TICKER = """
                INSERT INTO news_ticker
                (news_id, ticker_id)
                SELECT
                news_id, ticker_id
                FROM temp_table
                WHERE NOT EXISTS (
                  SELECT *
                  FROM news_ticker
                  WHERE news_ticker.ticker_id = temp_table.ticker_id
                    AND news_ticker.news_id = temp_table.news_id
                );
                """
DB_INSERT_PRICE = """           
                INSERT INTO price
                (close_price, price_date, ticker_id) 
                VALUES ({price}, {price_date} , {ticker_id})
                ;
                """

CHECK_PRICE_DUPLICATE = "select ticker_id from price " \
                        "where ticker_id = (select ID from ticker where ticker_id = {}) and price_date = {};"

DB_FIND_PRICE = "select close_price, price_date from price where ticker_id = '{}';"

DB_FIND_TICKER = "select ID from tickers where ticker_name = '{ticker}';"

DB_FIND_AUTHOR = "select ID from authors where name = '{author}';"

CHECK_DUPLICATE = "select ID from news where ticker_id = (select ID from ticker where ticker_name = {}) and url = {};"

DROP_TEMP_TABLE = 'DROP TABLE temp_table;'

SELECT_NEWS_DATA = "select ID from news where url = '{news_data}';"

INSERT_TEMP_TABLE_NEWS = 'INSERT INTO temp_table (title, author_id, news_date, news_text, url) VALUES'

INSERT_INTO_TEMP_TABLE_NEWS_TICKER = 'INSERT INTO temp_table (news_id, ticker_id) VALUES'
