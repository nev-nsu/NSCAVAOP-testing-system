from api import api
from kernel.testing_task import TestingTask
import json

class TApiCallHandler(api.IHandler):
    tasks = {}

    def handle(self, TRequestHandler):
        content_type = TRequestHandler.headers['Content-Type']
        if content_type.lower() != 'application/json':
            TRequestHandler.send_error(400, 'Bad request')
            return

        content_length = int(TRequestHandler.headers['Content-Length'])
        body = TRequestHandler.rfile.read(content_length).decode('utf-8')
        try:
            request = json.loads(body)
            type = request['type']
            if type == 'run_tests':
                task = TestingTask(request['data']['code'], request['data']['options'], 
                                   request['data']['tests'], request['data']['verifier'], request['data']['response_type'])
                self.tasks[task.number] = task
                response = { 'status': 'added', 'token': task.number }  
                self.send_answer(TRequestHandler, response)
                task.start()
            elif type == 'update_status':
                num = request['token']
                if not num in self.tasks:
                    response = { 'status': 'not_found' }  
                else :
                    task = self.tasks[num]
                    # it's thread safety operation, don't need locks here
                    status = task.status
                    if status == 'finished' or status == 'failed':
                        response = { 'status' : status, 'result' : task.result}
                        self.tasks.pop(num, None)
                    else:
                        response = { 'status' : status }
                print(repr(response))
                self.send_answer(TRequestHandler, response)
            else:
                TRequestHandler.send_error(400, 'Bad request type')

        except json.JSONDecodeError as e:
            TRequestHandler.send_error(400, 'Bad JSON')
            print(e)
            print(body)
        except (AttributeError, KeyError) as e:
            TRequestHandler.send_error(400, 'Bad request')
            print(e)
            return
   
    def send_answer(self, request, response):
        request.send_response(200)
        request.end_headers()
        request.wfile.write(bytes(json.dumps(response), 'utf-8'))

