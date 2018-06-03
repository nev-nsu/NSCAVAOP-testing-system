#!/usr/bin/python

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from jinja2 import Template
import metas
from config import SConfig
from api.api_proxy import SApiProxy
from kernel.thread_pool import SThreadPool


class TRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_GET(self):
        self.path = self.path.strip('?')
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
                    data = file.read()
            elif self.path.startswith('/dynamic'):
                params = self.path.split('/')
                path = SConfig().DYNAMIC_PATH + os.sep + params[2] + '.template'
                print(path)
                with open(path, 'r') as file:
                    template_text = file.read()
                    template = Template(template_text)
                    data = template.render({'p':params[3]}).encode('utf-8')
            else:
                self.send_error(415, 'Unsupported Media Type')
                return

            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', len(data))
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(data)

        except IOError:
            self.send_error(404, 'File Not Found: ' + self.path)
        except BrokenPipeError:
            print(str(e))
        except Exception as e:
            self.send_error(500, 'Internal Server Error')
            print(str(e))

    def do_POST(self):
        try:
            print(str(repr))
            if self.path.startswith('/api'):
                SApiProxy().handle(self.path, self)
            else:
                self.send_error(404, 'File Not Found: ' + self.path)
        except BrokenPipeError as e:
            print(str(e))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class STestingServer(metaclass=metas.Singleton):
    def __init__(self):
        if not os.path.exists(SConfig().TEMP_DIR):
            os.mkdir(SConfig().TEMP_DIR)
        self.server = ThreadedHTTPServer(('', SConfig().DEFAULT_PORT), TRequestHandler)

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
