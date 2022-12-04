import requests
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt


class ExtractorApi():
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

    def get_price_data(self, ticker = "bmw.de", interval="1d", range="30d",
                       period1=datetime.datetime(2022, 1, 1),
                       period2=datetime.datetime(2022, 1, 7)):
        """
        Gets price data
        :param ticker: (str) e.g. "bmw.de"
        :param interval: (str) # 1m 2m 5m 15m 30m 60m 90m 1h 1d 5d 1wk 1mo 3mo
        :param range: (str) e.g. "30d". Can be "max" or "previous"
        :param period1: (datetime.datetime) time to start at (can be overwritten by 'range')
        :param period2: (datetime.datetime) time to end at
        :return: DataFrame of prices over time
        """

        period1 = str(int(period1.timestamp()))  # UNIX timestamp representation of the date you wish to start at
        period2 = str(int(period2.timestamp()))

        url = "https://query1.finance.yahoo.com/v8/finance/chart/{}?&interval={}&range={}&period1={}&period2={}" \
            .format(ticker, interval, range, period1, period2)

        # url = "https://query1.finance.yahoo.com/v8/finance/chart/{}?&interval={}&range={}" \
        #     .format(ticker, interval, range)

        response = self.url_retrieve(url)
        json_content = response.content
        dict_content = json.loads(json_content)

        time_lst = dict_content['chart']['result'][0]['timestamp']
        time_lst = pd.to_datetime(time_lst, unit='s')
        data_lst = dict_content['chart']['result'][0]['indicators']['quote'][0]
        df_table = pd.DataFrame(data=data_lst, index=time_lst)
        return df_table


ticker = "bmw.de"
interval = "1d"
range = ""

api_obj = ExtractorApi()
df_table = api_obj.get_price_data(ticker=ticker,
                                  interval=interval,
                                  range=range,
                                  period1=datetime.datetime(2022, 1, 1),
                                  period2=datetime.datetime(2022, 1, 7))
