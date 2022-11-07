This is a code to scrap the news from finance.yahoo.com

1) it first opens the page and scraps all the news articles
2) the finance.yahoo.com has no paginator, but loads new content once the 
user is reaching the edge. So, the scrapper emulates this behaviour with
Selenium package
3) the news are filtered by &&&&&
3) for every news article we gets author, date and news text
4) 