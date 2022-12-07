from selenium import webdriver
from bs4 import BeautifulSoup
import time


class ParserSearchPage:
    """class ParserSearchPage parses result of search page with request of ticker at finance.yahoo.com"""
    def __init__(self, ticker):
        """
        Initializes the class Parser_search_page()
        :param ticker: (str) ticker of company, e.g. "BMW.DE"
        """
        self.ticker = ticker
        self._driver = webdriver.Chrome()
        self._html_page = self._get_html_page()
        return

    def _get_url(self):
        """
        Gets url from query (ticker of company (str). e.g. "BMW.DE").
        :params: none, only self
        :return: full url of the search with ticker
        """
        return "https://finance.yahoo.com/quote/" + self.ticker + "/news?p=" + self.ticker

    def _scroll_to_bottom(self):
        """
             Scrolls the web page to its bottom, overcoming the dynamic pagination.
             no params on input, only self
             no return, it only scrolls.
             """
        old_position = 0
        new_position = None
        while new_position != old_position:
            # Get old scroll position
            old_position = self._driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
            # Sleep and Scroll
            time.sleep(1)
            self._driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
            # Get new position
            new_position = self._driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        return

    def _get_html_page(self):
        """
        Returns content of html page (search page for the ticker of company (str). e.g. "BMW.DE")
        :params: no, only self
        :return: text (str), content in tag <html></html>
        """
        url_root_yahoo = self._get_url()
        self._driver.get(url_root_yahoo)
        self._scroll_to_bottom()
        text = self._driver.page_source
        self._driver.close()
        return text

    def _get_url_from_tag_h3(self, tag_h3):
        """
        Gets url from html tag h3
        :param tag_h3:  h3 tag
        :return: full url to the news page
        """
        URL_PREFIX = "https://finance.yahoo.com"
        url_to_news = URL_PREFIX + tag_h3.find("a").get("href")
        return url_to_news

    def get_url_lst(self, tag_h3_lst):
        """
        Returns list of urls in for of python list
        :param tag_h3_lst: list of h3 tags from the web page
        :return: list of urls
        """
        url_lst = []
        for tag_h3 in tag_h3_lst:
            url = self._get_url_from_tag_h3(tag_h3)
            url_lst.append(url)
        return url_lst

    def _get_tag_h3_lst_from_html_page(self):
        """
        Returns list h3 tags from html page, the list contains the h3 tags with url inside.
        :param: only self
        :return: list of tags h3 with urls inside
        """
        # Parse HTML content of the page (URL)
        soup = BeautifulSoup(self._html_page, "html.parser")
        # Find all tags "h3" with id="Mb(5px)"
        list_of_tags = soup.find_all("h3", "Mb(5px)")
        return list_of_tags

    def get_url_lst_from_html_page(self):
        """
        Accumulates the functions to get final url lists, calls functions to get list of h3 tags with
        urls first, and then calls the function to create the list of urls.
        :param: only self
        :return: final list of urls
        """
        # Get list tags <h3 id='Mb(5px)'></h3>
        tag_h3_lst = self._get_tag_h3_lst_from_html_page()
        # Get list of url to news
        url_lst = self.get_url_lst(tag_h3_lst)
        return url_lst
