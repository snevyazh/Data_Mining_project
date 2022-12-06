import parser
from parser_search_page import *


class Scraper:
    def __init__(self, ticker, max_cards):
        """Defines the class Scrapper
        :param ticker: (str) ticker of company. e.g. "BMW.DE"
        :param max_cards: (int) maximum number of cards"""
        self.ticker = ticker
        self.max_cards = max_cards
        self.news_data_lst = []
        self.scraper_by_ticker_from_yahoo()
        pass

    def scraper_by_ticker_from_yahoo(self):
        """
        Scrapes news from finance.yahoo.com for company
        :param: none, uses self only
        :return: prints the scraped data news. False if news were not found
        TODO returns list: in format
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


