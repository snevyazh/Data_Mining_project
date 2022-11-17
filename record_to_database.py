import pymysql

def get_sql_query_to_insert_news(ticker_id, news_data_lst):
    """
    Gets SQL query to insert news
    :param ticker_id: ticker_id from the TABLE tickers
    :param news_data_lst: list of news cards (return from scraper.scraper_by_ticker_from_yahoo())
    :return:
    """
    sql_query_to_insert = 'INSERT INTO news (title, author, date, text, url, ticker_id) VALUES'  # TODO to id of tickers
    for news_data in news_data_lst:
        sql_query_to_insert += ' '\
                               + str((news_data["author"], news_data["date_time"], news_data["title"],
                                    news_data["text_body"], news_data["url"], ticker_id)) + ','
    sql_query_to_insert = sql_query_to_insert[:-1] + ';'

    # INSERT INTO TABLE_2 (id, name)
    #     SELECT t1.id, t1.name FROM TABLE_1 t1 WHERE t1.id NOT IN (SELECT id FROM TABLE_2)

    return

def record_to_database(ticker, news_data_lst):
    """
    Records the scraped news into the database "yahoo"
    :param ticker: ticker of company
    :param news_data_lst: list of news cards (return from scraper.scraper_by_ticker_from_yahoo())
    :return:
    """
    # Connect to the database       TODO: change user and password
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='******',
                                 cursorclass=pymysql.cursors.DictCursor)
    # Choose to use the "yahoo" database
    with connection.cursor() as cursor:
        cursor.execute('USE yahoo;')

    # Insert the scraped values into the database
    # Sql query for the insert into TABLE ticker
    sql_query_to_insert = 'INSERT INTO ticker (ticker_name) VALUES ({})'.format(ticker)
    with connection.cursor() as cursor:
        cursor.execute(sql_query_to_insert)

    # Get ticker_id by ticker_name
    ticker_id = SELECT

    # Sql query for the insert into TABLE news
    # Checks if it is not a duplicate
    sql_query_to_insert = get_sql_query_to_insert_news(ticker_id, news_data_lst)
    with connection.cursor() as cursor:
        cursor.execute(sql_query_to_insert)

    return