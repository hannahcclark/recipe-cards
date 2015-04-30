from bs4 import BeautifulSoup
import urllib2
import re

def url_scraper(url):
	return some_source_scraper(url)

def some_source_scraper(url):
	recipe = {'url': url}
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	
	#get source
	recipe['source'] = get_source_site(url)

	#get title 
	recipe['name'] = soup.title.text

	#get author
	author = soup.find_all('a', class_="author personality")
	recipe['author'] = author[0].text.replace('\n','')

	#get servings

	#get time

	#get ingredients
	ingredients = soup.find_all('ul', class_="recipe-ingredients")
	ingredtext = []
	for ingred in ingredients:
		curr_ingred = ingred.text.replace('\n','')
		ingredtext.append(curr_ingred)
	recipe['ingredients'] = ingredtext

	#get directions
	steps = soup.find_all('ol', class_="recipe-steps")
	stepstext = []
	for step in steps:
		curr_step = step.text.replace('\n',' ')
		stepstext.append(curr_step)
	recipe['directions'] = stepstext

	return recipe

def get_source_site(url):
	result = re.search('://(.*)/recipes', url)
	return result.group(1)



