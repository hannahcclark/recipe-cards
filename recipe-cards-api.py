from flask import Flask, abort, make_response, jsonify, request, render_template, session, url_for, redirect
from pymongo import MongoClient
import bcrypt
import json
from bson.objectid import ObjectId
import logging

#http://stackoverflow.com/questions/19877903/using-mongo-with-flask-and-python used to resolve issue with objectids and json

app = Flask(__name__)
app.config.update(
	SECRET_KEY = open("/dev/random","rb").read(32) 
)
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

@app.route('/')
def index():
	if 'user' in session:
		recipes = get_recipes_by_user(session['user'])
		return render_template('index.html', recipes = recipes) #Index needs fixing up
	return redirect(url_for('login'))

@app.route('/login/', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		data = request.form
		if  not data or not 'username' in data or not 'password' in data:
			return render_template('login.html', error="A required field is empty")
		users = db.users
		user = users.find_one({"username":data['username']})
		if user == None or user['password'] != bcrypt.hashpw(data['password'].encode('UTF-8'), user['password'].encode('UTF-8')):
			return render_template('login.html', error="Invalid username or password")
		session['user'] = str(user['_id'])
		return redirect(url_for('index'))

@app.route('/signup/', methods=['GET', 'POST'])
def create_account():
	if request.method == 'GET':
		return render_template('login.html') #swap to signup
	elif request.method == 'POST':
		data = request.form
		if  not data or not 'username' in data or not 'password' in data:
			return render_template('login.html', error="A required field is empty")#swap to signup
		users = db.users
		is_user = users.find_one({"username":data['username']})
		if is_user == None:
			password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt())
			users.insert({"username":data['username'], "password":password, "recipes":[]})
			session['user'] = str(user['_id'])
			return redirect(url_for('index'))
		return render_template('login.html', error="Username is already taken")#swap to signup.html

@app.route('/signout/')
def signout():
	if 'user' not in session:
		return redirect(url_for('login'))
	session.pop('user', None)
	return redirect(url_for('login'))

@app.route('/recipes/<recipe_id>/', methods=['GET'])
def recipepage(recipe_id):
	recipe = json.loads(get_recipe_by_id(recipe_id))['recipe']
	return render_template('recipe.html', recipe=recipe)

@app.route('/recipe-cards/api/v1.0/recipes/<recipe_id>/', methods=['GET'])
def get_recipe_by_id(recipe_id):
	recipes = db.recipes
	try:
		recipe = recipes.find_one({"_id":ObjectId(str(recipe_id))})
	except:
		abort(404)
	if recipe == None:
	 	abort(404)
	return json.dumps({'recipe':recipe}, default=doc_encoder) #replace with one that does not give back objid

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
	return recipeList

@app.route('/recipe-cards/api/v1.0/recipes/recipe-by-url/', methods=['POST'])
def recipe_from_url():
	data = request.form
	if not data or not 'url' in data or not 'user' in session:
		return render_template('index.html', error="A url is required")
	recipes = db.recipes
	recipe = recipes.find_one({"url":data['url']})
	if recipe == None:
	 	abort(404) #replace with code to scrape and insert
	 	#recipe["_id"] = recipes.insert(recipe, default=doc_encoder)
	recipeid = str(recipe["_id"])
	users = db.users
	user = users.find_one({"_id":ObjectId(str(data['userid']))})
	if user == None:
		return render_template('index.html', error="An error occured with your account. Please try signing out and logging back in.")
	users.update({'_id':user['_id']},{'$addToSet':{'recipes': recipeid}})
	return redirect(url_for('recipes/' + recipeid))

if __name__ == '__main__': 
	app.run()
