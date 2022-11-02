import requests
from bs4 import BeautifulSoup

URL = "https://www.glassdoor.com/Job/israel-data-scientist-jobs-SRCH_IL.0,6_IN119_KO7,21.htm"
page = requests.get(URL)

#print(page.text)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="p-std")


# # Narrowing down the space to the article in the page
# #(since there are many other irrelevant elements in the page)
# article = soup.find(class_="article-wrapper grid row")
#
# <div id="CompanyContainer" class="p-std" data-brandviews="MODULE:n=jobs-company:eid=383492:jlid=1008147162114" data-triggered-brandview=""><div id="EmpBasicInfo" data-emp-id="100431"><div><h2 class="mb-std css-ukqtc8 e9b8rvy0">Company Overview</h2><div class="d-flex flex-wrap"><div class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"><span class="css-1taruhi e1pvx6aw1">Size</span><span class="css-i9gxme e1pvx6aw2">201 to 500 Employees</span></div><div class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"><span class="css-1taruhi e1pvx6aw1">Founded</span><span class="css-i9gxme e1pvx6aw2">1999</span></div><div class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"><span class="css-1taruhi e1pvx6aw1">Type</span><span class="css-i9gxme e1pvx6aw2">Company - Public</span></div><div class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"><span class="css-1taruhi e1pvx6aw1">Industry</span><span class="css-i9gxme e1pvx6aw2">HR Consulting</span></div><div class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"><span class="css-1taruhi e1pvx6aw1">Sector</span><span class="css-i9gxme e1pvx6aw2">Human Resources &amp; Staffing</span></div><div class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"><span class="css-1taruhi e1pvx6aw1">Revenue</span><span class="css-i9gxme e1pvx6aw2">$25 to $100 million (USD)</span></div></div></div><div><div class="m-0 pt-sm pb"><a href="http://www.ambitiongrouplimited.com" target="_blank" rel="nofollow noopener noreferrer">Visit AMBITION Website</a></div></div></div></div>