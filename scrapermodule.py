from bs4 import BeautifulSoup
import urllib2
import re

def url_scraper(url):
	#get source
	if len(url) == 0:
		return {error: 'bad url'}
	if not url[0] == 'h':
		url = "http://" + url
	source = get_source_site(url)
	if source == 'cooking.nytimes.com':
		return nyt_scraper(url)
	elif source == 'www.epicurious.com':
		return epi_scraper(url)
	elif source == 'food52.com':
		return f52_scraper(url)
	if source == 'allrecipes.com':
		return all_scraper(url)
	return {error: 'bad url'}

def get_source_site(url):
	result = re.search('://(.*)/(recipe|Recipe)', url)
	return result.group(1)

def nyt_scraper(url):
	recipe = {'url': url}
	recipe['source'] = 'cooking.nytimes.com'
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	
	#get title 
	title = soup.find('h1', class_="recipe-title title name")
	recipe['name'] = title.text.replace('\n    ', '')

	#get author
	author = soup.find_all('a', class_="author personality")
	recipe['author'] = author[0].text.replace('\n','')

	#get ingredients
	ingredients = soup.find_all('li', {"itemprop":"ingredients"})
	ingredtext = []
	for ingred in ingredients:
		curr_ingred = ingred.text.replace('\n',' ')
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

def epi_scraper(url):
	recipe = {'url': url}
	recipe['source'] = 'epicurious.com'
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	
	#get title 
	recipe['name'] = soup.find('h1', {"itemprop":"name"}).text

	#get author
	author = soup.find_all('p', class_="author source")
	recipe['author'] = author[0].text.replace('\n','')

	#get ingredients
	ingredients = soup.find_all('li', {"itemprop":"ingredients"})
	ingredtext = []
	for ingred in ingredients:
		curr_ingred = ingred.text.replace('\n','')
		ingredtext.append(curr_ingred)
	recipe['ingredients'] = ingredtext

	#get directions
	steps = soup.find('div', class_="instructions").findChildren()
	stepstext = []
	for step in steps:
	 	curr_step = step.text.replace('\n',' ')
	 	curr_step = curr_step.replace('  ', '')
	 	stepstext.append(curr_step)
	recipe['directions'] = stepstext

	return recipe

def f52_scraper(url):
	recipe = {'url': url}
	recipe['source'] = 'food52.com'
	req = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0'}) 
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page)
	
	#get title 
	recipe['name'] = soup.find('h1', {"itemprop":"name"}).text

	#get author
	author = soup.find_all('a', {"itemprop":"author"})
	recipe['author'] = author[0].text.replace('\n','')

	#get ingredients
	ingredients = soup.find_all('li', {"itemprop":"ingredients"})
	ingredtext = []
	for ingred in ingredients:
		curr_ingred = ingred.text.replace('\n',' ')
		ingredtext.append(curr_ingred)
	recipe['ingredients'] = ingredtext

	#get directions
	steps = soup.find_all('li', {"itemprop":"recipeInstructions"})
	stepstext = []
	for step in steps:
	 	curr_step = step.text.replace('\n',' ')
	 	curr_step = curr_step.replace('  ', '')
	 	stepstext.append(curr_step)
	recipe['directions'] = stepstext

	return recipe

def all_scraper(url):
	recipe = {'url': url}
	recipe['source'] = 'allrecipes.com'
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	
	#get title 
	recipe['name'] = soup.find('h1', {"itemprop":"name"}).text

	#get author
	author = soup.find_all('span', class_="name")
	recipe['author'] = author[0].text.replace('\n','')

	#get ingredients
	ingredients = soup.find_all('p', {"itemprop":"ingredients"})
	ingredtext = []
	for ingred in ingredients:
		curr_ingred = ingred.text.replace('\n','')
		ingredtext.append(curr_ingred)
	recipe['ingredients'] = ingredtext

	#get directions
	steps = soup.find('div', {"itemprop":"recipeInstructions"}).findChildren()
	stepstext = []
	for step in steps:
	 	curr_step = step.text.replace('\n','')
	 	curr_step = curr_step.replace('  ', '')
	 	curr_step = curr_step.replace('\t', '')
	 	stepstext.append(curr_step)
	recipe['directions'] = stepstext

	return recipe