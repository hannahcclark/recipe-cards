import os
from flask import Flask
from flask import abort
from flask import make_response
from flask import jsonify
from flask import request
from mongokit import Connection, Document
from urlparse import urlsplit

app = Flask(__name__)

#http://stackoverflow.com/questions/26617085/flask-with-mongodb-using-mongokit-to-mongolabs
db_url = os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017/recipe-cards-db')
parsed = urlsplit(db_url)
app.config['MONGODB_DATABASE'] = parsed.path[1:]
if '@' in parsed.netloc:
    # If there are authentication details, split the network locality.
    auth, server = parsed.netloc.split('@')
    # The username and password are in the first part, separated by a :.
    app.config['MONGODB_USERNAME'], app.config['MONGODB_PASSWORD'] = auth.split(':')
else:
    # Otherwise the whole thing is the host and port.
    server = parsed.netloc

# Split whatever version of netloc we have left to get the host and port.
app.config['MONGODB_HOST'], app.config['MONGODB_PORT'] = server.split(':')

connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])

class User(Document):
	__collection__ = 'users'
	__database__ = 'recipe-cards-db'
	structure = {
		'name': unicode,
		'username': unicode,
		'password': unicode,
		'recipes': [int]
	}
	use_dot_notation = True
	def __repr__(self):
        return '<User %r>' % (self.name)

connection.register([User])

class Recipe(Document):
	__collection__ = 'recipes'
	__database__ = 'recipe-cards-db'
	structure = {
		'id': int,
		'name': unicode,
		'source': unicode,
		'url': unicode,
		'ingredients': [unicode],
		'directions': [unicode]
	}
	use_dot_notation = True
	def __repr__(self):
        return '<Recipe %r>' % (self.name)

connection.register([Recipe])

# test_recipe_database = [
# 	{
# 		'id': u'someRecipe',
# 		'url': u'https:www.example.com/meatballs',
# 		'name': u'Meatballs',
# 		'source': u'example.com',
# 		'ingredients': [
# 			u'1 lb ground meat', 
# 			u'1 cup breadcrumbs', 
# 			u'1 egg', 
# 			u'1 cup grated parmesan',
# 			u'spices'
# 		],
# 		'directions': [
# 			u'Preheat oven to 400 degrees F',
# 			u'Thoroughly mix ingredients',
# 			u'Form into balls and place onto baking sheet',
# 			u'Bake for 30 minutes'
# 		]
# 	}
# ]
# test_user_database = [
# 	{
# 		'id': u'someUser',
# 		'username': u'user@example.com',
# 		'password': u'pass',
# 		'recipes': [u'someRecipe']
# 	}
# ]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
	return "Hello, World!" #Temporary home page

@app.route('/recipe-cards/api/v1.0/recipes/<int: recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
	recipes = list(connection.User.find_one({'id':recipe_id}))
	if len(recipes) == 0:
	 	abort(404)
	return jsonify({'recipe':recipes[0]})

# @app.route('/recipe-cards/api/v1.0/recipes/recipe-by-url/', methods=['POST'])
# def get_recipe_from_url():
# 	if  not request.json or not 'url' in request or not 'username' in request:
# 		abort(400)


if __name__ == '__main__':
	app.run()
