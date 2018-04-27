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
        body = TRequestHandler.rfile.read(content_length)
        try:
            request = json.loads(body)
            if request['primary']:
                type = request['type']
                if type == 'run_tests':
                    task = TestingTask(request['data']['code'], request['data']['options'], 
                                       request['data']['tests'], request['data']['verifier'], request['data']['response_type'])
                    self.tasks[task.number] = task
                    response = { 'status': 'added', 'token': task.number, 'finished': False }  
                    self.send_answer(TRequestHandler, response)
                    task.start()
                else:
                    TRequestHandler.send_error(400, 'Bad request type')
            else:
                type = request['type']
                if type == 'update_status':
                    num = request['token']
                    if not num in self.tasks:
                        response = { 'status': 'not_found' }  
                    else :
                        task = self.tasks[num]
                        status = task.status
                        if status == 'finished' or status == 'failed':
                            response = { 'status' : status, 'result' : task.result, 'finished': True}
                            self.tasks.pop(num, None)
                        else:
                            response = { 'status' : status, 'finished' : False }
                    self.send_answer(TRequestHandler, response)
                else:
                    TRequestHandler.send_error(400, 'Bad request type')

        except json.JSONDecodeError as e:
            TRequestHandler.send_error(400, 'Bad JSON')
            print (e)
        except (AttributeError, KeyError) as e:
            TRequestHandler.send_error(400, 'Bad request')
            print(e)
            return
   
    def send_answer(self, request, response):
        request.send_response(200)
        request.end_headers()
        request.wfile.write(bytes(json.dumps(response), 'utf-8'))

