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
DISCONNECT_MESSAGE = "!DISCONNECT"

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #SOCK_STREAM is needed for TCP server
serverSocket.bind(ADDRESS)

#Array keeping the IP and Port number of all active clients
activeClients = []

def handleClient(connectionSocket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    activeClients.append(addr)  #Adds a tuple containing clients IP and port number
    connected = True
    while connected:
        msg = connectionSocket.recv(2048).decode(FORMAT)   #Number of bytes it receives, it blocks on this line until it receives
        if msg:
            if msg == DISCONNECT_MESSAGE:
                for clientInfo in activeClients:
                    if clientInfo == addr:
                        activeClients.remove(clientInfo)    #Removing the address from active clients
                break
            elif msg == "send":
                returnStr = "This is from the list of active clients:\n"
                for info in activeClients:
                    returnStr += f"{info} \n"   
                connectionSocket.send(returnStr.encode(FORMAT))
            else:
                connectionSocket.send((f"[{addr}] {msg} this is being sent back from the server").encode(FORMAT))
    
    connectionSocket.close()
        
    

def start():
    serverSocket.listen(1)    #waits for incoming TCP requests
    print(f"[LISTENING] server is listening on {SERVER}")
    print()
    
    while True:                 
        connectionSocket, addr = serverSocket.accept()  #Waits for a new connection, addr is storing the IP and port number it came from AND connectionSocket is a socket object which allows us to comunicate back to the thing that connected
        
        thread = threading.Thread(target=handleClient,args=(connectionSocket,addr)) #when a new connection occurs create a new thread to handle it
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")    #Always -1 because of this always True thread
        
                                                        

print("[STARTING] server is starting...")
start()
 