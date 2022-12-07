import argparse


def get_command_line_params():
    """Reads the command line interface and returns the CLI arguments: print with URL (default yes),
    username , password, number of news to show and ticker symbol.
    Raises ValueError exception if number of news is not a number
    :param: none
    :return: list of input parameters in form of a list
        """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store_true', help="if selected URL won't be printed")
    parser.add_argument('username', type=str, help='username')
    parser.add_argument('password', type=str, help='password')
    parser.add_argument('number_of_news', type=int, help='how many news cards to export')
    parser.add_argument('ticker', type=str, help='what ticker you need')
    args = parser.parse_args()
    if not str(args.number_of_news).isalpha:
        raise ValueError("The number of news articles to show entered in command line is not a number")
    input_parameters = {
        "url_output": not args.u,
        "username": args.username,
        "password": args.password,
        "number_of_news": args.number_of_news,
        "ticker": args.ticker
    }
    return input_parameters

