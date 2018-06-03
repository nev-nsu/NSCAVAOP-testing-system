import json
from api.handler import IHandler
from kernel.testing_task import TTestingTask
from db.query import *
from db.connection import *

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
            if type == 'check_sid':
                sid = request['sid']
                expired = check_expired(sid)
                response = {'status': 'success', 'result': not expired}
                send_answer(handler, response)
            elif type == 'get_projects':
                sid = request['sid']
                res = get_projects(sid)
                if not res:
                    response = {'status': 'nothing to show'}
                else:
                    response = {'status':'success', 'data': res}
                send_answer(handler, response)
            elif type == 'project_info':
                sid = request['sid']
                pid = request['pid']
                res = load_project(sid, pid)
                if not res:
                    response = {'status': 'failed'}
                else:
                    response = {'status':'success', 'data': res}
                send_answer(handler, response)
            elif type == 'get_olymps_author':
                res = load_olymps_as_author(request['sid'])
                print(res)
                if not res:
                    response = {'status': 'nothing to show'}
                else:
                    response = {'status':'success', 'data': res}
                send_answer(handler, response)
            elif type == 'get_olymps_part':
                res = load_olymps_as_user(request['sid'])
                print(res)
                if not res:
                    response = {'status': 'nothing to show'}
                else:
                    response = {'status':'success', 'data': res}
                send_answer(handler, response)
            elif type == 'get_olymps_open':
                res = load_olymps_open()
                print(res)
                if not res:
                    response = {'status': 'nothing to show'}
                else:
                    response = {'status':'success', 'data': res}
                send_answer(handler, response)
            elif type == 'olymp_info':
                tryRegister(request['sid'], request['oid'])
                res = loadOlymp(request['sid'], request['oid'])
                print(res)
                if not res:
                    response = {'status': 'nothing to show'}
                else:
                    response = {'status':'success', 'data': res}
                send_answer(handler, response)
            elif type == "get_tasks_from_olymp":
                with SConnection().__lock__:
                    res = SConnection().__get_tasks__(int(request['oid']))
                if not res:
                    response = {'status': 'nothing to show'}
                else:
                    response = {'status':'success', 'data': res}
                send_answer(handler, response)
            elif type == "get_tests_for_parsing":
                with SConnection().__lock__:
                    res = SConnection().__get_tests__(int(request['tid']))
                if not res:
                    response = {'status': 'nothing to show'}
                else:
                    response = {'status':'success', 'data': res}
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
