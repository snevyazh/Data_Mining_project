import argparse
import datetime
from logger import logger
import sys


def get_command_line_params():
    """
    Reads the command line interface and returns the CLI arguments: print with URL (default yes),
    username , password, number of news to show and ticker symbol.
    Raises ValueError exception if number of news is not a number
    :param: none
    :return: list of input parameters in form of a list: username, password to DB, ticker name, dates FROM which to
    parse data and UP TIL which date
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store_true', help="if selected API won't be queried")
    parser.add_argument('username', type=str, help='username')
    parser.add_argument('password', type=str, help='password')
    parser.add_argument('number_of_news', type=int, help='how many news cards to export')
    parser.add_argument('ticker', type=str, help='what ticker you need')
    parser.add_argument('date_from', nargs='*', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                        help='Date from which to parse, format year-month-day')
    parser.add_argument('date_to', nargs=1, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                        help='Up to which date to parse, format year-month-day')
    args = parser.parse_args()
    logger.debug("User input {}".format(args))
    if not isinstance(args.date_from[0], datetime.datetime):
        logger.error("The start date {} is not a datetime.datetime type".format(args.date_from[0]))
        sys.exit()
    if not isinstance(args.date_to[0], datetime.datetime):
        logger.error("The start date is not a datetime.datetime type")
        sys.exit()
    if not str(args.number_of_news).isalpha:
        logger.error("The number of news articles to show entered in command line is not a number")
        sys.exit()
    if (args.date_to[0] - args.date_from[0]).total_seconds() < 0:
        logger.error(("The start date is later than the end day: {} and {}".format(args.date_from[0], args.date_to[0])))
        sys.exit()
    input_parameters = {"api": args.a, "username": args.username, "password": args.password,
                        "number_of_news": args.number_of_news, "ticker": args.ticker, "date_from": args.date_from[0],
                        "date_to": args.date_to[0]}
    logger.debug("User input is parsed {}".format(input_parameters))
    return input_parameters

print(get_command_line_params())