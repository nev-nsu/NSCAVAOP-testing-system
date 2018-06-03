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

class TApiCallHandler(IHandler):
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
            if type == 'sign_up':
                login = request['data']['login']
                password = request['data']['password']
                res = signup(login, password)
                if res:
                    response = {'status': 'success'}
                else:
                    response = {'status': 'failed'}
                send_answer(handler, response)
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

