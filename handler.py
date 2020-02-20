
import re
import json
import requests 

class Handler:
	def __init__(self):
		self.funcs = {}
		self.funcs['http'] = Handler.get_query

	def get(self, name):
		fn = None
		if name in self.funcs:
			fn = self.funcs[name]
		return fn

	@staticmethod
	def get_query(path, query, execute, match, debug):
		url = path
		payload = json.dumps(query)
		headers = {'content-type': 'application/json'}
		response = requests.get(url, data=payload, headers=headers) 
		expr = response.json()
		if not match: match = 'False'
		if not debug: debug = 'expr'
		if execute: exec(execute)
		return (eval(match), eval(debug))
