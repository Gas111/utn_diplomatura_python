import socket
import sys
import binascii

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    print("error socket")
# ################################################333
print("Sending Request for all data on LogFileDatabase")
mensaje = "Request All Data Register File"
try:
    sock.sendto(mensaje.encode("UTF-8"), (HOST, PORT))
    received = sock.recvfrom(1024)
    msg=str(received)
except:
    print("send and receive")
# ===== ENVIO Y RECEPCIÓN DE DATOS =================
 
print(msg)
# ===== FIN ENVIO Y RECEPCIÓN DE DATOS =================