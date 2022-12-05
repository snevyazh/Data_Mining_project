import pymysql
from sql_queries import *


class DatabaseRecord:
    """class for all SQL operations """

    def __init__(self, user, password, ticker):
        """initialise clss with username, password and ticker"""
        self.user = user
        self.password = password
        self.ticker = ticker
        self.connection = self.__create_connection_to_mysql()
        self.__create_database()

    def __create_connection_to_mysql(self):
        """
        Creates connection to MySQL database management system
        :param user: (str) user name
        :param password: (str)
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
        """checks if the news is in the DB already with the assumption that we can have same URL with news,
        but for different ticker"""
        if self.run_sql(CHECK_DUPLICATE.format(ticker, url)):
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
        """gets from DB the ticker ID based on given ticker and returns the ticker ID"""
        self.run_sql(DATABASE_TO_USE)
        result = self.run_sql(DB_FIND_TICKER.format(ticker=ticker), return_result=True)
        return result[0]['ID']
        # 0 is index for result list, used locally and will never change

    def __get_author_id(self, author):
        """gets from DB the author ID based on given author name and returns the author ID"""
        self.run_sql(DATABASE_TO_USE)
        result = self.run_sql(DB_FIND_AUTHOR.format(author=author), return_result=True)
        return result[0]['ID']
        # 0 is index for result list, used locally and will never change

    def __get_news_id_lst(self, news_data_lst):
        """gets from DB the news_ID based on given url and returns the ticker ID"""
        self.run_sql(DATABASE_TO_USE)

        news_id_lst = []
        for news_data in news_data_lst:
            result = self.run_sql(SELECT_NEWS_DATA.format(news_data=news_data['url']), return_result=True)
            news_id_lst.append(result[0]['ID'])
        # 0 is index for result list, used locally and will never change
        return news_id_lst

    def record_to_database(self, ticker, news_data_lst):
        """
        Records the scraped news into the database "yahoo"
        :param connection: <pymysql.connections.Connection object> connection to MySQL database management system
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

    def __create_database(self):
        """creates the database with desired tables to store news"""
        self.run_sql(DB_CREATE)
        self.run_sql(DATABASE_TO_USE)
        self.run_sql(DB_CREATE_TABLE_TICKERS)
        self.run_sql(DB_CREATE_TABLE_AUTHORS)
        self.run_sql(DB_CREATE_TABLE_NEWS)
        self.run_sql(DB_CREATE_TABLE_NEWS_TICKERS)

