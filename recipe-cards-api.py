from flask import Flask
from flask import abort
from flask import make_response
from flask import jsonify
from flask import request
from pymongo import MongoClient
import json
from bson.objectid import ObjectId

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
	return json.dumps({'recipe':recipe}, default=doc_encoder)

# @app.route('/recipe-cards/api/v1.0/recipes/recipe-by-url/', methods=['POST'])
# def get_recipe_from_url():
# 	if  not request.json or not 'url' in request or not 'username' in request:
# 		abort(400)


if __name__ == '__main__':
	app.run()
