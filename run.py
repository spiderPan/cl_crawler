from bs4 import BeautifulSoup
target = './index.html'

soup = 	BeautifulSoup(target, "html5lib")
print soup.prettify()