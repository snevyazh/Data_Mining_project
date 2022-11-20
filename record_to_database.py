import pymysql
import scraper


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
    if run_sql(f"select ID from news where ticker_id = (select ID from ticker where ticker_name = '{ticker}') "
               f"and url = '{url}';"):
        return True
    else:
        return False


def get_sql_query_to_insert_ticker(ticker):
    """
    Gets SQL query to insert ticker's name to TABLE tickers. Checks if ticker exists in the table already.
    :param ticker: (str) e.g. 'BMW.DE'
    :return: SQL query (str)
    """
    sql_query_to_insert = \
        f"""
        INSERT INTO tickers (ticker_name)
        SELECT * FROM (SELECT '{ticker}' AS ticker_name) AS temp
        WHERE NOT EXISTS (
            SELECT ticker_name FROM tickers WHERE ticker_name = '{ticker}'
        ) LIMIT 1;
        """
    return sql_query_to_insert


def get_sql_query_to_insert_news(news_data_lst):
    """
    Gets SQL query to insert news. Checks duplicates by url
    :param news_data_lst: list of news cards (return from scraper.scraper_by_ticker_from_yahoo())
    :return: tuple of 5 SQL queries (str)
    """
    sql_query1 = 'USE yahoo; '
    sql_query2 = 'CREATE TEMPORARY TABLE temp_table LIKE news; '
    sql_query3 = 'INSERT INTO temp_table (title, author, news_date, news_text, url) VALUES'
    for news_data in news_data_lst:
        sql_query3 += ' ' \
                      + str((news_data["title"], news_data["author"],
                             news_data["date_time"].isoformat(),
                             news_data["text_body"], news_data["url"])) + ','
    sql_query3 = sql_query3[:-1] + ';'

    sql_query4 = """
                INSERT INTO news
                (title, author, news_date, news_text, url)
                SELECT
                title, author, news_date, news_text, url
                FROM temp_table
                WHERE NOT EXISTS (
                  SELECT *
                  FROM news
                  WHERE news.url = temp_table.url
                );
                """
    sql_query5 = 'DROP TABLE temp_table;'
    return sql_query1, sql_query2, sql_query3, sql_query4, sql_query5


def get_sql_query_to_insert_news_ticker(ticker_id, news_id_lst):
    """
    Gets SQL query to insert news_ticker relation. Checks duplicates by news_id AND ticker_id
    :param ticker_id: ticker_id from the TABLE tickers
    :param news_id_lst: list of news id
    :return: tuple of 5 SQL queries (str)
    """
    sql_query1 = 'USE yahoo; '
    sql_query2 = 'CREATE TEMPORARY TABLE temp_table LIKE news_ticker; '
    sql_query3 = 'INSERT INTO temp_table (news_id, ticker_id) VALUES'
    for news_id in news_id_lst:
        sql_query3 += ' ' \
                      + str((news_id, ticker_id)) + ','
    sql_query3 = sql_query3[:-1] + ';'

    sql_query4 = """
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
    sql_query5 = 'DROP TABLE temp_table;'
    return sql_query1, sql_query2, sql_query3, sql_query4, sql_query5


def get_ticker_id(connection, ticker):
    """gets from DB the ticker ID based on given ticker and returns the ticker ID"""
    run_sql(connection, """use yahoo;""")
    result = run_sql(connection, f"select ID from tickers where ticker_name = '{ticker}';", return_result=True)
    return result[0]['ID']


def get_news_id_lst(connection, news_data_lst):
    """gets from DB the news_ID based on given url and returns the ticker ID"""
    run_sql(connection, """use yahoo;""")

    news_id_lst = []
    for news_data in news_data_lst:
        result = run_sql(connection, f"select ID from news where url = '{news_data['url']}';", return_result=True)
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
    run_sql(connection, 'USE yahoo;')

    # Insert the scraped values into the database (checks duplicate)
    # SQL query for the insert into TABLE tickers
    sql_query = get_sql_query_to_insert_ticker(ticker)
    run_sql(connection, sql_query)
    connection.commit()

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

    run_sql(connection, """CREATE DATABASE IF NOT EXISTS yahoo;""")
    run_sql(connection, """USE yahoo;""")
    # Creates TABLE ticker
    run_sql(connection,
            """CREATE TABLE IF NOT EXISTS tickers (
              ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              ticker_name VARCHAR(45) NULL)
                ;""")
    # Creates TABLE news
    run_sql(connection,
            """CREATE TABLE IF NOT EXISTS news
            (
            ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NULL,
            author VARCHAR(255) NULL,
            news_date DATETIME NULL,
            news_text MEDIUMTEXT NULL,
            url VARCHAR(500) NULL
            )
            ;""")
    # Creates TABLE news_ticker
    run_sql(connection,
            """CREATE TABLE IF NOT EXISTS news_ticker (
              ID INT NOT NULL AUTO_INCREMENT
              PRIMARY KEY,
              news_id INT,
              ticker_id INT,
                FOREIGN KEY(news_id) 
                REFERENCES yahoo.news (ID),
                FOREIGN KEY(ticker_id)
                REFERENCES yahoo.tickers (ID)
            )
            ; """)


# connection = create_connection_to_mysql(user='root', password='*******')
# create_database(connection)
# for ticker in ['BMW.DE', 'META']:
#     # ticker = 'BMW.DE'
#     news_data_lst = scraper.scraper_by_ticker_from_yahoo(ticker, max_cards=5)
#     record_to_database(connection, ticker, news_data_lst)