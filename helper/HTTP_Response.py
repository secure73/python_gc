from http.server import BaseHTTPRequestHandler
import json
class HTTP_Response(BaseHTTPRequestHandler):
    def _response(self, status_code, data):
        """Send JSON response"""
        self.send_header('Content-Type', 'application/json')
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def success(self,data):
        self._response(200,data=data)
    
    def badRequest(self,data):
        self._response(400,data=data)
    
    def unauthorize(self,message: str):
        self._response(401,message)

    