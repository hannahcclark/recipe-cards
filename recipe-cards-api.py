from flask import Flask, abort, make_response, jsonify, request, render_template, session, url_for, redirect
from pymongo import MongoClient
import os
import bcrypt
import json
from bson.objectid import ObjectId
from twilio.rest import TwilioRestClient 

#http://stackoverflow.com/questions/19877903/using-mongo-with-flask-and-python used to resolve issue with objectids and json

app = Flask(__name__)
app.config.update(
	SECRET_KEY = open("/dev/random","rb").read(32) 
)
connection = MongoClient("ds031701.mongolab.com", 31701)
db = connection["recipe-cards-db"]
db.authenticate("admin", "password")

@app.errorhandler(500)
def bad_params(error):
    return make_response(jsonify({error: error}), 500)

def doc_encoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__

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
		elif 'button' in data and data['button'] == 'create':
			return create_account()
		users = db.users
		user = users.find_one({"username":data['username']})
		if user == None:
			return render_template('login.html', error="Invalid username")
		elif user['password'] != bcrypt.hashpw(data['password'].encode('UTF-8'), user['password'].encode('UTF-8')):
			return render_template('login.html', error="Invalid password")
		session['user'] = str(user['_id'])
		return redirect(url_for('index'))

@app.route('/signup/', methods=['POST'])
def create_account():
	data = request.form
	if  not data or not 'username' in data or not 'password' in data:
		return render_template('login.html', error="A required field is empty")
	users = db.users
	is_user = users.find_one({"username":data['username']})
	if is_user == None:
		password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt())
		user = users.insert({"username":data['username'], "password":password, "recipes":[]})
		session['user'] = str(user)
		return redirect(url_for('index'))
	return render_template('login.html', error="Username is already taken")

@app.route('/signout/')
def signout():
	if 'user' not in session:
		return redirect(url_for('login'))
	session.pop('user', None)
	return redirect(url_for('login'))

@app.route('/recipes/<recipe_id>/', methods=['GET'])
def recipepage(recipe_id):
	recipe = json.loads(get_recipe_by_id(recipe_id))
	return render_template('recipe.html', recipe=recipe)

@app.route('/recipe-by-url/', methods=['POST'])
def recipe_by_url():
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
	user = users.find_one({"_id":ObjectId(str(session['user']))})
	if user == None:
		return render_template('index.html', error="An error occured with your account. Please try signing out and logging back in.")
	users.update({'_id':user['_id']},{'$addToSet':{'recipes': recipeid}})
	return redirect(url_for('recipepage', recipe_id=recipeid))

@app.route('/recipe-cards/api/v1.0/recipes/<recipe_id>/', methods=['GET'])
def get_recipe_by_id(recipe_id):
	recipes = db.recipes
	try:
		recipe = recipes.find_one({"_id":ObjectId(str(recipe_id))})
	except:
		return make_response(jsonify({'error': 'Request not properly formed'}), 404)
	if recipe == None:
	 	return make_response(jsonify({'error': 'Request not properly formed'}), 404)
	return json.dumps(recipe, default=doc_encoder)


@app.route('/sendSMS/', methods=['POST'])
def sendSMS():
	data = request.form
	if not data or not 'phone' in data or not 'msg' in data:
		return make_response(jsonify({'error': 'Request not properly formed'}), 404)
	key = os.environ['TWILIO_API']
	secret = os.environ['TWILIO_SECRET']
	from_num = "+18604847973"
	client = TwilioRestClient(key, secret) 
	req = client.messages.create(
		to=data['phone'], 
		from_=from_num, 
		body=data['msg'],  
	)
	print req.status
	return jsonify(success = True)

def get_recipes_by_user(user_id):
	users = db.users
	try:
		user = users.find_one({"_id":ObjectId(str(user_id))})
	except:
		abort(404)
	if user == None:
	 	abort(404)
	recipe_list = map(lambda x: ObjectId(x), user['recipes'])
	recipes = db.recipes.find({"_id":{"$in": recipe_list}})
	recipe_list = []
	for recipe in recipes:
	 	recipe_list.append({"_id":str(recipe["_id"]),"name":recipe["name"]})
	return recipe_list
if __name__ == '__main__': 
	app.run()
