import url_from_html_page
import lister
import parser
import tabulate


class Scraper:
    def __init__(self, ticker, max_cards):
        self.ticker = ticker
        self.max_cards = max_cards
        self.news_data_lst = []
        pass

    # def __getitem__(self, key):
    #     return self.news_data_lst[key]

    def scraper_by_ticker_from_yahoo(self):
        """
        Scrapes news from finance.yahoo.com for company
        :param ticker: (str) ticker of company. e.g. "BMW.DE"
        :param max_cards: (int) maximum number of cards
        :return: prints the scraped data news. False if news were not found
        TODO returns list: in format
        """
        html_page = lister.get_html_page(self.ticker)
        url_lst = url_from_html_page.get_url_lst_from_html_page(html_page)
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

    def print_dictionary_list(dict_list):
        """
        Prints list of dictionaries to the screen
        :param dict_list: e.g. [{"name": 'Alice', "age": 20}, {"name": 'Bob', "age": 21}]
        UPD !!!! not used in final implementation
        """
        header = dict_list[0].keys()
        rows = [x.values() for x in dict_list]
        print(tabulate.tabulate(rows, header))
        pass

# def main():
#     """Calls Scraper(query) and prints the result"""
#     # ticker_name_lst = ['ORCL','BMW.DE', 'CRM', 'MSFT', 'ORCX', 'MNDY', 'META', 'AAPL', 'TSLA', 'GTR', 'HJY']
#     # ticker_name_lst = ['ORCX', 'ORCL']
#     ticker_name_lst = input("Enter tickers in a row ").split()
#     max_cards = int(input("Enter maximal news cards number "))
#     for ticker_name in ticker_name_lst:
#         news_data = scraper_by_ticker_from_yahoo(ticker_name, max_cards)
#         if not news_data:
#             print(f"News were not found for {ticker_name}. Check ticker name.")
#             continue
#         print(f"Searching news for {ticker_name}...")
#         print_dictionary_list(news_data)
#     return
#
#
# if __name__ == "__main__":
#     main()
