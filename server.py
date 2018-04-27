#!/usr/bin/python

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import config
from api.api import ApiProxy

api_proxy = ApiProxy()

class TRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path += config.DEFAULT_PAGE
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
                f = open(config.STATIC_PATH + os.sep + self.path, 'rb') 
                self.send_response(200)
                self.send_header('Content-type', mime_type)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            else:
                self.send_error(415, 'Unsupported Media Type')

        except IOError:
            self.send_error(404, 'File Not Found: ' + self.path)
        except Exception as e:
            self.send_error(500, 'Internal Server Error')
            print(str(e))

    def do_POST(self):
        if self.path.startswith('/api'):
            api_proxy.handle(self.path, self)
        else:
            self.send_error(404, 'File Not Found: ' + self.path)

if __name__ == '__main__':
    try:
        server = HTTPServer(('', config.DEFAULT_PORT), TRequestHandler)
        print('Started on port', config.DEFAULT_PORT)
        server.serve_forever()

    except KeyboardInterrupt:
        print('Shutting down the server...')
    except Exception as e:
        print(str(e))
        print("Aborted")

    server.socket.close()
