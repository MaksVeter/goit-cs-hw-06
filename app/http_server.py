import os
import json
import asyncio
import websockets
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'
HTTP_PORT = 3000
WEBSOCKET_SERVER = 'ws://127.0.0.1:5000'


class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = f'/{TEMPLATES_DIR}/index.html'
        elif self.path == '/message':
            self.path = f'/{TEMPLATES_DIR}/message.html'
        elif self.path.startswith('/static/'):
            self.path = self.path.lstrip('/')
        else:
            self.path = f'/{TEMPLATES_DIR}/error.html'
            self.send_response(404)

        return super().do_GET()

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)

            username = form_data.get('username', [''])[0]
            message = form_data.get('message', [''])[0]

            if username and message:
                asyncio.run(self.send_to_socket_server(username, message))
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Message sent!")
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Missing username or message!")
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Unsupported path!")

    async def send_to_socket_server(self, username, message):
        data = {
            'username': username,
            'message': message
        }

        try:
            async with websockets.connect(WEBSOCKET_SERVER) as websocket:
                await websocket.send(json.dumps(data))
        except Exception as e:
            print(f"Помилка при з'єднанні з сокет-сервером: {e}")


def run_http_server():
    server_address = ('', HTTP_PORT)
    httpd = HTTPServer(server_address, Handler)
    print(f"HTTP сервер запущений на порту {server_address[1]}")
    httpd.serve_forever()


if __name__ == '__main__':
    run_http_server()
