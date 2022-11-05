import requests
from bs4 import BeautifulSoup

def get_article_card(card):
    """Gets parameter of article from given card of the news in HTML tags"""
    headline = card.find("h4", "s-title").text    # Get title of article
    source = card.find("span","s-source").text  # Get source of article
    time_posted = card.find("span","s-time").text.replace('·','').strip() # Get publication time of article
    description = card.find("p","s-desc").text.strip() # Get description of the article
    link_to_article = card.find("a").get("href") # Get link to article
    article_card = {"headline": headline,
                    "source": source,
                    "time_posted": time_posted,
                    "description": description,
                    "link": link_to_article}
    return article_card

#URL = "https://finance.yahoo.com/news/"
URL_template = "https://news.search.yahoo.com/search?p={}"
URL = URL_template.format('bmw')

# Create a response to the URL
page = requests.get(URL)

# Parse HTML content of the page (URL)
soup = BeautifulSoup(page.content, "html.parser")

# Find all tags "div" with id="NewsArticle"
cards = soup.find_all("div","NewsArticle")


