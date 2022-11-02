import requests
from bs4 import BeautifulSoup

URL = 'https://finance.yahoo.com/quote/'
request1 = '?p='
request2 = '&.tsrc=fin-srch'
search_string = 'AMD'  # input('enter search ticker ')
response = requests.get(URL + search_string + request1 + search_string + request2)
soup = BeautifulSoup(response.content, "html.parser")
print(response)
print(response.headers)
# print(response.text)
with open('/Users/stanislavnevyazhsky/My Drive/Data Science/Python/data mining/output1.html', 'w') as output:
    output.write(soup.prettify())


