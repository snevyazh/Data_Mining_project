from datetime import datetime
import pymysql

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
    run_sql("""CREATE TABLE IF NOT EXISTS yahoo.ticker (
              ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              ticker_name VARCHAR(45) NULL)
                ;""")
    run_sql("""CREATE TABLE IF NOT EXISTS news 
        (
        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(45) NULL,
        author VARCHAR(45) NULL,
        news_date DATETIME NULL,
        news_text MEDIUMTEXT NULL,
        url VARCHAR(45) NULL,
        ticker_id INT not null,
        
        FOREIGN KEY (ticker_id)
            REFERENCES ticker(ID)
            ON UPDATE CASCADE ON DELETE RESTRICT
        )
        ;""")


def get_ticker_id(ticker):
    """gets from DB the ticker ID based on given ticker and returns the ticker ID"""
    run_sql("""use yahoo;""")
    result = run_sql(f"select * from ticker where ticker.ticker_name = {ticker};")
    return result


create_database()


