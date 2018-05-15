import json
from api.handler import IHandler
from kernel.testing_task import TTestingTask

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
            if type == 'run_tests':
                task = TTestingTask(
                    request['data']['code'],
                    request['data']['options'],
                    request['data']['tests'],
                    request['data']['verifier'],
                    request['data']['response_type'])
                self.tasks[task.number] = task
                response = {'status': 'added', 'token': task.number}
                send_answer(handler, response)
                task.start()
            elif type == 'update_status':
                num = request['token']
                if num not in self.tasks:
                    response = {'status': 'not_found'}
                    send_answer(handler, response)
                else:
                    task = self.tasks[num]
                    callback = lambda tt: send_result(handler, tt) 
                    task.add_cb(callback)
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

