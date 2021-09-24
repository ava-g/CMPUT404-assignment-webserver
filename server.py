#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


# global dictionary to store served file contents
files = {}
files["base.css"] = \
'''
h1 {
    color:orange;
    text-align:center;
}
'''
files["index.html"] = \
'''
<!DOCTYPE html>
<html>
<head>
    <title>Example Page</title>
        <meta http-equiv="Content-Type"
        content="text/html;charset=utf-8"/>
        <!-- check conformance at http://validator.w3.org/check -->
        <link rel="stylesheet" type="text/css" href="base.css">
</head>

<body>
    <div class="eg">
        <h1>An Example Page</h1>
        <ul>
            <li>It works?
                        <li><a href="deep/index.html">A deeper page</a></li>
        </ul>
    </div>
</body>
</html> 
'''
files["deep/deep.css"] = \
'''
h1 {
    color:green;
    text-align:center;
}
'''
files["deep/index.html"] = \
'''
<!DOCTYPE html>
<html>
<head>
    <title>Deeper Example Page</title>
        <meta http-equiv="Content-Type"
        content="text/html;charset=utf-8"/>
        <!-- check conformance at http://validator.w3.org/check -->
        <link rel="stylesheet" type="text/css" href="deep.css">
</head>

<body>
    <div class="eg">
        <h1>An Example of a Deeper Page</h1>
        <ul>
            <li>It works?</li>
                        <li><a href="../index.html">A page below!</a></li>
        </ul>
    </div>
</body>
</html>
'''
class MyWebServer(socketserver.BaseRequestHandler):
    '''def __init__(self, request, client_address, server):
        self.base = os.path.realpath("./www")
        super().__init__(request, client_address, server)
    '''
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print("type(self.data): ", type(self.data))
        #print("dir(self.data): ", dir(self.data))
        print ("Got a request of: %s\n" % self.data)
        # process string
        components = self.data.decode("utf-8").split("\r\n")
        #print("components: ", components)
        data_dict = {}  # extract info from data string
        for component in components:
            if component.find(": ") == -1:  # extract request type
                sub_components = component.split(" /")
                if len(sub_components) < 2:
                    continue
                data_dict[sub_components[0]] = sub_components[1].split(" ")
            else:
                sub_components = component.split(": ")
                data_dict[sub_components[0]] = sub_components[1]
        
        response = ''
        if "GET" in data_dict:
            path = data_dict['GET'][0]
            if path == "":
                path += "index.html"
            
            # if url is in served files
            if path in files:
                response = "HTTP/1.1 200 OK\r\n"  # response header
                file_type = path.split(".")[-1]        
                response += "Content-type: text/" + file_type + "\r\n"
                response += "\r\n"
                response += files[path]  # response body
            else:
                response = "HTTP/1.1 404 Not Found\r\n"  # response header
        else:
            # 405 error in case of other request methods
            response = "HTTP/1.1 405 Method Not Allowed\r\n"  # header
        
        self.request.sendall(bytearray(response,'utf-8'))  # send http response
        print("Response sent.")    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
