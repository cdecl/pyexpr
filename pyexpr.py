
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

handler = {}
handler['http'] = get_query

def parse(f, args):
	conf = yaml.safe_load(f)
	
	for c in conf['tasks']:
		task = c['task']
		if not task in handler: continue

		name = c['name']
		if args.name and args.name != name: continue

		if args.verbose:
			print('verbose {}'.format('-' * 80))
			print(json.dumps(c, indent=4))
		
		(fire, debug) = handler[task](c["path"], c["query"], c["execute"], c["match"], c["debug"])
		print('output {}'.format('-' * 80))
		print('[fire] : {}'.format(fire))
		print('[debug] : {}'.format(debug))
		print()

def runYaml(args):
	fname = args.file
	with open(fname, 'r', encoding='utf-8') as f:
		try:
			parse(f, args)
		except Exception as e:
			print(e)

def usage():
	parser = argparse.ArgumentParser()
	parser.add_argument('--verbose', '-v', help="verbose", action='store_true')
	parser.add_argument('--file', '-f', help="yaml file ", type=str, default="tasks.yml")
	parser.add_argument('--name', '-n', help="task name", type=str, default="")
	args = parser.parse_args()
	return args

def main():
	args = usage()
	runYaml(args)

if __name__ == "__main__":
	main()