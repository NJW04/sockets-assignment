import socket

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
    
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = get_local_ip()
ADDRESS = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS) #Client connecting to address of server

def send(msg):
    message = msg.encode(FORMAT)    #Encoding it to be sent to the server
    client.send(message)
    
    #Now to view the message sent from server back to client use
    print(client.recv(2048).decode(FORMAT))
    
send("Hello world!")
send(DISCONNECT_MESSAGE)