USER = 'root'
PASSWORD = 'barmaglot'
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

