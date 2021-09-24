# coding: utf-8 
import socketserver
import os
import os.path

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

# Copyright 2021 Ava Guo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class MyWebServer(socketserver.BaseRequestHandler):
    
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
                sub_components = component.split(" ")
                if len(sub_components) < 2:
                    continue
                data_dict[sub_components[0]] = sub_components[1]
            else:
                sub_components = component.split(": ")
                data_dict[sub_components[0]] = sub_components[1]
        
        response = ''
        if "GET" in data_dict:
            path = "www" + data_dict['GET']
            if os.path.isdir(path) and path[-1] != "/":
                # append ending "/" sign
                path += "/"
            if len(path) >= 1 and path[-1] == "/":
                path += "index.html"
            
            # search url in folder
            if "../" not in path and os.path.exists(path):
                # file found - open file
                file = open(path, mode = 'r')
                response = "HTTP/1.1 200 OK\r\n"  # response header
                file_type = path.split(".")[1]        
                response += "Content-type: text/" + file_type + "\r\n"
                response += "\r\n"
                response += file.read()  # response body
                file.close()
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
