from bs4 import BeautifulSoup
import urllib2

def url_scraper(url):
	scraper_fn = some_source_scraper
	url = 'http://food52.com/recipes/30119-homemade-teriyaki-sauce'
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	#Given url as a string, give back the result of calling the correct source function
	#either throw exception or give back a dictionary indicating an error
	#if source doesn't have a scraper
	return scraper_fn(url)

def some_source_scraper(url):
	recipe = {'url': url, 'source':'some_source.com'}#replace with correct source
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
	recipe['ingredients'] = ingredtext
	recipe['steps'] = stepstext
	recipe['title'] = soup.title.text
	#do scraping
	#insert name of recipe under key 'name'
	#insert array of ingredients under 'ingredients'
	#insert array of instructions under key 'directions'
	return recipe