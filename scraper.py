#Module for scraper functions

def url_scraper(url):
	scraper_fn = some_source_scraper
	#Given url as a string, give back the result of calling the correct source function
	#either throw exception or give back a dictionary indicating an error
	#if source doesn't have a scraper
	return scraper_fn(url)

def some_source_scraper(url):
	recipe = {'url': url, 'source':'some_source.com'}#replace with correct source
	#do scraping
	#insert name of recipe under key 'name'
	#insert array of ingredients under 'ingredients'
	#insert array of instructions under key 'directions'
	return recipe