#recipe.card
Using online recipes, as opposed to cookbooks, is becoming very common. However, on many sites text is small and requires keeping a device closer to the food and wet surfaces than ideal. Magnifying text requires frequent scrolling and getting food on the device. The problem is not finding recipes, but using them after finding ones from a favorite site. We will also streamline shopping for ingredients for multiple recipes, to create an appealing digital cooking utility.

We will create a website that will generate a recipe card from a URL of a recipe page on one of several popular recipe source websites and allow the user to save it in their recipes. The user will be able to view recipes in a cooking mode, where a small portion of the directions will be displayed on the screen, and the directions can be swapped between easily. As an additional incentive to use the product mobile users will also be able to generate a shopping list from ingredients in recipes they select as well as the nearest supermarkets.

##Features
* We will scrape the file at a user provided URL to generate a recipe card. This information will be stored in a database. (Pick 5: Data or screen scraping, Server-side data persistence)
* We will allow the user to alternate between a printer friendly full view of the recipe and a cooking view.
* The cooking view will move either forward or backwards in the steps by pressing any letter key in the appropriate half of the keyboard, as well as buttons.
* The space bar will show or hide the ingredient sidebar when in cooking view.
* We will allow the user to look through their previously saved recipes.
* We will allow the user to choose between two different styles of view.
* We will allow the user to text ingredients of a recipe to themselves or someone else. (Pick 5: Send emails, SMSes, or push notifications)
* We will allow the user to include the address of the supermarket nearest them or an address in the SMS (Pick 5: Geolocation, Google Places and Geocoding APIs)
* We will be using a Bootstrap to help accomplish implementing our planned features. (Pick 5: Front-end framework)

##Data Collected
* We will use and store very basic user information for accounts, such as name and login information.
* We will use and store user preferences about style.
* We will use but not store the user location for generating a list of supermarkets.
* We will be using and storing information about the recipes: the original url, the ingredients, and the directions.

##Algorithms/Special Techniques
* We will need to accurately scrape recipe information for different websites that will likely present it in different formats.

##Mockups
###Front Page
![Cooking View Wireframe](https://github.com/tuftsdev/comp20-spring2015-team13/blob/master/Wireframes/newuser.png)
![Cooking View Wireframe](https://github.com/tuftsdev/comp20-spring2015-team13/blob/master/Wireframes/ruserpage.png)
###Recipe View
![Cooking View Wireframe](https://github.com/tuftsdev/comp20-spring2015-team13/blob/master/Wireframes/mockup.png)
###Cooking View
![Cooking View Wireframe](https://github.com/tuftsdev/comp20-spring2015-team13/blob/master/Wireframes/cookingview.png)
###Mobile Features Views
![Cooking View Wireframe](https://github.com/tuftsdev/comp20-spring2015-team13/blob/master/Wireframes/mobileview.png)

#Comments by Ming
1. WAY too ambitious, you will be lucky to complete 2 or 3 of the features listed well.
2. Be very careful with data scraping. It can be ugly.
3. Lovely wireframes
4. What APIs will you be using?
5. Overall score: 14/15
