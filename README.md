#recipe.card
Using online recipes, as opposed to cookbooks, is becoming very common. However, on many sites text is small and requires keeping a device closer to the food and wet surfaces than ideal. Magnifying text requires frequent scrolling and getting food on the device. The problem is not finding recipes, but using them after finding ones from a favorite site. We will also streamline shopping for ingredients for multiple recipes, to create an appealing digital cooking utility.

We will create a website that will generate a recipe card from a URL of a recipe page on one of several popular recipe source websites and allow the user to save it in their recipes. The user will be able to view recipes in a cooking mode, where a small portion of the directions will be displayed on the screen, and the directions can be swapped between easily. As an additional incentive to use the product mobile users will also be able to generate a shopping list from ingredients in recipes they select as well as a list of the nearest supermarkets.

##Features
* We will scrape the file at a user provided URL to generate a recipe card. This information will be stored in a database. (Pick 5: Data or screen scraping, Server-side data persistence)
* We will allow the user to choose between two different view styles of the website, and remember their preferences locally. (Pick 5: Client-side data persistence)
* We will allow the user to alternate between a printer friendly full view of the recipe and a cooking view.
* The cooking view will move either forward or backwards in the steps by pressing any letter key in the appropriate half of the keyboard, as well as buttons.
* The space bar will show or hide the ingredient sidebar when in cooking view.
* We will allow the user to look through their previously saved recipes.
* We will allow the user to choose between two different styles of view.
* We will allow the user to generate and view a shopping list from selected recipes, with the option to email or text it to themselves or someone else. (Pick 5: Send emails, SMSes, or push notifications)
	* Identical ingredients from several recipes to one item will be combined if possible.
* We will allow the user to view the nearest supermarkets to them as a list and on a map. (Pick 5: Geolocation)
* We will be using a currently unchosen front-end framework to help accomplish implementing our planned features.

##Data Collected
* We will use and store very basic user information for accounts, such as name and login information.
* We will use and store user preferences about style.
* We will use but not store the user location for generating a list of supermarkets.
* We will be using and storing information about the recipes: the original url, the ingredients, and the directions.

##Algorithms/Special Techniques
* We will need to accurately scrape recipe information for different websites that will likely present it in different formats.
* We will also need to come up with a method of determining "sameness" of ingredients. For example:
	* tomatoes, diced is equal to tomatoes because it implies fresh tomatoes that are diced by the cook
	* diced tomatoes is not equal to tomatoes because it implies canned diced tomatoes
* We will possible need to determine how to add different measures if we include amount for items in the shopping list.

##Mockups
###Front Page
###Recipe View
###Cooking View
![Cooking View Wireframe](https://github.com/tuftsdev/comp20-spring2015-team13/blob/master/Wireframes/cookingview.png)
###Mobile Features Views
![Cooking View Wireframe](https://github.com/tuftsdev/comp20-spring2015-team13/blob/master/Wireframes/mobileview.png)

