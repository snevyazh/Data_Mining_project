import parser
from parser_search_page import *
from extractor_api import *


class Scraper:
    def __init__(self, ticker, max_cards, api=False, date_start=None, date_end=None):
        """
        Defines the class Scrapper
        :param ticker: (str) ticker of company. e.g. "BMW.DE"
        :param max_cards: (int) maximum number of cards
        :param api: (boolean) retrieve the stock prices through API if True
        """
        self.ticker = ticker
        self.max_cards = max_cards
        self.news_data_lst = []
        self.scraper_by_ticker_from_yahoo()

        if api:
            self.price_table = self.get_price_table(date_start, date_end)
        pass

    def get_price_table(self, date_start, date_end):
        """
        Gets price data over the specified period with a resolution of 1 day
        :param date_start: (datetime.datetime) time to start at (can be overwritten by 'range')
        :param date_end: (datetime.datetime) time to end at (the current day by default)
        :return: DataFrame of prices over time, None if the query was not correct
        """
        if (date_start is None) or (date_end is None):
            print("The stock prices were not retrieved! The dates were not provided.")
            return
        else:
            price_table = ExtractorApi().get_price_data(self.ticker, date_start, date_end)
            return price_table

    def scraper_by_ticker_from_yahoo(self):
        """
        Scrapes news from finance.yahoo.com for company
        :param: none, uses self only
        :return: prints the scraped data news. False if news were not found
        """
        page = ParserSearchPage(self.ticker)
        url_lst = page.get_url_lst_from_html_page()
        if not url_lst:  # news were not found
            return False

        i = 1  # news number
        for url in url_lst:
            print(f"process page #{i} out of {self.max_cards}")
            parser_for_news_card = parser.Parser(url)
            self.news_data_lst.append(parser_for_news_card.get_news_data(url))
            if i > self.max_cards - 1:
                break
            i += 1
        pass
