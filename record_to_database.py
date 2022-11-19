import pymysql
import scraper
#import datetime


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
    Gets SQL query to insert ticker's name to TABLE ticker. Checks if ticker exists in the table already.
    :param ticker: (str) e.g. 'BMW.DE'
    :return: SQL query (str)
    """
    sql_query_to_insert = \
        f"""
        INSERT INTO ticker (ticker_name)
        SELECT * FROM (SELECT '{ticker}' AS ticker_name) AS temp
        WHERE NOT EXISTS (
            SELECT ticker_name FROM ticker WHERE ticker_name = '{ticker}'
        ) LIMIT 1;
        """
    return sql_query_to_insert


def get_sql_query_to_insert_news(ticker_id, news_data_lst):
    """
    Gets SQL query to insert news
    :param ticker_id: ticker_id from the TABLE tickers
    :param news_data_lst: list of news cards (return from scraper.scraper_by_ticker_from_yahoo())
    :return: tuple of 5 SQL queries (str)
    """
    sql_query1 = 'USE yahoo; '
    sql_query2 = 'CREATE TEMPORARY TABLE temp_table LIKE news; '
    sql_query3 = 'INSERT INTO temp_table (title, author, news_date, news_text, url, ticker_id) VALUES'
    for news_data in news_data_lst:
        sql_query3 += ' '\
                    + str((news_data["title"], news_data["author"],
                        news_data["date_time"].isoformat(),
                        news_data["text_body"], news_data["url"], ticker_id)) + ','
    sql_query3 = sql_query3[:-1] + ';'

    sql_query4 = """
                INSERT INTO news
                (title, author, news_date, news_text, url, ticker_id)
                SELECT
                title, author, news_date, news_text, url, ticker_id
                FROM temp_table
                WHERE NOT EXISTS (
                  SELECT *
                  FROM news
                  WHERE news.ticker_id = temp_table.ticker_id
                  AND news.url = temp_table.url
                );
                """
    sql_query5 = 'DROP TABLE temp_table;'
    return sql_query1, sql_query2, sql_query3, sql_query4, sql_query5


def get_ticker_id(connection, ticker):
    """gets from DB the ticker ID based on given ticker and returns the ticker ID"""
    run_sql(connection, """use yahoo;""")
    result = run_sql(connection, f"select ID from ticker where ticker_name = '{ticker}';", return_result=True)
    return result[0]['ID']


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
    # SQL query for the insert into TABLE ticker
    sql_query = get_sql_query_to_insert_ticker(ticker)
    run_sql(connection, sql_query)
    connection.commit()

    # Get ticker_id by ticker_name
    ticker_id = get_ticker_id(connection, ticker)

    # Sql query for the insert into TABLE news
    sql_query_to_insert = get_sql_query_to_insert_news(ticker_id, news_data_lst)
    list(map(lambda sql_query: run_sql(connection, sql_query), sql_query_to_insert))

    connection.commit()
    return


def create_database(connection):
    """creates the database with desired tables to store news"""

    run_sql(connection, """CREATE DATABASE IF NOT EXISTS yahoo;""")
    run_sql(connection, """USE yahoo;""")
    # Creates TABLE ticker
    run_sql(connection,
            """CREATE TABLE IF NOT EXISTS yahoo.ticker (
              ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              ticker_name VARCHAR(45) NULL)
                ;""")
    # Creates TABLE news
    run_sql(connection,
            """CREATE TABLE IF NOT EXISTS news
            (
            ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NULL,
            author VARCHAR(45) NULL,
            news_date DATETIME NULL,
            news_text MEDIUMTEXT NULL,
            url VARCHAR(500) NULL,
            ticker_id INT not null,
    
            FOREIGN KEY (ticker_id)
                REFERENCES ticker(ID)
                ON UPDATE CASCADE ON DELETE RESTRICT
            )
            ;""")


#news_data_lst = [{'author': 'Larry Printz, The Motley Fool', 'date_time': datetime.datetime(2022, 11, 17, 10, 4), 'title': 'Down 20%, Is BMW Stock a Buy?', 'text_body': "Consider BMW Group (OTC: BMWYY), a brand that may not be the first one to spring to mind among automakers, but one that merits consideration. A casual investor might only think of the company's namesake brand, a premium marque with products that, in the U.S. market, start with the $37,400 BMW 230i Coupe and top out with the $145,000 Alpina XB7. This means the majority of BMW models fall well above the cost of an average new car of $48,281.Continue reading", 'url': 'https://finance.yahoo.com/m/95e4eeda-a800-3095-bc53-e185264acf8a/down-20-is-bmw-stock-a-buy-.html'}, {'author': 'Zacks Equity Research', 'date_time': datetime.datetime(2022, 11, 16, 14, 40, 2), 'title': 'Are Investors Undervaluing Bayerische Motoren Werke (BAMXF) Right Now?', 'text_body': 'While the proven Zacks Rank places an emphasis on earnings estimates and estimate revisions to find strong stocks, we also know that investors tend to develop their own individual strategies. With this in mind, we are always looking at value, growth, and momentum trends to discover great companies.Of these, perhaps no stock market trend is more popular than value investing, which is a strategy that has proven to be successful in all sorts of market environments. Value investors rely on traditional forms of analysis on key valuation metrics to find stocks that they believe are undervalued, leaving room for profits.Luckily, Zacks has developed its own Style Scores system in an effort to find stocks with specific traits. Value investors will be interested in the system\'s "Value" category. Stocks with both "A" grades in the Value category and high Zacks Ranks are among the strongest value stocks on the market right now.One company value investors might notice is Bayerische Motoren Werke (BAMXF). BAMXF is currently sporting a Zacks Rank of #1 (Strong Buy), as well as a Value grade of A. The stock has a Forward P/E ratio of 5.86. This compares to its industry\'s average Forward P/E of 8.54. BAMXF\'s Forward P/E has been as high as 7.03 and as low as 4.41, with a median of 5.20, all within the past year.We should also highlight that BAMXF has a P/B ratio of 0.54. The P/B ratio is used to compare a stock\'s market value with its book value, which is defined as total assets minus total liabilities. BAMXF\'s current P/B looks attractive when compared to its industry\'s average P/B of 0.90. Over the past 12 months, BAMXF\'s P/B has been as high as 0.76 and as low as 0.42, with a median of 0.51.Value investors also use the P/S ratio. The P/S ratio is is calculated as price divided by sales. This is a popular metric because sales are harder to manipulate on an income statement, so they are often considered a better performance indicator. BAMXF has a P/S ratio of 0.37. This compares to its industry\'s average P/S of 0.5.Story continuesFinally, we should also recognize that BAMXF has a P/CF ratio of 1.99. This figure highlights a company\'s operating cash flow and can be used to find firms that are undervalued when considering their impressive cash outlook. BAMXF\'s current P/CF looks attractive when compared to its industry\'s average P/CF of 4.26. Within the past 12 months, BAMXF\'s P/CF has been as high as 3.33 and as low as 1.57, with a median of 1.86.If you\'re looking for another solid Automotive - Foreign value stock, take a look at Stellantis (STLA). STLA is a # 1 (Strong Buy) stock with a Value score of A.Shares of Stellantis currently holds a Forward P/E ratio of 3.37, and its PEG ratio is 0.09. In comparison, its industry sports average P/E and PEG ratios of 8.54 and 0.36.Want the latest recommendations from Zacks Investment Research? Today, you can download 7 Best Stocks for the Next 30 Days. Click to get this free report\xa0Bayerische Motoren Werke AG (BAMXF) : Free Stock Analysis Report\xa0Stellantis N.V. (STLA) : Free Stock Analysis Report\xa0To read this article on Zacks.com click here.\xa0Zacks Investment Research', 'url': 'https://finance.yahoo.com/news/investors-undervaluing-bayerische-motoren-werke-144002878.html'}, {'author': 'Zacks Equity Research', 'date_time': datetime.datetime(2022, 11, 10, 14, 40, 2), 'title': 'Are Investors Undervaluing Bayerische Motoren Werke AG Sponsored ADR (BMWYY) Right Now?', 'text_body': 'While the proven Zacks Rank places an emphasis on earnings estimates and estimate revisions to find strong stocks, we also know that investors tend to develop their own individual strategies. With this in mind, we are always looking at value, growth, and momentum trends to discover great companies.Looking at the history of these trends, perhaps none is more beloved than value investing. This strategy simply looks to identify companies that are being undervalued by the broader market. Value investors use tried-and-true metrics and fundamental analysis to find companies that they believe are undervalued at their current share price levels.On top of the Zacks Rank, investors can also look at our innovative Style Scores system to find stocks with specific traits. For example, value investors will want to focus on the "Value" category. Stocks with high Zacks Ranks and "A" grades for Value will be some of the highest-quality value stocks on the market today.One company to watch right now is Bayerische Motoren Werke AG Sponsored ADR (BMWYY). BMWYY is currently sporting a Zacks Rank of #2 (Buy), as well as a Value grade of A. The stock has a Forward P/E ratio of 4.90. This compares to its industry\'s average Forward P/E of 8.16. BMWYY\'s Forward P/E has been as high as 5.21 and as low as 4.23, with a median of 4.61, all within the past year.We should also highlight that BMWYY has a P/B ratio of 0.57. The P/B ratio pits a stock\'s market value against its book value, which is defined as total assets minus total liabilities. This company\'s current P/B looks solid when compared to its industry\'s average P/B of 0.87. Over the past 12 months, BMWYY\'s P/B has been as high as 0.57 and as low as 0.48, with a median of 0.53.Value investors also love the P/S ratio, which is calculated by simply dividing a stock\'s price with the company\'s sales. This is a prefered metric because revenue can\'t really be manipulated, so sales are often a truer performance indicator. BMWYY has a P/S ratio of 0.36. This compares to its industry\'s average P/S of 0.5.These figures are just a handful of the metrics value investors tend to look at, but they help show that Bayerische Motoren Werke AG Sponsored ADR is likely being undervalued right now. Considering this, as well as the strength of its earnings outlook, BMWYY feels like a great value stock at the moment.Want the latest recommendations from Zacks Investment Research? Today, you can download 7 Best Stocks for the Next 30 Days. Click to get this free report\xa0Bayerische Motoren Werke AG Sponsored ADR (BMWYY) : Free Stock Analysis Report\xa0To read this article on Zacks.com click here.\xa0Zacks Investment Research', 'url': 'https://finance.yahoo.com/news/investors-undervaluing-bayerische-motoren-werke-144002762.html'}]

connection = create_connection_to_mysql(user='root', password='******')
for ticker in ['BMW.DE', 'META']:
#ticker = 'BMW.DE'
    news_data_lst = scraper.scraper_by_ticker_from_yahoo(ticker, max_cards=5)
    record_to_database(connection, ticker, news_data_lst)
