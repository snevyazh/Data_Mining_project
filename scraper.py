import url_from_html_page
import lister
import parser
import tabulate


def print_dictionary_list(dict_list):
    """
    Prints list of dictionaries to the screen
    :param dict_list: e.g. [{"name": 'Alice', "age": 20}, {"name": 'Bob', "age": 21}]
    """
    header = dict_list[0].keys()
    rows = [x.values() for x in dict_list]
    print(tabulate.tabulate(rows, header))
    return


def scraper(query):
    """
    Scrapes news from finance.yahoo.com for company
    :param query: (str) ticker of company. e.g. "BMW.DE"
    :return: prints the scraped data news
    """
    html_page = lister.get_html_page(query)
    url_lst = url_from_html_page.get_url_lst_from_html_page(html_page)

    i = 1  # i for test
    imax = 3  # prints imax results
    news_data_lst = []
    for url in url_lst:
        print(f"process page #{i} out of {imax}")
        news_data_lst.append(parser.get_news_data(url))
        if i > imax - 1:
            break
        i += 1
    return news_data_lst


def main():
    """Calls Scraper(query) and prints the result"""
    news_data = scraper("BMW.DE")
    print_dictionary_list(news_data)
    return


if __name__ == "__main__":
    main()
