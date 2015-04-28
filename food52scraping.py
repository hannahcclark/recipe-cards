from bs4 import BeautifulSoup
import urllib2

url = 'http://food52.com/recipes/30119-homemade-teriyaki-sauce'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
ingredients = soup.find_next('ul').find_all('li')
steps = soup.find_next('ol').find_all('li')
stepstext = []
ingredtext = []
title = soup.title.string

for step in steps:
	stepstext.append(step.text)

for ingred in ingredients:
	ingredtext.append(ingred.text)

toReturn = {'title': title, 'url': url, 'steps': stepstext, 'ingredients': ingredtext}