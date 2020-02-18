
import json
import yaml
import requests 
import argparse

def get_query(path, query, execute, match, debug):
	url = path
	payload = json.dumps(query)
	headers = {'content-type': 'application/json'}
	response = requests.get(url, data=payload, headers=headers)
	expr = response.json()
	
	if not match: match = 'True'
	if not debug: debug = 'expr'
	if execute: exec(execute)

	return (eval(match), eval(debug))

# def filequery(path, execute, query, match, debug):
# 	with open(path, encoding='utf-8') as fin:
# 		txt = fin.read()
# 		regex = re.compile(query)
# 		expr = regex.findall(txt, re.M)
# 		if not debug: debug = 'expr'
# 		exec(execute)
# 		return (eval(match), eval(debug))

handler = {}
handler['http'] = get_query

def parse(f, args):
	conf = yaml.safe_load(f)

	for c in conf["tasks"]:
		task = c['task']
		if not task in handler: continue

		if args.verbose:
			print(c)
		
		(ok, debug) = handler[task](c["path"], c["query"], c["execute"], c["match"], c["debug"])
		print('ok : {}'.format(ok))
		print('debug : {}'.format(debug))
		print()

def runConfig(args):
	with open('conf.yml', 'r', encoding='utf-8') as f:
		try:
			parse(f, args)
		except Exception as e:
			print(e)

def usage():
	parser = argparse.ArgumentParser()
	parser.add_argument('--verbose', '-v', help="verbose", action='store_true')
	args = parser.parse_args()
	return args

def main():
	args = usage()
	runConfig(args)

if __name__ == "__main__":
	main()