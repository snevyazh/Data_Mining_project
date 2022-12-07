import read_cli_argiuments
from record_to_database import *
from scraper import *


def main():
    """Launches the Milestone 2
        Runs the general functions to read the CLI parameters, create database, scrape the web-site,
        write the scraped news to the database.
        :params: none
        :return: none
        """
    input_parameters = read_cli_argiuments.get_command_line_params()
    database = DatabaseRecord(user=input_parameters["username"], password=input_parameters["password"],
                              ticker=input_parameters["ticker"], date_from=input_parameters["date_from"],
                              date_to=input_parameters['date_to'], api=input_parameters['api'])
    scrapper_object = Scraper(ticker=input_parameters["ticker"], max_cards=input_parameters["number_of_news"])
    if input_parameters['api']:
        price_table = scrapper_object.get_price_table(date_start=input_parameters['date_from'],
                                                      date_end=input_parameters['date_to'])
    news_data_lst = scrapper_object.news_data_lst
    database.record_to_database(input_parameters["ticker"], news_data_lst)
    database.record_price_to_database(ticker=input_parameters['ticker'], price_table=price_table)


if __name__ == "__main__":
    main()
