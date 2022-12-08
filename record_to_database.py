import pymysql
from sql_queries import *
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


class DatabaseRecord:
    """class for all SQL operations """

    def __init__(self, user, password, ticker, api=False, date_from=None, date_to=None):
        """initialise clss with username, password and ticker
            :params: database user, his password and ticker, that was selected to scrape for news
            :return: none. Only initialise the class with input parameters
        """
        self.user = user
        self.password = password
        self.ticker = ticker
        self.connection = self.__create_connection_to_mysql()
        self.__create_database()
        self.date_to = date_to
        self.date_from = date_from
        self.api = api
        self.db_data = 'mysql+pymysql://' + self.user + ':' + self.password + '@' + 'localhost/' + DATABASE
        self.engine = create_engine(self.db_data)

    def __create_connection_to_mysql(self):
        """
        Creates connection to MySQL database management system
        :param: none, takes (str) user name
        :return: <pymysql.connections.Connection object>
        """
        self.connection = pymysql.connect(host='localhost',
                                          user=self.user,
                                          password=self.password,
                                          cursorclass=pymysql.cursors.DictCursor)
        return self.connection

    def run_sql(self, sql_command, return_result=False):
        """
        Runs SQL command for the given connection that is taken from self.connection in class:
        <pymysql.connections.Connection object> connection to MySQL database management system
        :param sql_command: (str) sql query
        :param return_result: returns result of SQL query if True (False by default)
        :return: result if the SQL query
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql_command)
            if return_result:
                return cursor.fetchall()
        return

    def check_duplicate(self, url, ticker):
        """Checks if the news is in the DB already with the assumption that we can have same URL with news,
        but for different ticker
        :param ticker: (str) e.g. 'BMW.DE' to check for duplicate
        :param url: url to the news for this ticker to check
        :return: True is duplicate found and False if not
        """
        if self.run_sql(CHECK_DUPLICATE.format(ticker, url)):
            return True
        else:
            return False

    def check_duplicate_price(self, date, close_price):
        """Checks if the price is in the DB
        :param date: (datetime) date of the price record
        :param close_price: close price for the given date
        :return: True is duplicate found and False if not
        """
        if self.run_sql(CHECK_DUPLICATE.format(date, close_price)):
            return True
        else:
            return False

    def __get_sql_query_to_insert_ticker(self, ticker):
        """
        Gets SQL query to insert ticker's name to TABLE tickers. Checks if ticker exists in the table already.
        :param ticker: (str) e.g. 'BMW.DE'
        :return: SQL query (str)
        """
        sql_query_to_insert = DB_INSERT_TICKER.format(ticker=ticker)
        return sql_query_to_insert

    def __get_sql_query_to_insert_author(self, author):
        """
        Gets SQL query to insert author name to TABLE authors. Checks if author exists in the table already.
        :param author: (str) e.g. 'John Smith'
        :return: SQL query (str)
        """
        sql_query_to_insert = DB_INSERT_AUTHORS.format(author=author)
        return sql_query_to_insert

    def __get_sql_query_to_insert_news(self, news_data_lst):
        """
        Gets SQL query to insert news. Function Checks duplicates by url
        :param news_data_lst: list of news cards (return from scraper.scraper_by_ticker_from_yahoo())
        :return: tuple of 5 SQL queries (str)
        """
        sql_query1 = DATABASE_TO_USE
        sql_query2 = CREATE_TEMP_TABLE_NEWS
        sql_query3 = INSERT_TEMP_TABLE_NEWS
        for news_data in news_data_lst:
            sql_query3 += ' ' \
                          + str((news_data["title"], news_data["author_id"],
                                 news_data["date_time"].isoformat(),
                                 news_data["text_body"], news_data["url"])) + ','
        sql_query3 = sql_query3[:-1] + ';'
        sql_query4 = DB_INSERT_NEWS
        sql_query5 = DROP_TEMP_TABLE
        return sql_query1, sql_query2, sql_query3, sql_query4, sql_query5

    def __get_sql_query_to_insert_news_ticker(self, ticker_id, news_id_lst):
        """
        Gets SQL query to insert news_ticker relation. Function checks duplicates by news_id AND ticker_id
        :param ticker_id: ticker_id from the TABLE tickers
        :param news_id_lst: list of news id
        :return: tuple of 5 SQL queries (str)
        """
        sql_query1 = DATABASE_TO_USE
        sql_query2 = CREATE_TEMP_TABLE_TICKERS
        sql_query3 = INSERT_INTO_TEMP_TABLE_NEWS_TICKER
        for news_id in news_id_lst:
            sql_query3 += ' ' \
                          + str((news_id, ticker_id)) + ','
        sql_query3 = sql_query3[:-1] + ';'
        sql_query4 = DB_INSERT_NEWS_TICKER
        sql_query5 = DROP_TEMP_TABLE
        return sql_query1, sql_query2, sql_query3, sql_query4, sql_query5

    def __get_ticker_id(self, ticker):
        """gets from DB the ticker ID based on given ticker and returns the ticker ID
        :param ticker: ticker entered by user
        :return: ID of the ticker in the database"""
        self.run_sql(DATABASE_TO_USE)
        result = self.run_sql(DB_FIND_TICKER.format(ticker=ticker), return_result=True)
        return result[0]['ID']
        # 0 is index for result list, used locally and will never change

    def __get_news_id(self, ticker_id):
        """gets from DB the news ID based on given ticker and returns the ticker ID
        :param ticker_id: ticker_id for ticker entered by user
        :return: ID of the news in the database in form of list of dictionaries [{'news_id': 1}, {'news_id': 2}]"""
        self.run_sql(DATABASE_TO_USE)
        result = self.run_sql(DB_FIND_NEWS.format(ticker_id=ticker_id), return_result=True)
        print('result', result)
        return result
        # 0 is index for result list, used locally and will never change

    def __get_author_id(self, author):
        """gets from DB the author ID based on given author name and returns the author ID
        :param author: name of the author from news
        :return: ID of the author from the database"""
        self.run_sql(DATABASE_TO_USE)
        result = self.run_sql(DB_FIND_AUTHOR.format(author=author), return_result=True)
        return result[0]['ID']
        # 0 is index for result list, used locally and will never change

    def __get_news_id_lst(self, news_data_lst):
        """gets from DB the news_ID based on given url and returns the ticker ID
        :param news_data_lst: list of news cards (return from scraper.scraper_by_ticker_from_yahoo())
        :return: list of IDs for news from database"""
        self.run_sql(DATABASE_TO_USE)

        news_id_lst = []
        for news_data in news_data_lst:
            result = self.run_sql(SELECT_NEWS_DATA.format(news_data=news_data['url']), return_result=True)
            news_id_lst.append(result[0]['ID'])
        # 0 is index for result list, used locally and will never change
        return news_id_lst

    def __get_sql_query_to_insert_price(self, ticker_id, close_price, date):
        """
        Gets SQL query to insert close_price to TABLE price.
        :param ticker_id: (int) ticker ID from tickers
        :param date: (datetime) date for price identification
        :param close_price: (int) the price for the date given
        :return: SQL query (str)
        """
        sql_query_to_insert = DB_INSERT_PRICE.format(price=close_price, date=date, ticker_id=ticker_id)
        return sql_query_to_insert

    def record_to_database(self, ticker, news_data_lst):
        """
        Records the scraped news into the database "yahoo"
        :param ticker: ticker of company
        :param news_data_lst: list of news cards (return from scraper.scraper_by_ticker_from_yahoo())
        :return:
        """
        self.run_sql(DATABASE_TO_USE)
        sql_query = self.__get_sql_query_to_insert_ticker(ticker)
        self.run_sql(sql_query)
        self.connection.commit()
        for author in [x["author"] for x in news_data_lst]:
            sql_query = self.__get_sql_query_to_insert_author(author)
            self.run_sql(sql_query)
            self.connection.commit()
        for i, value in enumerate([x["author"] for x in news_data_lst]):
            index = self.__get_author_id(value)
            news_data_lst[i]["author_id"] = index
        sql_query_to_insert = self.__get_sql_query_to_insert_news(news_data_lst)
        list(map(lambda sql_query: self.run_sql(sql_query), sql_query_to_insert))
        self.connection.commit()
        ticker_id = self.__get_ticker_id(ticker)
        news_id_lst = self.__get_news_id_lst(news_data_lst)
        sql_query_to_insert = self.__get_sql_query_to_insert_news_ticker(ticker_id, news_id_lst)
        list(map(lambda sql_query: self.run_sql(sql_query), sql_query_to_insert))
        self.connection.commit()
        return

    def record_price_to_database(self, ticker, price_table):
        """
        Records the queried prices from API into the database "yahoo"
        :param ticker: (str) ticker from input
        :param price_table: (dataframe) dataframe of date-price for selected ticker
        :return: none
        """
        ticker_id = self.__get_ticker_id(ticker)
        df_to_sql = pd.DataFrame({'price_date': price_table.index, 'close_price': price_table['close'],
                                  'ticker_id': ticker_id})
        df_to_sql.to_sql('price', con=self.engine, if_exists='append', index=False)

    def __create_database(self):
        """creates the database with desired tables to store news
        :param: none
        :return: none"""
        self.run_sql(DB_CREATE)
        self.run_sql(DATABASE_TO_USE)
        self.run_sql(DB_CREATE_TABLE_TICKERS)
        self.run_sql(DB_CREATE_TABLE_AUTHORS)
        self.run_sql(DB_CREATE_TABLE_NEWS)
        self.run_sql(DB_CREATE_TABLE_NEWS_TICKERS)
        self.run_sql(DB_CREATE_TABLE_PRICE)

    def draw_graph(self, date_start, date_end):
        """draws the fraph of the database: price graph and news graphs
        :param date_start: start date for the graph - the price range start
        :param date_end: stop date for the graph - the price range end
        :return: none"""
        ticker_id = self.__get_ticker_id(self.ticker)
        news_id = pd.DataFrame(self.__get_news_id(ticker_id))
        df_price = pd.read_sql('price', con=self.engine, index_col=None)
        df_price = df_price[df_price['ticker_id'] == ticker_id]
        df_price = df_price[df_price['price_date'] <= date_end]
        df_price = df_price[df_price['price_date'] >= date_start]
        df_news = pd.read_sql('news', con=self.engine, index_col=None)

        df_news = df_news[df_news['news_date'] <= date_end]
        df_news = df_news[df_news['news_date'] >= date_start]

        f, ax = plt.subplots(figsize=(16, 5))
        ax.scatter(df_price['price_date'], df_price['close_price'], label='price')
        for date in df_news['news_date']:
            ax.plot([date, date], [50, 100], color='purple', linestyle='--', linewidth=2, alpha=0.5, label='news')
        ax.set(title='Price over time',
               xlabel='Date',
               ylabel='Purchasing power parity')
        ax.legend(loc=(1, 0.6))
        plt.show()
