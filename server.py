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
DISCONNECT_MESSAGE = "!disconnect"

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #SOCK_STREAM is needed for TCP server
serverSocket.bind(ADDRESS)

#Array keeping the IP and Port number of all active clients, maybe turn this into dictionary which maps addr to online status
activeClients = []
activeClientsStatus = {}
activeClientsUsername = {}
help_message = "Available Commands:\n" \
                   "- !help: Display a list of available commands.\n" \
                   "- !list: Display a list of active clients.\n" \
                   "- message [recipientUsername] [content]: Send a message to another client.\n" \
                    "- !hide: Hide yourself to not appear to any other client\n" \
                    "- !active: Set yourself as active to be seen by other clients\n" \
                   "- !disconnect: Disconnect from the server.\n"

def handleClient(connectionSocket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    activeClients.append(addr)  #Adds a tuple containing clients IP and port number
    activeClientsStatus[addr] = "active"
    connected = True
    try:
        while connected:
            msg = connectionSocket.recv(2048).decode(FORMAT)   #Number of bytes it receives, it blocks on this line until it receives
            msgArr = msg.split()
            if msg:
                if msg == DISCONNECT_MESSAGE:
                    if addr in activeClients:
                        activeClients.remove(addr)     #Removing the address from active clients
                        connectionSocket.send("!disconnect".encode(FORMAT))
                    break
                elif msg[0:4] == "JOIN":
                    clientInfoArr = msg.split()
                    activeClientsUsername[clientInfoArr[3]] = addr
                    connectionSocket.send((f"\n{clientInfoArr[3]}, you have successfully joined the server").encode(FORMAT))
                elif msg == "!list":
                    returnStr = "This is the list of active clients:\n"
                    for key, value in activeClientsUsername.items():
                        if activeClientsStatus[value] == "active":
                            returnStr += (f"{key}: {value}\n")   
                    connectionSocket.send(returnStr.encode(FORMAT))
                elif msg == "!help":
                        connectionSocket.send(help_message.encode(FORMAT))
                elif msg == "!hide":
                    if not (activeClientsStatus[addr] == "hidden"):
                        activeClientsStatus[addr] = "hidden"
                        connectionSocket.send(f"You have been hidden {addr}".encode(FORMAT))
                elif msg == "!active":
                    if not (activeClientsStatus[addr] == "active"):
                        activeClientsStatus[addr] = "active"
                        connectionSocket.send(f"You are now active {addr}".encode(FORMAT))
                elif msgArr[1] in activeClientsUsername:
                    result_string = ' '.join(str(element) for element in activeClientsUsername[msgArr[1]])    # 192.123.3.8 42598, this returns this string
                    connectionSocket.send(result_string.encode(FORMAT)) #This is sending a string with a space of the IP and PORT
                else:
                    connectionSocket.send((f"Invalid Command: {msg}").encode(FORMAT))   #Send Nathan Hey
        
        connectionSocket.close()
    except ConnectionResetError:
        print("Connection reset by peer.")
        
    

def start():
    serverSocket.listen(1)    #waits for incoming TCP requests
    print(f"[LISTENING] server is listening on {SERVER}")
    print()
    
    try:
        while True:                 
            connectionSocket, addr = serverSocket.accept()  #Waits for a new connection, addr is storing the IP and port number it came from AND connectionSocket is a socket object which allows us to comunicate back to the thing that connected
            
            thread = threading.Thread(target=handleClient,args=(connectionSocket,addr)) #when a new connection occurs create a new thread to handle it
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")    #Always -1 because of this always True thread
    except  (socket.error, socket.timeout):
        print("Error error")
        
                                                        

print("[STARTING] server is starting...")
start()
 