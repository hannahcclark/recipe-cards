from flask import Flask
from flask import abort
from flask import make_response
from flask import jsonify
from flask import request
from pymongo import MongoClient
import json
from bson.objectid import ObjectId

#http://stackoverflow.com/questions/19877903/using-mongo-with-flask-and-python used to resolve issue with objectids and json

app = Flask(__name__)

connection = MongoClient("ds031701.mongolab.com", 31701)
db = connection["recipe-cards-db"]
db.authenticate("admin", "password")

def doc_encoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
	return "Hello, World!" #Temporary home page

@app.route('/recipe-cards/api/v1.0/recipes/<recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
	recipes = db.recipes
	recipe = recipes.find_one({"_id":ObjectId(str(recipe_id))})
	if recipe == None:
	 	abort(404)
	return json.dumps({'recipe':recipe}, default=doc_encoder) #replace with one that does not give back objid

@app.route('/recipe-cards/api/v1.0/recipes/recipe-by-url/', methods=['POST'])
def get_recipe_from_url():
	data = request.json
	if  not data or not 'url' in data or not 'userid' in data:
		abort(400)
	recipes = db.recipes
	recipe = recipes.find_one({"url":data['url']})
	if recipe == None:
	 	abort(404) #replace with code to scrape and insert
	users = db.users
	user = users.find_one({"_id":ObjectId(str(data['userid']))})
	if user == None:
		abort(404)
	users.update({'_id':user['_id']},{'$push':{'recipes': str(recipe["_id"])}})
	return json.dumps({'recipe':recipe}, default=doc_encoder)

@app.route('/recipe-cards/api/v1.0/create-account/', methods=['POST'])
def create_account():
	data = request.json
	if  not data or not 'username' in data or not 'password' in data:
		abort(400)
	users = db.users
	is_user = users.find_one({"username":data['username']})
	if is_user == None:
		return json.dumps({'userid':users.insert({"username":data['username'], "password":data['password'], "recipes":[]})}, default=doc_encoder)
	abort(404) #replace with helpful error with message about username is taken

@app.route('/recipe-cards/api/v1.0/login/', methods=['POST'])
def login():
	data = request.json
	if  not data or not 'username' in data or not 'password' in data: #needs real authentication
		abort(400)
	users = db.users
	user = users.find_one({"username":data['username']})
	if user == None:
		abort(404) #replace with helpful error with message about username is taken
	return json.dumps({'userid':user['_id']}, default=doc_encoder)

if __name__ == '__main__':
	app.run()
