import read_cli_argiuments
from record_to_database import *
from scraper import *


def main():
    """Launches the Milestone 2"""
    input_parameters = read_cli_argiuments.get_command_line_params()
    database = DatabaseRecord(user=input_parameters["username"], password=input_parameters["password"],
                              ticker=input_parameters["ticker"])
    scrapper_object = Scraper(ticker=input_parameters["ticker"], max_cards=input_parameters["number_of_news"])

    news_data_lst = scrapper_object.news_data_lst
    database.record_to_database(input_parameters["ticker"], news_data_lst)


if __name__ == "__main__":
    main()
