import pymysql
import sys

USER = 'root'
PASSWORD = 'barmaglot'

connection = pymysql.connect(host='localhost',
                             user=USER,
                             password=PASSWORD,
                             )


def run_sql(sql_command):
    """function receives the SQL query and runs it """
    with connection.cursor() as cursor:
        cursor.execute(sql_command)
        result = cursor.fetchall()
        connection.commit()
    return result


def create_database():
    """creates the database with desired tables to store news"""

    run_sql("""create database if not exists yahoo;""")
    run_sql("""use yahoo;""")
    run_sql("""CREATE TABLE IF NOT EXISTS tickers (
              ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              ticker_name VARCHAR(45) NULL)
                ;""")
    run_sql("""CREATE TABLE IF NOT EXISTS news 
            (
            ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NULL,
            author VARCHAR(255) NULL,
            news_date DATETIME NULL,
            news_text MEDIUMTEXT NULL,
            url VARCHAR(500) NULL
            )
            ;""")
    run_sql("""CREATE TABLE IF NOT EXISTS news_ticker (
              ID INT NOT NULL AUTO_INCREMENT
              PRIMARY KEY,
              news_id INT,
              ticker_id INT,
                FOREIGN KEY(news_id) 
                REFERENCES yahoo.news (ID),
                FOREIGN KEY(ticker_id)
                REFERENCES yahoo.ticker (ID)
            )
            ; """)


def get_ticker_id(ticker):
    """gets from DB the ticker ID based on given ticker and returns the ticker ID"""
    run_sql("""use yahoo;""")
    result = run_sql(f"select ID from ticker where ticker_name = '{ticker}';")
    return result[0][0]


def check_duplicate(url, ticker):
    """checks if the news is in the DB already with the assumption that we can have same URL with news,
    but for different ticker"""
    run_sql("""use yahoo;""")
    if run_sql(f"select ID from news join news_ticker on news.ID = news_ticker.ID "
               f"where ticker_id = (select ID from ticker where ticker_name = '{ticker}') "
               f"and url = '{url}';"):
        return True
    else:
        return False



create_database()
check_duplicate()

