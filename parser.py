import requests

URL = 'https://www.glassdoor.com/Search/results.htm'
request = '?keyword='
search_string = 'engineer' # input('enter search word ')
response = requests.get(URL + request + search_string)
print(response)


print(response.headers)
print(response.text)
