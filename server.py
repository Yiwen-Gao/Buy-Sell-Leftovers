from flask import Flask, render_template, Response, request, jsonify, redirect
from werkzeug.utils import secure_filename
import json
import sys
import os

from database import Database

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/assets"
user = None
db = Database()

@app.route("/", methods=["GET"])
def get_base():
	return redirect("/login")

@app.route("/login", methods=["GET"])
def get_login():
	global user

	user = None
	return render_template('login.html')

@app.route("/login-validation", methods=["GET"])
def validate_login():
	global user

	user = request.args.get("user", None)
	return redirect("/home")

@app.route("/home", methods=["GET"])
def get_home():
	return render_template("home.html")

@app.route("/item-listing", methods=["GET"])
def get_item_listing():
	global db

	db.get(search_terms=request.args.get('search', None))
	print(json.dumps(db.access_data(), indent=2))
	return render_template("item-listing.html", data=db.access_data())

@app.route("/item-details/<item_id>", methods=["GET"])
def get_item_details(item_id):
	global db, user
	return render_template("item-details.html", item=db.access_data(item_id), user=user)

@app.route("/item-add", methods=["GET"])
def add_item():
	return render_template("item-edit.html", item={})

@app.route("/item-edit/<item_id>", methods=["GET"])
def edit_item(item_id):
	global db
	return render_template("item-edit.html", item=db.access_data(item_id))

@app.route("/item-delete/<item_id>", methods=["GET"])
def delete_item(item_id):
	global db

	path = db.access_data(item_id)["image"]
	os.remove(path[1:])
	db.delete(item_id)
	return redirect("/item-listing")

@app.route("/item-submit", methods=["POST"])
def submit_item():
	global db, user

	item = (request.form).to_dict()	
	item["image"] = upload_file(request.files["image"])
	print(json.dumps(item, indent=2))

	if item["id"] != "":
		db.put(item)
	else:
		item["user"] = user
		db.post(item)

	return redirect("/item-listing")

def upload_file(file):
	filename = secure_filename(file.filename)
	path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
	file.save(path)
	return "/" + path

@app.route("/item-like/<item_id>", methods=["GET"])
def add_like(item_id):
	global db

	data = {
		"id": item_id,
		"likes": user
	}

	db.put(data)
	return jsonify(item=db.access_data(item_id))

@app.route("/item-comment", methods=["POST"])
def add_comment():
	global db, user

	item = request.get_json()
	data = {
		"id": item["id"],
		"comments": [{"user": user, "comment": item["comment"]}]
	}

	db.put(data)
	return jsonify(item=db.access_data(item["id"]))

if __name__ == "__main__":
   app.run(debug = True)