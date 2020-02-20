
import os
import json
from datetime import datetime
from flask_api import FlaskAPI
import pyexpr
import asyncio

app = FlaskAPI(__name__)
loop = asyncio.get_event_loop()

class Args:
	verbose = True
	file = ''
	name = ''

def getArgs(conf, name):
	curdir = os.path.dirname(os.path.abspath(__file__))
	args = Args()
	args.file = os.path.join(curdir, 'conf', '{}.yml'.format(conf))
	args.name = name
	print(args.file)
	return args

@app.route('/expr/<string:conf>/', defaults={'name': '.*'}, methods=['GET', 'POST'])
@app.route('/expr/<string:conf>/<string:name>', methods=['GET', 'POST'])
def expr_execute(conf, name):
	args = getArgs(conf, name)
	ret = {}
	try:
		# ret = pyexpr.run(args)
		ret = loop.run_until_complete(pyexpr.run(args))
		ret = {'status': 200, 'data' : ret}
	except Exception as e:
		ret = {'status': 500, 'data' : e}
	return ret

@app.route("/", methods=['GET', 'POST'])
def index():
	return 'Alive : ' + datetime.now().strftime('%Y-%m-%D %H:%M:%S')


if __name__ == '__main__':
	# app.run(debug=True)
	app.run(host='0.0.0.0')
