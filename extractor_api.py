import requests
import json
import pandas as pd
import datetime


class ExtractorApi:
    def __init__(self):
        return

    def url_retrieve(self, url):
        """creates the response from given URL of a news article and returns it"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/102.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)  # + search_string + request1 + search_string + request2
        if response.status_code != 200:
            raise Exception("not retrieved ")

        # if response.status_code == "200":
        #     print("URL retrieved GOOD")
        # else:
        #     print(response.status_code)
        return response

    def get_price_data(self, ticker, period1, period2=datetime.datetime.now()):
        """"
        Gets price data over the specified period with a resolution of 1 day
        :param ticker: (str) e.g. "bmw.de"
        :param period1: (datetime.datetime) time to start at (can be overwritten by 'range')
        :param period2: (datetime.datetime) time to end at (the current day by default)
        :return: DataFrame of prices over time, None if the query was not correct
        """
        if not isinstance(period1, datetime.datetime):
            print("The start date is not a datetime.datetime type")
            return

        if not isinstance(period2, datetime.datetime):
            print("The end date is not a datetime.datetime type")
            return

        if (period2 - period1).total_seconds() < 0:
            print("The start date is later than the end day!")
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
        return df_table


# ticker = "bmw.de"
#
# api_obj = ExtractorApi()
# df_table = api_obj.get_price_data(ticker=ticker,
#                                   period1=datetime.datetime(2022, 1, 1),
#                                   period2=datetime.datetime(2022, 1, 7))