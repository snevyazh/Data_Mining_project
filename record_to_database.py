import pymysql
#import scraper
from sql_queries import *


def create_connection_to_mysql(user, password):
    """
    Creates connection to MySQL database management system
    :param user: (str) user name
    :param password: (str)
    :return: <pymysql.connections.Connection object>
    """
    connection = pymysql.connect(host='localhost',
                                 user=user,
                                 password=password,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def run_sql(connection, sql_command, return_result=False):
    """
    Runs SQL command for the given connection
    :param connection: <pymysql.connections.Connection object> connection to MySQL database management system
    :param sql_command: (str) sql query
    :param return_result: returns result of SQL query if True (False by default)
    :return: result if the SQL query
    """
    with connection.cursor() as cursor:
        cursor.execute(sql_command)
        if return_result:
            return cursor.fetchall()
    return


def check_duplicate(url, ticker):
    """checks if the news is in the DB already with the assumption that we can have same URL with news,
    but for different ticker"""
    if run_sql(CHECK_DUPLICATE.format(ticker, url)):
        return True
    else:
        return False


def get_sql_query_to_insert_ticker(ticker):
    """
    Gets SQL query to insert ticker's name to TABLE tickers. Checks if ticker exists in the table already.
    :param ticker: (str) e.g. 'BMW.DE'
    :return: SQL query (str)
    """
    sql_query_to_insert = DB_INSERT_TICKER.format(ticker=ticker)
    return sql_query_to_insert


def get_sql_query_to_insert_author(author):
    """
    Gets SQL query to insert author name to TABLE authors. Checks if author exists in the table already.
    :param author_name: (str) e.g. 'John Smith'
    :return: SQL query (str)
    """
    sql_query_to_insert = DB_INSERT_AUTHORS.format(author=author)
    return sql_query_to_insert


def get_sql_query_to_insert_news(news_data_lst):
    """
    Gets SQL query to insert news. Checks duplicates by url
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


def get_sql_query_to_insert_news_ticker(ticker_id, news_id_lst):
    """
    Gets SQL query to insert news_ticker relation. Checks duplicates by news_id AND ticker_id
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


def get_ticker_id(connection, ticker):
    """gets from DB the ticker ID based on given ticker and returns the ticker ID"""
    run_sql(connection, DATABASE_TO_USE)
    result = run_sql(connection, DB_FIND_TICKER.format(ticker=ticker), return_result=True)
    return result[0]['ID']


def get_author_id(connection, author):
    """gets from DB the author ID based on given author name and returns the author ID"""
    run_sql(connection, DATABASE_TO_USE)
    result = run_sql(connection, DB_FIND_AUTHOR.format(author=author), return_result=True)
    return result[0]['ID']


def get_news_id_lst(connection, news_data_lst):
    """gets from DB the news_ID based on given url and returns the ticker ID"""
    run_sql(connection, DATABASE_TO_USE)

    news_id_lst = []
    for news_data in news_data_lst:
        result = run_sql(connection, SELECT_NEWS_DATA.format(news_data=news_data['url']), return_result=True)
        news_id_lst.append(result[0]['ID'])
    return news_id_lst


def record_to_database(connection, ticker, news_data_lst):
    """
    Records the scraped news into the database "yahoo"
    :param connection: <pymysql.connections.Connection object> connection to MySQL database management system
    :param ticker: ticker of company
    :param news_data_lst: list of news cards (return from scraper.scraper_by_ticker_from_yahoo())
    :return:
    """
    # Choose to use the "yahoo" database
    run_sql(connection, DATABASE_TO_USE)

    # Insert the scraped values into the database (checks duplicate)
    # SQL query for the insert into TABLE tickers
    sql_query = get_sql_query_to_insert_ticker(ticker)
    run_sql(connection, sql_query)
    connection.commit()

    # SQL query for the insert into TABLE authors
    for author in [x["author"] for x in news_data_lst]:
        sql_query = get_sql_query_to_insert_author(author)
        run_sql(connection, sql_query)
        connection.commit()


    # get author_id by author name
    for i, value in enumerate([x["author"] for x in news_data_lst]):
        index = get_author_id(connection, value)
        news_data_lst[i]["author_id"] = index

    # Sql query for the insert into TABLE news
    sql_query_to_insert = get_sql_query_to_insert_news(news_data_lst)
    list(map(lambda sql_query: run_sql(connection, sql_query), sql_query_to_insert))
    connection.commit()

    # Sql query for the insert into TABLE news_ticker relation
    # Get ticker_id by ticker_name
    ticker_id = get_ticker_id(connection, ticker)


    # Get news_id by url
    news_id_lst = get_news_id_lst(connection, news_data_lst)
    sql_query_to_insert = get_sql_query_to_insert_news_ticker(ticker_id, news_id_lst)
    list(map(lambda sql_query: run_sql(connection, sql_query), sql_query_to_insert))
    connection.commit()
    return


def create_database(connection):
    """creates the database with desired tables to store news"""

    run_sql(connection, DB_CREATE)
    run_sql(connection, DATABASE_TO_USE)
    # Creates TABLE ticker
    run_sql(connection, DB_CREATE_TABLE_TICKERS)

    run_sql(connection, DB_CREATE_TABLE_AUTHORS)

    run_sql(connection, DB_CREATE_TABLE_NEWS)

    run_sql(connection, DB_CREATE_TABLE_NEWS_TICKERS)

# connection = create_connection_to_mysql(user='root', password='*******')
# create_database(connection)
# for ticker in ['BMW.DE', 'META']:
#     # ticker = 'BMW.DE'
#     news_data_lst = scraper.scraper_by_ticker_from_yahoo(ticker, max_cards=5)
#     record_to_database(connection, ticker, news_data_lst)
