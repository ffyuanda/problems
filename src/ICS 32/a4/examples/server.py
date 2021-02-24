import http, socketserver
from http import server

"""
This is a subclass of the BaseHTTPRequestHandler class which provdies methods
for various aspects of HTTP request management. Since our only goal is to 
show how POST data works, this class simply renders and prints data when a 
POST request is received.
"""
class ICSHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print(self.command + " received.")
        data = self.rfile.read(int(self.headers['content-length']))
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write("ok".encode(encoding = 'utf-8'))
        print(data.decode(encoding = 'utf-8'))


"""
This is just basic startup code to run the TCPServer that accompanies
the Python standard library.
"""
PORT = 8000

handler = ICSHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)

print ("serving at port", PORT)
httpd.serve_forever()