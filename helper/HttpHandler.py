import json
import importlib
from http.server import BaseHTTPRequestHandler, HTTPServer
"""
Note:This class is not suitable for production.
It is designed solely for educational purposes to demonstrate how HTTP requests work. 
There are several areas that could be cleaner, more optimized, and more secure for a production-level application.
This class is intended for beginners to understand the HTTP request lifecycle 
-and gain insights into how robust frameworks like Flask and Django handle requests efficiently.
"""
class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests"""
        self._handle_request("GET")

    def do_POST(self):
        """Handle POST requests"""
        self._handle_request("POST")

    def do_PUT(self):
        """Handle PUT requests"""
        self._handle_request("PUT")

    #def do_DELETE(self):
     #   """Handle DELETE requests"""
      #  self._handle_request("DELETE")

    def _handle_request(self, method_HTTP):
        controller_name, method_name = self._validateRequestParts()
        try:
            controller_instance = self._createInstance(controller_name)
            method_to_call = self._createMethod(controller_instance,method_name)
            data = self._load_data(method_HTTP)
            #response = method_to_call(data) if method_HTTP in ["POST", "PUT"] else method_to_call()
            #self._response(200,result)
            method_to_call(data) if method_HTTP in ["POST", "PUT"] else method_to_call()
       
        except Exception as e:
            self._response(500, {"error": str(e)})

    def _validateRequestParts(self):
        """Dynamically route requests to the correct controller and method"""
        # z.B: /user/get
        path_parts = self.path.strip('/').split('/')  
        #[user,get]
        if len(path_parts) < 2:
           return self._response(400, {"error": "Invalid request. Use /Controller/Method"})
        controller_name, method_name = path_parts[:2] 
        controller_name = controller_name.capitalize() # user => User
        controller_name = controller_name+"Controller" #=> User => UserController
        return controller_name, method_name
    
    def _createInstance(self,controller_name:str)->object:
            try:
                module = importlib.import_module(f'controller.{controller_name}')  # Import controller.UserController
                controller_class = getattr(module, controller_name)  # Get class
                controller_instance = controller_class()  # Instantiate controller = UserController()
                return controller_instance
            except ImportError:
                self._response({"internal": ImportError.msg})

    def _createMethod(self,controller_insance_to_run:object,method_name_to_create:str):
        if not hasattr(controller_insance_to_run, method_name_to_create):
                self._response(404, {"error": f"Method '{method_name_to_create}' not found in {type(controller_insance_to_run).__name__}"})
                return

        return getattr(controller_insance_to_run, method_name_to_create)  # z.B Get method get

    def _load_data(self,HTTP_method)->None|object:
            if HTTP_method in ["POST", "PUT"]:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode('utf-8')
                try:
                    return json.loads(post_data)
                except json.JSONDecodeError:
                    self._response(400, {"error": "Invalid JSON format"})
                    return
            return None



def run(server_class=HTTPServer, handler_class=HttpHandler, port=8001):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

