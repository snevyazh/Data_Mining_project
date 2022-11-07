from bs4 import BeautifulSoup


def get_url_from_tag_h3(tag_h3):
    """Gets url to news from tag <h3 id='Mb(5px)'>"""
    URL_PREFIX = "https://finance.yahoo.com"
    url_to_news = URL_PREFIX + tag_h3.find("a").get("href")
    return url_to_news


def get_url_lst(tag_h3_lst):
    """Get list of url to news from the tag <h3 id='Mb(5px)'>"""
    url_lst = []
    for tag_h3 in tag_h3_lst:
        url = get_url_from_tag_h3(tag_h3)
        url_lst.append(url)
    return url_lst


def get_tag_h3_lst_from_html_page(html_page):
    """
    Gets list of tags <h3 id='Mb(5px)'> from the html page
    :param html_page: page in html tags. Content between <html></html>
    :return: list_of_tags (list): each tag contains the link to news
    """
    # Parse HTML content of the page (URL)
    soup = BeautifulSoup(html_page, "html.parser")
    # Find all tags "h3" with id="Mb(5px)"
    list_of_tags = soup.find_all("h3", "Mb(5px)")
    return list_of_tags


def get_url_lst_from_html_page(html_page):
    """
    Gets list of url to news from finance yahoo
    """
    # Get list tags <h3 id='Mb(5px)'></h3>
    tag_h3_lst = get_tag_h3_lst_from_html_page(html_page)
    # Get list of url to news
    url_lst = get_url_lst(tag_h3_lst)
    return url_lst


def main():
    # url_lst = get_url_lst_from_html_page(html_page)
    return


if __name__ == "__main__":
    main()
