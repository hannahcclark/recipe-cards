from bs4 import BeautifulSoup
import urllib2
import re

def url_scraper(url):
<<<<<<< HEAD
	return some_source_scraper(url)
=======
	scraper_fn = some_source_scraper
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	#Given url as a string, give back the result of calling the correct source function
	#either throw exception or give back a dictionary indicating an error
	#if source doesn't have a scraper
	return scraper_fn(url)
>>>>>>> c837825c8788d2303b6f36512c98626c2fe0b562

def some_source_scraper(url):
	recipe = {'url': url}
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
<<<<<<< HEAD
	
	#get source
	recipe['source'] = get_source_site(url)
=======
	#food 52 itemprop="author"
	#food network itemprop="name"
	ingredients = soup.find_next('ul').find_all('li') #might not work - there are a lot of lists on any given page, need to know the class
	steps = soup.find_next('ol').find_all('li')
	stepstext = []
	ingredtext = []
	title = soup.title.string
>>>>>>> c837825c8788d2303b6f36512c98626c2fe0b562

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
<<<<<<< HEAD

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



=======
	recipe['directions'] = stepstext
	recipe['name'] = soup.title.text
	return recipe
>>>>>>> c837825c8788d2303b6f36512c98626c2fe0b562
