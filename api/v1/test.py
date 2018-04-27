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
            if request.primary == True:
                type = request.type
                if type == 'run_tests':
                    task = TestingTask(request.data.code, request.data.options, 
                                       request.data.tests, request.data.verifier, request.data.respnonce_type)
                    self.tasks[task.number] = task
                    responce = { 'status': 'added', 'token': task.number, 'finished': False }  
                    self.send_answer(TRequestHandler, responce)
                    task.start()
                elif type == 'update_status':
                    num = request.token
                    if not num in self.tasks:
                        responce = { 'status': 'not_found' }  
                    else :
                        task = self.tasks[num]
                        status = task.status
                        if status == 'finished' or status == 'failed':
                            responce = { 'status' : status, 'result' : task.result, 'finished': True}
                            self.tasks.pop(num, None)
                        else:
                            responce = { 'status' : status, 'finished' : False }
                    self.send_answer(TRequestHandler, responce)
                else:
                    TRequestHandler.send_error(400, 'Bad request')

        except (json.JSONDecodeError, AttributeError):
            TRequestHandler.send_error(400, 'Bad request')
            return
   
    def send_answer(self, request, responce):
        request.send_response(200)
        request.end_headers()
        request.wfile.write(bytes(json.dumps(responce), 'utf-8'))

