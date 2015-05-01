from bs4 import BeautifulSoup
import urllib2
import re

def url_scraper(url):
	return some_source_scraper(url)

def some_source_scraper(url):
	#get source
	source = get_source_site(url)
	if source == 'cooking.nytimes.com':
		return nyt_scraper(url)
	return {error: 'bad url'}

def get_source_site(url):
	if not url[0] == 'h':
		url = "http://" + url
	result = re.search('://(.*)/recipes', url)
	return result.group(1)

def nyt_scraper(url):
	recipe = {'url': url}
	recipe['source'] = 'cooking.nytimes.com'
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	
	#get title 
	recipe['name'] = soup.title.text

	#get author
	author = soup.find_all('a', class_="author personality")
	recipe['author'] = author[0].text.replace('\n','')

	#get ingredients
	ingredients = soup.find('ul', class_="recipe-ingredients").find_all('li')
	ingredtext = []
	for ingred in ingredients:
		curr_ingred = ingred.text.replace('\n','')
		ingredtext.append(curr_ingred)
	recipe['ingredients'] = ingredtext

	#get directions
	steps = soup.find('ol', class_="recipe-steps").findChildren()
	stepstext = []
	for step in steps:
	 	curr_step = step.text.replace('\n',' ')
	 	stepstext.append(curr_step)
	recipe['directions'] = stepstext

	return recipe
