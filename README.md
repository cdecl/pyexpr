

# PyExpr 
Yaml, Python 표현식 활용 데이터 수집 

## Getting Started

### Prerequisites
- Python 3.6 이상
	- asyncio 

```bash
# requerments.txt 

# Basic : CLI Interfrade 
PyYAML==5.3
requests==2.22.0

# Web : RESET API
flask_api==2.0
gunicorn==20.0.4
```

### Installing

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

- Package 를 받지 못하는 환경 

```bash
$ pip install -r requirements.txt --no-index --find-links=package
```

## Running the tests

### CLI 환경 

```bash
$ python pyexpr.py -h
usage: pyexpr.py [-h] [--verbose] --file FILE [--name NAME]

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         verbose
  --file FILE, -f FILE  yaml file
  --name NAME, -n NAME  task name (default: .*)
```

- Yaml 파일 전체 수행 

```bash
$ python pyexpr.py -f conf/http-sample.yml
output --------------------------------------------------------------------------------
[name] : httpbin-get
[fire] : True
[debug] : {'args': {}, 'headers': {'Accept': '*/*', ...}

output --------------------------------------------------------------------------------
[name] : httpbin-post
[fire] : True
[debug] : {'args': {}, 'data': '{"data": "httpbin-post"}', ...}

json --------------------------------------------------------------------------------
[
  {
    "name": "httpbin-post",
    "fire": true,
    "debug": {
      "args": {},
      "headers": {
      ...
      },
      ...
      "url": "http://httpbin.org/get"
    }
  },
  {
    "name": "httpbin-post",
    "fire": true,
    "debug": {
      "args": {},
      "data": "{\"data\": \"httpbin-post\"}",
      ...
      "json": {
        "data": "httpbin-post"
      },
      ...
      "url": "http://httpbin.org/post"
    }
  }
]
```

- Yaml 파일, task 이름으로 수행 

```bash
python pyexpr.py -f conf/http-sample.yml -n "httpbin-post"
output --------------------------------------------------------------------------------
[name] : httpbin-post
[fire] : True
[debug] : {'args': {}, 'data': '{"data": "httpbin-post"}',...}

json --------------------------------------------------------------------------------
[
  {
    "name": "httpbin-post",
    "fire": true,
    "debug": {
      "args": {},
      "data": "{\"data\": \"httpbin-post\"}",
      ...
      "url": "http://httpbin.org/post"
    }
  }
]
```

#### CLI 환경에서의 Response 
- json -- 이하 항목을 이용 

```bash
json --------------------------------------------------------------------------------
[
  {
    "name": "httpbin-post",
    "fire": true,
    "debug": {
      "args": {},
      "data": "{\"data\": \"httpbin-post\"}",
      ...
      "url": "http://httpbin.org/post"
    }
  }
]
```

### REST API 환경 

- 테스트용 서버 실행 

```bash
$ python index.py

 * Serving Flask app "index" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

- Product용 서버 실행 

```bash
$ gunicorn -b :5000 --threads=2 --workers=4 --reload index:app

[2020-02-20 11:46:49 +0900] [73003] [INFO] Starting gunicorn 20.0.4
[2020-02-20 11:46:49 +0900] [73003] [INFO] Listening at: http://0.0.0.0:5000 (73003)
[2020-02-20 11:46:49 +0900] [73003] [INFO] Using worker: threads
[2020-02-20 11:46:49 +0900] [73006] [INFO] Booting worker with pid: 73006
[2020-02-20 11:46:49 +0900] [73007] [INFO] Booting worker with pid: 73007
[2020-02-20 11:46:49 +0900] [73008] [INFO] Booting worker with pid: 73008
[2020-02-20 11:46:49 +0900] [73010] [INFO] Booting worker with pid: 73010
```

#### REST API 테스트 
- Yaml 파일은 conf 디렉토리에 위치
- Yaml 지정을 확장자 없는 이름으로 지정 


##### Url 형식 

```text
http://localhost:5000/expr/{yaml_no_extension}
http://localhost:5000/expr/{yaml_no_extension}/{task_name}
```

##### Json Response

```
- {"status": 200, "data": [{"name": "", "fire": bool, "debug": "..."}
```

##### Test

```bash
$ curl http://localhost:5000/expr/http-sample/
{"status": 200, "data": [{"name": "httpbin-post", "fire": true, "debug": {...}


$ curl http://localhost:5000/expr/http-sample/httpbin-get
{"status": 200, "data": [{"name": "httpbin-post", "fire": true, "debug": {...}}

# {"status": 200, "data": [{"name": "", "fire": bool, "debug": "..."}
```


## Yaml - handler function

#### Concept 
- http 
	- path : url
	- query : http body 
	- expr : json 
- file
	- path : file path 
	- query : 정규식 표현 (re.findall)
	- expr : text
- mysql 
	- path : connection string 
	- query : sql query 
	- expr : named cursor
- tcp
	- path : address, port
	- query : send data
	- expr : recv data


#### Yaml Template

```yml
tasks:
  - task: http                         # Handler name
    name: httpbin-get                  # Task name
    path: http://httpbin.org/get       # 소스 경로 
    query:                             # 검색어, http 모듈의 경우 body 전송 데이터 
    execute: |                         # [python] expr 변수에 결과값 저장됨
      user = expr['headers']['User-Agent']
	match: ('requests' in user)        # [python] bool 형식의 지표 평가 
	                                   #   response name : fire 
	debug: expr                        # [python] debug print 항목
	                                   #   response name : debug
```

#### Handler Function 

```python 
class Handler:
	# 생성자: Task 이름과 Handler 함수 매핑
	def __init__(self):
		self.funcs = {}
		self.funcs['http'] = Handler.http_handler  

	# Interface 형식
	# (path, query, execute, match, debug) 형식의 Arguments 
	# Yaml 파일 항목과 매칭 
	@staticmethod
	def http_handler(path, query, execute, match, debug):
		pass
```


## Parallel 

### asyncio  
- asyncio 사용하여 비동기로 task 수행 
- asyncio concept 코드

```python
#-*- coding: utf-8 -*-
import asyncio
 
async def add(a, b):
	print('add: {0} + {1}'.format(a, b))
	await asyncio.sleep(2.0)  # 2초 대기
	return a + b  

async def run():
	ret = []
	# 3.7 이상은 create_task() 사용 
	# 3.6 ensure_future() 사용 
	ret.append(asyncio.ensure_future(add(1, 1)))
	ret.append(asyncio.ensure_future(add(2, 2)))
	ret.append(asyncio.ensure_future(add(3, 3)))
	
	result = await asyncio.gather(*ret)
	print(result)

	return True

def main():
	# asyncio.run() 3.7 이상 지원 - 개고생 
	# r = asyncio.run(submain())

	# 3.6 이상 
	loop = asyncio.get_event_loop()
	ok = loop.run_until_complete(run())
	loop.close()

	# 3개의 호출의 결과로 2초 * 3 = 6초 후 결과가 나와야 하나
	# 2초 후 동시에 결과 리턴 
	print(ok)

if __name__ == "__main__":
	main()

```

```bash
add: 1 + 1
add: 2 + 2
add: 3 + 3
[2, 4, 6]
True
```

### CLI Command 
- Parallel 가능한 CLI 명령어를 통해 실행 

#### parun
- https://github.com/cdecl/go-parun
- golang 으로 제작된 병렬 수행도구 (goroutine 사용)

```bash
$ cat name.txt | bin/parun -p 8 venv/bin/python pyexpr.py -v -f conf/tasks.yml -n
```

```bash
$ bin/parun -h
Usage of bin/parun:
  -f string
        Input file path, default
  -i    Placeholder (default : {})
  -p int
        Thread pool count (default 1)
```
