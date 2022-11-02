import requests
from bs4 import BeautifulSoup

URL = 'https://www.glassdoor.com/Search/results.htm'
request = '?keyword='
search_string = 'engineer'  # input('enter search word ')
response = requests.get(URL + request + search_string)

print(response)
print(response.headers)
# print(response.text)
with open('/Users/stanislavnevyazhsky/My Drive/Data Science/Python/data mining/output.html', 'w') as output:
    output.write(response.text)


