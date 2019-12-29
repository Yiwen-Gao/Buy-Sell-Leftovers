from flask import Flask, render_template, Response, request, jsonify, redirect
from werkzeug.utils import secure_filename
import json
import sys
import os

from src.database import Database

application = Flask(__name__)
application.config["UPLOAD_FOLDER"] = "src/static/assets"
user = None
db = Database()

@application.route("/", methods=["GET"])
def get_base():
	return redirect("/login")

@application.route("/login", methods=["GET"])
def get_login():
	global user
	
	user = None
	return render_template("login.html")

@application.route("/login-validation", methods=["GET"])
def validate_login():
	global user

	user = request.args.get("user", None)
	return redirect("/home")

@application.route("/home", methods=["GET"])
def get_home():
	global user

	if user == None:
		return redirect("/login")
	else:
		return render_template("home.html")

@application.route("/item-listing", methods=["GET"])
def get_item_listing():
	global db, user

	if user == None:
		return redirect("/login")

	db.get(search_terms=request.args.get('search', None))
	print(json.dumps(db.access_data(), indent=2))
	return render_template("item-listing.html", data=db.access_data())

@application.route("/item-details/<item_id>", methods=["GET"])
def get_item_details(item_id):
	global db, user

	if user == None:
		return redirect("/login")
	else:
		return render_template("item-details.html", item=db.access_data(item_id), user=user)

@application.route("/item-add", methods=["GET"])
def add_item():
	global user

	if user == None:
		return redirect("/login")
	else:
		return render_template("item-edit.html", item={})

@application.route("/item-edit/<item_id>", methods=["GET"])
def edit_item(item_id):
	global db, user

	if user == None:
		return redirect("/login")
	else:
		return render_template("item-edit.html", item=db.access_data(item_id))

@application.route("/item-delete/<item_id>", methods=["GET"])
def delete_item(item_id):
	global db, user

	if user == None:
		return redirect("/login")

	image_path = db.access_data(item_id)["image"]
	os.remove("src" + image_path)
	db.delete(item_id)
	return redirect("/item-listing")

@application.route("/item-submit", methods=["POST"])
def submit_item():
	global db, user

	if user == None:
		return redirect("/login")

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
	path = os.path.join(application.config["UPLOAD_FOLDER"], filename)
	file.save(path)
	return "/static/assets/" + filename

@application.route("/item-like/<item_id>", methods=["GET"])
def add_like(item_id):
	global db, user

	if user == None:
		return redirect("/login")

	db.put({
		"id": item_id,
		"likes": user
	})
	return jsonify(item=db.access_data(item_id))

@application.route("/item-comment", methods=["POST"])
def add_comment():
	global db, user

	if user == None:
		return redirect("/login")

	item = request.get_json()
	db.put({
		"id": item["id"],
		"comments": [{"user": user, "comment": item["comment"]}]
	})
	return jsonify(item=db.access_data(item["id"]))

if __name__ == "__main__":
   application.run(debug=True)
