from selenium import webdriver
import time

# url_root_yahoo = 'https://finance.yahoo.com/news/'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
#
# driver = webdriver.Chrome()
# driver.get(url_root_yahoo)



def scroll_to_bottom(driver):
    old_position = 0
    new_position = None
    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))


def get_url(query):
    """
    Gets url from query.
    :param query: ticker of company (str). e.g. "BMW.DE"
    :return: url (str)
    """
    return "https://finance.yahoo.com/quote/" + query + "/news?p=" + query


def get_html_page(query):
    """
    :param query: ticker of company (str). e.g. "BMW.DE"
    :return: text (str), content in tag <html></html>
    """
    url_root_yahoo = get_url(query)

    browser = driver = webdriver.Chrome()
    browser.get(url_root_yahoo)
    scroll_to_bottom(driver)
    text = driver.page_source
    browser.close()
    return text


def main():
    return


if __name__ == "__main__":
    main()

