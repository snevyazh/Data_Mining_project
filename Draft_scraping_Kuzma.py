import requests
from bs4 import BeautifulSoup
import csv
import os
import tabulate
from time import sleep
from random import randint


def get_article_card(card):
    """Gets parameter of article from given card of the news in HTML tags"""
    headline = card.find("h4", "s-title").text    # Get title of article
    source = card.find("span", "s-source").text  # Get source of article
    time_posted = card.find("span", "s-time").text.replace('·', '').strip()  # Get publication time of article
    description = card.find("p", "s-desc").text.strip()  # Get description of the article
    link_to_article = card.find("a").get("href")  # Get link to article
    article_card = {"headline": headline,
                    "source": source,
                    "time_posted": time_posted,
                    "description": description,
                    "link": link_to_article}
    return article_card


def get_list_of_article_cards_from_page(cards):
    """Get list of article cards from a page"""
    article_card_lst = []
    for card in cards:  # Maybe to add filtering out duplicates by links
        article_card = get_article_card(card)
        article_card_lst.append(article_card)
    return article_card_lst


def get_news_yahoo_from_page(url):
    """
    Gets list of article cards from the specified URL of yahoo news
    :param url: url format for query "bmw": https://news.search.yahoo.com/search?p=bmw"
    :return: articles_cards (list), URL_next_page (URL to the next page with the same query)
    """
    # Create a response to the URL
    page = requests.get(url)
    # Parse HTML content of the page (URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # Find all tags "div" with id="NewsArticle"
    cards = soup.find_all("div", "NewsArticle")  # Finds cards of articles on the page (10 per page)
    # Get list of article cards from a page
    articles_card_list = get_list_of_article_cards_from_page(cards)
    # Find URL to the next page
    url_next_page = soup.find('a', 'next').get('href')
    return articles_card_list, url_next_page


def get_news_yahoo(query, number_of_pages):
    """
    Prints the article cards from the yahoo news for the specified query to the screen
    :param query: name of company (string)
    :param number_of_pages: (int)
    :return: List of article cards
    """
    URL_TEMPLATE = "https://news.search.yahoo.com/search?p={}"
    url = URL_TEMPLATE.format(query)
    articles_card_list = []
    for page_number in range(1, number_of_pages + 1):
        print(f'page {page_number} in processing...')
        sleep(randint(15, 30))  # wait for 15-30 seconds before the next response to yahoo
        articles_card_list_from_page, url = get_news_yahoo_from_page(url)
        articles_card_list += articles_card_list_from_page
    return articles_card_list


def dictionary_list_to_csv(dict_list, filename):
    """
    Saves list of dictionaries to csv file
    :param dict_list: e.g. [{"name": 'Alice', "age": 20}, {"name": 'Bob', "age": 21}]
    :param filename: path of output file
    """
    keys = dict_list[0].keys()
    # Write header if file does not exist
    if not os.path.isfile(filename):
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
    # Add new rows to the file
    with open(filename, 'a', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writerows(dict_list)
    return


def print_dictionary_list(dict_list):
    """
    Prints list of dictionaries to the screen
    :param dict_list: e.g. [{"name": 'Alice', "age": 20}, {"name": 'Bob', "age": 21}]
    """
    header = dict_list[0].keys()
    rows = [x.values() for x in dict_list]
    print(tabulate.tabulate(rows, header))
    return


article_cards_list = get_news_yahoo("bmw", 2)
print_dictionary_list(article_cards_list)
