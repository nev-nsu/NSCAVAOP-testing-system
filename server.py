#!/usr/bin/python

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import metas
from config import SConfig
from api.api_proxy import SApiProxy
from kernel.thread_pool import SThreadPool


class TRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path += SConfig().DEFAULT_PAGE
        try:
            mime_type = ''
            type_supported = True

            if self.path.endswith('.html'):
                mime_type = 'text/html'
            elif self.path.endswith('.jpg'):
                mime_type = 'image/jpg'
            elif self.path.endswith('.ico'):
                mime_type = 'image/x-icon'
            elif self.path.endswith('.js'):
                mime_type = 'application/javascript'
            elif self.path.endswith('.css'):
                mime_type = 'text/css'
            else:
                type_supported = False

            if type_supported:
                with open(SConfig().STATIC_PATH + os.sep + self.path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', mime_type)
                    self.end_headers()
                    self.wfile.write(file.read())
            else:
                self.send_error(415, 'Unsupported Media Type')

        except IOError:
            self.send_error(404, 'File Not Found: ' + self.path)
        except Exception as e:
            self.send_error(500, 'Internal Server Error')
            print(str(e))

    def do_POST(self):
        if self.path.startswith('/api'):
            SApiProxy().handle(self.path, self)
        else:
            self.send_error(404, 'File Not Found: ' + self.path)


class STestingServer(metaclass=metas.Singleton):
    def __init__(self):
        if not os.path.exists(SConfig().TEMP_DIR):
            os.mkdir(SConfig().TEMP_DIR)
        self.server = HTTPServer(('', SConfig().DEFAULT_PORT), TRequestHandler)

    def start(self):
        print('Started on port', SConfig().DEFAULT_PORT)
        self.server.serve_forever()

    def stop(self):
        self.server.socket.close()


if __name__ == '__main__':
    try:
        STestingServer().start()
    except KeyboardInterrupt:
        print('Shutting down the server...')
    except Exception as e:
        print(str(e))
        print("Aborted")

    STestingServer().stop()
    SThreadPool().terminate()
