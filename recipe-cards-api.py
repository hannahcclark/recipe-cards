from flask import Flask
from flask import abort
from flask import make_response
from flask import jsonify

app = Flask(__name__)
test_recipe_database = [
	{
		'id': u'someRecipe',
		'url': u'https:www.example.com/meatballs',
		'name': u'Meatballs',
		'source': u'example.com',
		'ingredients': [
			u'1 lb ground meat', 
			u'1 cup breadcrumbs', 
			u'1 egg', 
			u'1 cup grated parmesan',
			u'spices'
		],
		'directions': [
			u'Preheat oven to 400 degrees F',
			u'Thoroughly mix ingredients',
			u'Form into balls and place onto baking sheet',
			u'Bake for 30 minutes'
		]
	}
]
test_user_database = [
	{
		'id': u'someUser',
		'username': u'user@example.com',
		'password': u'pass',
		'recipes': [u'someRecipe']
	}
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
	return "Hello, World!" #Temporary home page

@app.route('/recipe-cards/api/v1.0/recipes/<recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
	recipes = [recipe for recipe in test_recipe_database if recipe['id'] == unicode(recipe_id)]
	if len(recipes) == 0:
	 	abort(404)
	return jsonify({'recipe':recipes[0]})

if __name__ == '__main__':
	app.run()
