

import requests
from bs4 import BeautifulSoup


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
    with open('/Users/stanislavnevyazhsky/My Drive/Data Science/Python/data mining/output1.html', 'w') as output:
        output.write(soup.prettify())
    # print(soup.title)
    return soup


def function_author(soup):
    """takes the author from the article based on soup object"""
    author = soup.find_all(class_="caas-author-byline-collapse")
    # print(str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">'))
    return str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">')


def function_datetime(soup):
    """takes the date and time from the article based on soup object"""
    from datetime import datetime
    date_time = soup.find_all(class_="caas-attr-meta-time")
    date_time_cleaned1 = str(date_time[0]).rstrip('</time>').lstrip('<time class="caas-attr-meta-time" datetime="')
    date_time_cleaned2 = date_time_cleaned1.split('Z">')[0]
    date_time_cleaned = datetime.strptime(date_time_cleaned2, '%Y-%m-%dT%H:%M:%S.%f')
    # print(str(author[0]).rstrip('</span>').lstrip('<span class="caas-author-byline-collapse">'))
    return date_time_cleaned


def function_title(soup):
    import html
    """takes the title of the news article based on soup aoject"""
    title_raw = soup.find_all(class_="caas-title-wrapper")
    # print(title_raw)
    title = str(title_raw[0]).lstrip('<header class="caas-title-wrapper"><h1 data-test-locator="headline">')\
        .rstrip('</h1></header>')
    title_clean = html.unescape(title)
    # print(title_clean)
    return title_clean


def main():
    url = 'https://finance.yahoo.com/news/top-analyst-reports-bristol-myers-164504521.html'
    response = url_retrieve(url)

    soup = create_soup(response)
    author = function_author(soup)
    print(author)
    date_time = function_datetime(soup)
    print(date_time)
    title = function_title(soup)
    print(title)


if __name__ == "__main__":
    main()
