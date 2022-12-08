import requests
import json
import pandas as pd
import datetime
from logger import logger


class ExtractorApi:
    """Class ExtractorApi() retrieves stock price data from finance.yahoo.com"""
    def __init__(self):
        return

    def url_retrieve(self, url):
        """
        creates the response from given URL of a news article and returns it
        :param url: (str) url for request
        :return: response class
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/102.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)  # + search_string + request1 + search_string + request2
        if response.status_code != 200:
            logger.error("Response from {} is not correct: {}.".format(url, response.status_code))
            raise Exception("not retrieved ")
        logger.debug("Response from {} is obtained correctly.".format(url))
        return response

    def _check_date_input(self, period1, period2):
        """
        Checks if the input dates are in hte correct format
        :param period1: (datetime.datetime) time to start at
        :param period2: (datetime.datetime) time to end at (the current day by default)
        :return: (boolean) True if the test passed, False otherwise
        """
        if not isinstance(period1, datetime.datetime):
            logger.error(("The start date is not a datetime.datetime type: {}".format(period1)))
            return False
        if not isinstance(period2, datetime.datetime):
            logger.error(("The start date is not a datetime.datetime type: {}".format(period2)))
            return False
        if (period2 - period1).total_seconds() < 0:
            logger.error(("The start date is later than the end day: {} and {}".format(period1, period2)))
            return False
        return True

    def get_price_data(self, ticker, period1, period2=datetime.datetime.now()):
        """"
        Gets price data over the specified period with a resolution of 1 day
        :param ticker: (str) e.g. "bmw.de"
        :param period1: (datetime.datetime) time to start at
        :param period2: (datetime.datetime) time to end at (the current day by default)
        :return: DataFrame of prices over time, None if the query was not correct
        """
        if not self._check_date_input(period1, period2):
            return

        period1 = str(int(period1.timestamp()))  # UNIX timestamp representation of the date you wish to start at
        period2 = str(int(period2.timestamp()))

        url = "https://query1.finance.yahoo.com/v8/finance/chart/{}?&interval=1d&period1={}&period2={}" \
            .format(ticker, period1, period2)

        response = self.url_retrieve(url)
        json_content = response.content
        dict_content = json.loads(json_content)

        time_lst = dict_content['chart']['result'][0]['timestamp']
        time_lst = pd.to_datetime(time_lst, unit='s')
        data_lst = dict_content['chart']['result'][0]['indicators']['quote'][0]
        df_table = pd.DataFrame(data=data_lst, index=time_lst)
        logger.debug("The price data is retrieved.")
        return df_table
