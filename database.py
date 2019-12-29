import requests

class Database():

	def __init__(self):
		self.API = "https://3b7rp9lxz0.execute-api.us-east-2.amazonaws.com/default/dynamodb-manage-buy-sell-leftovers-nodejs"
		self.data = {}
		self.get()

	def access_data(self, id=None):
		if id:
			return self.data[id]  
		else:
			return list((self.data).values())

	def get(self, id=None, search_terms=None):
		params = {
			"id": id,
			"searchTerms": search_terms
		}

		response = requests.get(url=self.API, params=params)		
		if not id:
			self.data = {}
		for item in response.json():
			self.data[item["id"]] = item 

	def post(self, data):
		requests.post(url=self.API, json=data)
		self.get(id=data["id"])

	def put(self, data):
		requests.put(url=self.API, json=data)
		self.get(id=data["id"])

	def delete(self, id):
		params = {
			"id": id
		}

		requests.delete(url=self.API, params=params)
		self.get()