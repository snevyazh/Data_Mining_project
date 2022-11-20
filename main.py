import read_cli_argiuments
import record_to_database
import scraper


def main():
    """Launches the Milestone 2"""

    # Get parameters from terminal given by user
    input_parameters = read_cli_argiuments.get_command_line_params()

    # Create connection to MySQL
    connection = record_to_database.create_connection_to_mysql(user=input_parameters["username"],
                                                               password=input_parameters["password"])
    # Create Database yahoo
    record_to_database.create_database(connection)

    # Scrape news data for the company ticker
    news_data_lst = scraper.scraper_by_ticker_from_yahoo(ticker=input_parameters["ticker"],
                                                         max_cards=input_parameters["number_of_news"])
    # Record the scraped news to the Database yahoo
    record_to_database.record_to_database(connection, input_parameters["ticker"], news_data_lst)
    return


if __name__ == "__main__":
    main()
