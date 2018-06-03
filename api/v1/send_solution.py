import json
from api.handler import IHandler
from kernel.testing_task import TTestingTask
from db.query import *

def send_answer(request, response):
    request.send_response(200)
    print(response)
    data = bytes(json.dumps(response), 'utf-8')
    request.send_header('Content-Length', len(data))
    request.send_header('Connection', 'close')
    request.end_headers()
    request.wfile.write(data)
    request.wfile.flush()

def send_result(request, task):
    status = task.status
    response = {'status': status, 'result': task.result}
    send_answer(request, response)

def cb(tt, sid, tid):
    print (tt.result)
    if 'ok\n' not in tt.result:
        res = 0
    else:
        res = tt.result['ok\n']
    set_result(res, sid, tid)

class TApiCallHandler(IHandler):
    tasks = {}

    def handle(self, handler):
        content_type = handler.headers['Content-Type']
        if content_type.lower() != 'application/json':
            handler.send_error(400, 'Bad request')
            return

        content_length = int(handler.headers['Content-Length'])
        body = handler.rfile.read(content_length).decode('utf-8')
        print (body)
        try:
            request = json.loads(body)
            type = request['type']

            if type == 'send_solution':
                tid = int(request['tid'])
                sid = request['sid']
                code = request['code']
                tests = request['tests']
                data = load_task_data(tid)
                task = TTestingTask(code, {"optimization_level":"3"}, tests, data[0][5], "statistics")
                self.tasks[task.number] = task
                response = {'status': 'added', 'token': task.number}
                send_answer(handler, response)
                task.start()
                task.add_cb(lambda x: cb(x, sid, tid))
            else:
                handler.send_error(400, 'Bad request type')

        except json.JSONDecodeError as e:
            handler.send_error(400, 'Bad JSON')
            print(e)
            print(body)
        except (AttributeError, KeyError) as e:
            handler.send_error(400, 'Bad request')
            print(e)
            return
