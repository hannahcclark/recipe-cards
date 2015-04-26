from bs4 import BeautifulSoup
import urllib2

def url_scraper(url):
	scraper_fn = some_source_scraper
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
	#food 52 itemprop="author"
	#food network itemprop="name"
	ingredients = soup.find_next('ul').find_all('li') #might not work - there are a lot of lists on any given page, need to know the class
	steps = soup.find_next('ol').find_all('li')
	stepstext = []
	ingredtext = []
	title = soup.title.string

	for step in steps:
		stepstext.append(step.text)

	for ingred in ingredients:
		ingredtext.append(ingred.text)
	recipe['ingredients'] = ingredtext
	recipe['directions'] = stepstext
	recipe['name'] = soup.title.text
	return recipe