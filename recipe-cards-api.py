from flask import Flask
from flask import abort
from flask import make_response

app = Flask(__name__)
test_recipe_database = [
	{
		'id': 'someRecipe',
		'url': 'https:www.example.com/meatballs',
		'name': 'Meatballs',
		'source': 'example.com',
		'ingredients': [
			'1 lb ground meat', 
			'1 cup breadcrumbs', 
			'1 egg', 
			'1 cup grated parmesan',
			'spices'
		],
		'directions': [
			'Preheat oven to 400 degrees F',
			'Thoroughly mix ingredients',
			'Form into balls and place onto baking sheet',
			'Bake for 30 minutes'
		]
	}
]
test_user_database = [
	{
		'id': 'someUser',
		'username': 'user@example.com',
		'password': 'pass',
		'recipes': ['someRecipe']
	}
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
	return "Hello, World!" #Temporary home page

@app.route('/recipe-cards/api/v1.0/<string:recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
	recipes = [recipe for recipe in test_recipe_database if recipe['id'] == recipe_id]
	if len(recipes) == 0:
		abort(404)
	return jsonify({'recipe':recipes[0]})

if __name__ == '__main__':
	app.run(debug=True)
