import socket
import threading
import socketserver
from pathlib import Path
import os
import sys
import binascii
from datetime import datetime

# global HOST
global PORT


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        binary_field = bytearray(data)
        print(data.decode("UTF-8"))
        # mi_string = binascii.hexlify(binary_field).decode("UTF-8")
        # print("data of my server is %s",mi_string)
        # # ####################################################
        #   Paquete e
        # ####################################################

        file=open("logfile.txt","r")
        word=file.read()
        file.close()    
        mensaje=str(word)
   
        # packed_data_2 = bytearray()
        # packed_data_2 += value2.to_bytes(1, "big")
        # socket.sendto(packed_data_2, self.client_address)
        try:
            socket.sendto(mensaje.encode("UTF-8"), self.client_address)
            print(data.decode("UTF-8"))
        except:
            print("error send message")

if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 9999
        with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
            server.serve_forever()
    except:
           print("error creating socket")