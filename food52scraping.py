from bs4 import BeautifulSoup
import urllib2

url = 'http://food52.com/recipes/30119-homemade-teriyaki-sauce'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
steps = soup.find_next('ol').find_all('li')
stepstext = []

for step in steps:
	stepstext.append(step.text)