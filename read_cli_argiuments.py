import argparse
import datetime
from logger import logger
import sys


class CommandLineReader:
    def __init__(self):
        return

    def _check_integer(self, input_param):
        """
        Checks if the input is an integer number and converts the input to type of int
        :param input_param: (str)
        :return: (int) input converted to int. If the input is incorrect it logs error.
        """
        if not str(input_param).isdigit():
            logger.error("The number of news articles to show entered in command line is not a number")
            sys.exit()
        return int(input_param)

    def _check_date(self, input_param):
        """
        Checks if the input is a date format and converts the input to type of datetime.datetime
        :param input_param: (str)
        :return: (datetime.datetime) input converted to datetime.datetime. If the input is incorrect it logs error.
        """
        try:
            input_param = datetime.datetime.strptime(input_param, '%Y-%m-%d')
            return input_param
        except ValueError:
            logger.error("The start date {} is not correct format".format(input_param))
            sys.exit()

    def _check_dates_range(self, date1, date2):
        """
        Checks if the input date_start is earlier than the input date_end
        :param date1: (datetime.datetime) date_start
        :param date2: (datetime.datetime) date_end
        :return: Logs error if the input date_start is earlier than the input date_end
        """
        if date1 is None:
            return
        if date2 is None:
            return
        if (date2 - date1).total_seconds() < 0:
            logger.error(("The start date is later than the end day: {} and {}".format(date1, date2)))
            sys.exit()

    def get_command_line_params(self):
        """
        Reads the command line interface and returns the CLI arguments: print with URL (default yes),
        username , password, number of news to show and ticker symbol.
        Raises ValueError exception if number of news is not a number and stops
        :param: none
        :return: list of input parameters in form of a list: username, password to DB, ticker name, dates FROM which to
        parse data and UP TIL which date
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', action='store_true', help="if selected API won't be queried")
        parser.add_argument('username', type=str, help='username')
        parser.add_argument('password', type=str, help='password')
        parser.add_argument('number_of_news', type=self._check_integer, help='how many news cards to export')
        parser.add_argument('ticker', type=str, help='what ticker you need')
        parser.add_argument('date_from', nargs='?', type=self._check_date,
                            help='Date from which to parse, format year-month-day')
        parser.add_argument('date_to', nargs='?', type=self._check_date,
                            help='Up to which date to parse, format year-month-day')
        args = parser.parse_args()
        logger.debug("User input {}".format(args))
        self._check_dates_range(args.date_from, args.date_to)
        input_parameters = {"api": args.a, "username": args.username, "password": args.password,
                            "number_of_news": args.number_of_news, "ticker": args.ticker, "date_from": args.date_from,
                            "date_to": args.date_to}
        logger.debug("User input is parsed {}".format(input_parameters))
        return input_parameters
