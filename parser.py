import requests
from bs4 import BeautifulSoup
import html
from datetime import datetime


def url_retrieve(url):
    """creates the response from given URL of a news article and returns it"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)  # + search_string + request1 + search_string + request2
    if response.status_code != 200:
        raise Exception("not retrieved ")

    if response.status_code == "200":
        print("URL retrieved GOOD")
    else:
        print(response.status_code)
    return response


def create_soup(response):
    """creates soup object from news page retrieved to response, and writes it to .html file on disk"""
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def function_author(soup):
    """takes the author from the article based on soup object"""
    author = soup.find_all(class_="caas-author-byline-collapse")
    # print(str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">'))
    return str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">')


def function_datetime(soup):
    """takes the date and time from the article based on soup object"""
    date_time = soup.find_all(class_="caas-attr-meta-time")
    date_time_cleaned1 = str(date_time[0]).rstrip('</time>').lstrip('<time class="caas-attr-meta-time" datetime="')
    date_time_cleaned2 = date_time_cleaned1.split('Z">')[0]
    date_time_cleaned = datetime.strptime(date_time_cleaned2, '%Y-%m-%dT%H:%M:%S.%f')
    # print(str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">'))
    return date_time_cleaned


def function_title(soup):

    """takes the title of the news article based on soup aoject"""
    title_raw = soup.find_all(class_="caas-title-wrapper")
    # print(title_raw)
    title = str(title_raw[0]).lstrip('<header class="caas-title-wrapper"><h1 data-test-locator="headline">')\
        .rstrip('</h1></header>')
    title_clean = html.unescape(title)
    # print(title_clean)
    return title_clean


def function_text(soup):
    """takes the news text body from the article based on soup object"""
    text_body_raw = soup.find_all(class_="caas-body")
    text_body = text_body_raw[0].text.strip()
    #print(text_body)
    return text_body


def news_renderer(url):
    """takes the url as an input and renders the author, title, date/time and text"""
    response = url_retrieve(url)
    soup = create_soup(response)
    author = function_author(soup)
    print(author)
    date_time = function_datetime(soup)
    print(date_time)
    title = function_title(soup)
    print(title)
    text_body = function_text(soup)
    print(text_body)


def get_news_data(url):
    """
    Returns news_data from the url (news_page)
    :param url: url of news page
    :return: news_data (dict): {author, date_time, title, text_body}
    """
    response = url_retrieve(url)
    soup = create_soup(response)
    news_data = {
        "author": function_author(soup),
        "date_time": function_datetime(soup),
        "title": function_title(soup),
        "text_body": function_text(soup)
    }
    return news_data


def main():
    return


if __name__ == "__main__":
    main()
