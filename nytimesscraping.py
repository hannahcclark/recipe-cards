from bs4 import BeautifulSoup
import urllib2

url = 'http://cooking.nytimes.com/recipes/12817-pork-chops-with-apples-and-cider'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
steps = soup.find_next('ol').find_all('li')
stepstext = []

for step in steps:
	stepstext.append(step.text)

