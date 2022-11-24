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
        :return: url (str)
        """
        return "https://finance.yahoo.com/quote/" + self.ticker + "/news?p=" + self.ticker

    def _scroll_to_bottom(self):
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
        :return: text (str), content in tag <html></html>
        """
        url_root_yahoo = self._get_url()

        self._driver.get(url_root_yahoo)
        self._scroll_to_bottom()
        text = self._driver.page_source
        self._driver.close()
        return text

    def _get_url_from_tag_h3(self, tag_h3):
        """Gets url to news from tag <h3 id='Mb(5px)'>"""
        URL_PREFIX = "https://finance.yahoo.com"
        url_to_news = URL_PREFIX + tag_h3.find("a").get("href")
        return url_to_news

    def get_url_lst(self, tag_h3_lst):
        """Get list of url to news from the tag <h3 id='Mb(5px)'>"""
        url_lst = []
        for tag_h3 in tag_h3_lst:
            url = self._get_url_from_tag_h3(tag_h3)
            url_lst.append(url)
        return url_lst

    def _get_tag_h3_lst_from_html_page(self):
        """
        Gets list of tags <h3 id='Mb(5px)'> from the html page (Content between <html></html>)
        :return: list_of_tags (list): each tag contains the link to news
        """
        # Parse HTML content of the page (URL)
        soup = BeautifulSoup(self._html_page, "html.parser")
        # Find all tags "h3" with id="Mb(5px)"
        list_of_tags = soup.find_all("h3", "Mb(5px)")
        return list_of_tags

    def get_url_lst_from_html_page(self):
        """
        Gets list of url to news from finance yahoo
        """
        # Get list tags <h3 id='Mb(5px)'></h3>
        tag_h3_lst = self._get_tag_h3_lst_from_html_page()
        # Get list of url to news
        url_lst = self.get_url_lst(tag_h3_lst)
        return url_lst
