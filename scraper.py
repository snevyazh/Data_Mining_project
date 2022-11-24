import parser
from parser_search_page import *


class Scraper:
    def __init__(self, ticker, max_cards):
        self.ticker = ticker
        self.max_cards = max_cards
        self.news_data_lst = []
        self.scraper_by_ticker_from_yahoo()
        pass

    def scraper_by_ticker_from_yahoo(self):
        """
        Scrapes news from finance.yahoo.com for company
        :param ticker: (str) ticker of company. e.g. "BMW.DE"
        :param max_cards: (int) maximum number of cards
        :return: prints the scraped data news. False if news were not found
        TODO returns list: in format
        """
        page = ParserSearchPage(self.ticker)
        # html_page = lister.get_html_page(self.ticker) # was working)
        #url_lst = url_from_html_page.get_url_lst_from_html_page(html_page)
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
        # print('news data list from scrapper', self.news_data_lst)
        pass

    # def print_dictionary_list(dict_list):
    #     """
    #     Prints list of dictionaries to the screen
    #     :param dict_list: e.g. [{"name": 'Alice', "age": 20}, {"name": 'Bob', "age": 21}]
    #     UPD !!!! not used in final implementation
    #     """
    #     header = dict_list[0].keys()
    #     rows = [x.values() for x in dict_list]
    #     print(tabulate.tabulate(rows, header))
    #     pass

