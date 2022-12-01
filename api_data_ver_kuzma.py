import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

class api_data():
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

# Price history
url = "https://query1.finance.yahoo.com/v8/finance/chart/bmw.de"

api_obj = api_data()
response = api_obj.url_retrieve(url)
json_content = response.content
dict_content = json.loads(json_content)

time_lst = dict_content['chart']['result'][0]['timestamp']
time_lst = pd.to_datetime(time_lst, unit='s')
data_lst = dict_content['chart']['result'][0]['indicators']['quote'][0]
df_table = pd.DataFrame(data=data_lst, index=time_lst)
