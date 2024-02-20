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

PORT = 5050
SERVER = get_local_ip() #Instead of hard coding in the IP Address this gets the IP Address of local machines
#SERVER = "196.24.190.87"
ADDRESS = (SERVER,PORT) #This is the exact address with matching IP and Port number for the server
FORMAT = 'utf-8'

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #SOCK_STREAM is needed for TCP server
serverSocket.bind(ADDRESS)

#DELVING INTO MY OWN THINKING
activeClients = []  #My thinking is to have this array hold all of the active socket client objects so if someone wants to request to see we have it
#Maybe rather have a dictionary which maps the IP address of the client with their name for the chatting function and stuff

def handleClient(connectionSocket, addr): #I think 
    print(f"[NEW CONNECTION] IP: {addr} connected.")
    connected = True
    while connected:
        msg = connectionSocket.recv(1024).decode(FORMAT)   #Number of bytes it receives
    

def start():
    serverSocket.listen(1)    #waits for incoming TCP requests
    while True:                 
        connectionSocket, addr = serverSocket.accept()  #Waits for a new connection, addr is storing the IP and port number it came from AND connectionSocket is a socket object which allows us to comunicate back to the thing that connected
        
        activeClients.append(connectionSocket)  #NOT SURE ABOUT THIS
        
        thread = threading.Thread(target=handleClient,args=(connectionSocket,addr)) #when a new connection occurs create a new thread to handle it
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount-1}")    #Always -1 because of this always True thread
        
                                                        

print("[STARTING] server is starting...")
start()
 