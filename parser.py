import requests
from bs4 import BeautifulSoup
import html
from datetime import datetime


class Parser:
    """class Parser creates an object that is created with URL, processes all url-related data and returns
    the dictionary for news"""

    def __init__(self, url):
        self.url = url
        self.response = self.__url_retrieve(self.url)
        self.soup = self.__create_soup(self.response)
        self.author = self.__function_author(self.soup)
        self.date_time = self.__function_datetime(self.soup)
        self.title = self.__function_title(self.soup)
        self.text = self.__function_text(self.soup)

    def __url_retrieve(self, url):
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

    def __create_soup(self, response):
        """creates soup object from news page retrieved to response, and writes it to .html file on disk"""
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def __function_author(self, soup):
        """takes the author from the article based on soup object"""
        author = soup.find_all(class_="caas-author-byline-collapse")
        # print(str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">'))
        return str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">')
        # 0 is an index for web scrapping of author, will never change and is used only locally


    def __function_datetime(self, soup):
        """takes the date and time from the article based on soup object"""
        date_time = soup.find_all(class_="caas-attr-meta-time")
        date_time_cleaned1 = str(date_time[0]).rstrip('</time>').lstrip('<time class="caas-attr-meta-time" datetime="')
        # 0 is an index for web scrapping, will never change and is used only locally
        date_time_cleaned2 = date_time_cleaned1.split('Z">')[0]
        date_time_cleaned = datetime.strptime(date_time_cleaned2, '%Y-%m-%dT%H:%M:%S.%f')
        # print(str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">'))
        return date_time_cleaned

    def __function_title(self, soup):
        """takes the title of the news article based on soup aoject"""
        title_raw = soup.find_all(class_="caas-title-wrapper")
        # print(title_raw)
        title = str(title_raw[0]).lstrip('<header class="caas-title-wrapper"><h1 data-test-locator="headline">') \
            .rstrip('</h1></header>')
        # 0 is an index for web scrapping, will never change and is used only locally
        title_clean = html.unescape(title)
        # print(title_clean)
        return title_clean

    def __function_text(self, soup):
        """takes the news text body from the article based on soup object"""
        text_body_raw = soup.find_all(class_="caas-body")
        text_body = text_body_raw[0].text.strip()
        # 0 is an index for web scrapping, will never change and is used only locally
        return text_body

    def get_news_data(self, url):
        """
        Returns news_data from the url (news_page)
        :param url: url of news page
        :return: news_data (dict): {author, date_time, title, text_body}
        """
        response = self.__url_retrieve(url)
        soup = self.__create_soup(response)
        news_data = {
            "author": self.__function_author(soup),
            "date_time": self.__function_datetime(soup),
            "title": self.__function_title(soup),
            "text_body": self.__function_text(soup), "url": url
        }
        return news_data
