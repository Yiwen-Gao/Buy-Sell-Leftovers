from flask import Flask, render_template, Response, request, jsonify, redirect
import json
import sys
app = Flask(__name__)

user = None
data = {}
new_id = 1

def reset_data():
	global data
	global user
	global new_id

	with open("./data/data.json", "r") as f:
		temp = json.load(f)
		for item in temp.values():
			title_terms = item["title"].lower().split()
			description_terms = item["description"].lower().split()
			item["search_terms"] = title_terms + description_terms

			item["image"] = "/static/assets/" + item["image"] if "http" not in item["image"] and "/static/assets/" not in item["image"] else item["image"]
			item["likedByUser"] = True if user in item["likes"] else False

			data[str(item["id"])] = item

	new_id = len(data) + 1

def write_to_file():
	global data
	with open("./data/data.json", "w") as f:
		json.dump(data, f)

@app.route("/", methods=["GET"])
def get_base():
	return redirect("/login")

@app.route("/login", methods=["GET"])
def get_login():
	return render_template('login.html')

@app.route("/login-validation", methods=["GET"])
def validate_login():
	global user
	user = request.args.get("user", None)
	reset_data()
	return redirect("/home")

@app.route("/home", methods=["GET"])
def get_home():
	return render_template('home.html')

@app.route("/item-listing", methods=["GET"])
def get_item_listing():
	global data
	results = {}

	query = request.args.get('search', None)
	if query:
		search_terms = set(query.lower().split())
		for item in data.values():
			if search_terms.intersection(set(item["search_terms"])):
				results[item["id"]] = item
	else:
		results = data

	return render_template('item-listing.html', data=results)

@app.route('/item-details/<item_id>', methods=["GET"])
def get_item_details(item_id):
	global data
	global user
	return render_template('item-details.html', item=data[item_id], user=user)

@app.route('/item-add', methods=["GET"])
def add_item():
	global data
	return render_template('item-edit.html', item={})

@app.route('/item-edit/<item_id>', methods=["GET"])
def edit_item(item_id):
	global data
	return render_template('item-edit.html', item=data[item_id])

@app.route('/item-delete/<item_id>', methods=["GET"])
def delete_item(item_id):
	global data
	
	del data[item_id]
	write_to_file()

	return redirect("/item-listing")

@app.route('/item-submit', methods=["POST"])
def submit_item():
	global data
	global user
	global new_id

	item = (request.form).to_dict()
	title_terms = item["title"].lower().split()
	description_terms = item["description"].lower().split()		
	item["search_terms"] = title_terms + description_terms 

	if item["id"] != "":
		data[item["id"]] = item
	else:
		item["id"] = new_id
		item["user"] = user
		item["likes"] = []
		item["comments"] = []
		data[str(new_id)] = item
		new_id += 1

	write_to_file()

	return redirect("/item-listing")

@app.route('/item-like-toggle/<item_id>', methods=["GET"])
def toggle_like(item_id):
	global data
	global user

	liked_users = set(data[item_id]["likes"])
	if user in liked_users:
		liked_users.remove(user)
		data[item_id]["likedByUser"] = False
	else:
		liked_users.add(user)
		data[item_id]["likedByUser"] = True

	data[item_id]["likes"] = list(liked_users)
	write_to_file()

	return jsonify(item=data[item_id])

@app.route('/item-comment', methods=["POST"])
def add_comment():
	global data
	global user

	item = request.get_json()
	item_id = str(item["id"])
	comment = {"user": user, "comment": item["comment"]}
	
	data[item_id]["comments"].append(comment)
	write_to_file()

	return jsonify(item=data[item_id])

if __name__ == '__main__':
   app.run(debug = True)