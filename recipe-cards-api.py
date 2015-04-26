from flask import Flask
from flask import abort
from flask import make_response
from flask import jsonify
from flask import request
from flask import render_template
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import logging

#http://stackoverflow.com/questions/19877903/using-mongo-with-flask-and-python used to resolve issue with objectids and json

app = Flask(__name__)

connection = MongoClient("ds031701.mongolab.com", 31701)
db = connection["recipe-cards-db"]
db.authenticate("admin", "password")

def doc_encoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__

@app.errorhandler(400)
def bad_params(error):
    return make_response(jsonify({'error': 'Request not properly formed'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(409)
def dup_login(error):
    return make_response(jsonify({'error': 'A user with that username already exists.'}), 409)

@app.errorhandler(422)
def bad_credentials(error):
    return make_response(jsonify({'error': 'Login credentials are incorrect.'}), 422)

@app.route('/')
def index():
	return render_template('login.html') #Always logs in, change based on session

@app.route('/recipes/<recipe_id>', methods=['GET'])
def recipepage(recipe_id):
	recipe = json.loads(get_recipe_by_id(recipe_id))['recipe']
	return render_template('recipe.html', recipe=recipe)

@app.route('/recipe-cards/api/v1.0/recipes/<recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
	recipes = db.recipes
	try:
		recipe = recipes.find_one({"_id":ObjectId(str(recipe_id))})
	except:
		abort(404)
	if recipe == None:
	 	abort(404)
	return json.dumps({'recipe':recipe}, default=doc_encoder) #replace with one that does not give back objid

@app.route('/recipe-cards/api/v1.0/recipes-by-user/<user_id>', methods=['GET'])
def get_recipes_by_user(user_id):
	users = db.users
	try:
		user = users.find_one({"_id":ObjectId(str(user_id))})
	except:
		abort(404)
	if user == None:
	 	abort(404)
	recipeList = map(lambda x: ObjectId(x), user['recipes'])
	recipes = db.recipes.find({"_id":{"$in": recipeList}})
	recipeList = []
	for recipe in recipes:
	 	recipeList.append({"_id":str(recipe["_id"]),"name":recipe["name"]})
	return json.dumps(recipeList, default=doc_encoder)

@app.route('/recipe-cards/api/v1.0/recipes/recipe-by-url/', methods=['POST'])
def recipe_from_url():
	data = request.form
	if not data or not 'url' in data or not 'userid' in data:
		abort(400)
	recipes = db.recipes
	recipe = recipes.find_one({"url":data['url']})
	if recipe == None:
	 	abort(404) #replace with code to scrape and insert
	 	#recipe["_id"] = recipes.insert(recipe, default=doc_encoder)
	recipeid = str(recipe["_id"])
	users = db.users
	user = users.find_one({"_id":ObjectId(str(data['userid']))})
	if user == None:
		abort(404)
	users.update({'_id':user['_id']},{'$addToSet':{'recipes': recipeid}})
	return json.dumps({'recipeid':recipeid}, default=doc_encoder)

@app.route('/recipe-cards/api/v1.0/create-account/', methods=['POST'])
def create_account():
	data = request.form
	if  not data or not 'username' in data or not 'password' in data:
		abort(400)
	users = db.users
	is_user = users.find_one({"username":data['username']})
	if is_user == None:
		return json.dumps({'userid':users.insert({"username":data['username'], "password":data['password'], "recipes":[]})}, default=doc_encoder)
	abort(409)

@app.route('/recipe-cards/api/v1.0/login/', methods=['POST'])
def login():
	data = request.form
	if  not data or not 'username' in data or not 'password' in data: #needs real authentication
		abort(400)
	users = db.users
	user = users.find_one({"username":data['username']})
	if user == None:
		abort(422)
	return json.dumps({'userid':user['_id']}, default=doc_encoder)

if __name__ == '__main__':
	app.run()
