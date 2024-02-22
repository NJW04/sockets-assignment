import socket
import threading

def get_local_ip():
    try:
        # Create a socket object and connect to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return "Unable to determine IP address"

def sendToServer(msg):
    client_socket.send(msg.encode(FORMAT))    #Encoding it to be sent to the server
    
    #Now to view the message sent from server back to client use
    print(client_socket.recv(2048).decode(FORMAT))
    
    
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = get_local_ip()
ADDRESS = (SERVER,PORT)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    
try:
   client_socket.connect(ADDRESS) #Client connecting to address of server
   
   while True:
    msgToSend = input("What do you want to send to the server: ")
    if msgToSend == "exit":
        break
    else:
        sendToServer(msgToSend)

except (socket.error, socket.timeout) as e:
    print(f"Error: Unable to connect to the server. {e}")

finally:
    client_socket.close()
    
    