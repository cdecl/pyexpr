
import re
import json
import requests 

class Handler:
	def __init__(self):
		self.funcs = {}
		self.funcs['http'] = Handler.http_handler

	def get(self, name):
		fn = None
		if name in self.funcs:
			fn = self.funcs[name]
		return fn

	@staticmethod
	def http_handler(path, query, execute, match, debug):
		method = 'GET'
		url = path
		m = re.findall('([\w]{3,4})[ ]+(http.*)', path)
		if len(m) > 0: 
			method = m[0][0]
			url = m[0][1]

		payload = json.dumps(query)
		headers = {'content-type': 'application/json'}
		response = requests.request(method, url, data=payload, headers=headers) 
		expr = response.json()
		if not match: match = 'False'
		if not debug: debug = 'expr'
		if execute: exec(execute)
		return (eval(match), eval(debug))
