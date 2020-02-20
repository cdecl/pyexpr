
import re
import json
import yaml
import argparse
import asyncio
from handler import Handler

def match(find, s):
	regex = re.compile(find)
	return None != regex.match(s)

async def parseOne(c, args, name, fnInvoke):
	if args.verbose:
		print('verbose {}'.format('-' * 80))
		print(json.dumps(c, indent=2))
	
	(fire, debug) = fnInvoke(c["path"], c["query"], c["execute"], c["match"], c["debug"])
	print('output {}'.format('-' * 80))
	print('[name] : {}'.format(name))
	print('[fire] : {}'.format(fire))
	print('[debug] : {}'.format(debug))
	print()
	return (fire, debug) 

async def parse(f, args):
	conf = yaml.safe_load(f)
	invoke = Handler()
	retval = []
	wait = []

	for c in conf['tasks']:
		task = c['task']
		if invoke.get(task) is None: continue
		fnInvoke = invoke.get(task)

		name = c['name']
		if not match(args.name, name): continue
		ft = asyncio.ensure_future(parseOne(c, args, name, fnInvoke))
		wait.append(ft)

	asret = await asyncio.gather(*wait)	
	for fire, debug in asret:
		retval.append({'name': name, 'fire': fire, 'debug': debug})
	return retval

async def run(args):
	fname = args.file
	ret = None
	with open(fname, 'r', encoding='utf-8') as f:
		ret = await parse(f, args)
	return ret

def usage():
	parser = argparse.ArgumentParser()
	parser.add_argument('--verbose', '-v', help="verbose", action='store_true')
	parser.add_argument('--file', '-f', help="yaml file ", type=str, default="", required=True)
	parser.add_argument('--name', '-n', help="task name (default: .*)", type=str, default=".*")
	args = parser.parse_args()
	return args

def main():
	args = usage()
	try:
		loop = asyncio.get_event_loop()
		ret = loop.run_until_complete(run(args))
		loop.close()

		print('json {}'.format('-' * 80))
		print(json.dumps(ret, indent=2))
	except Exception as e:
		print(e)

if __name__ == "__main__":
	main()