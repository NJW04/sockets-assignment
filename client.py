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
    
def sendToFriend(socket,message,other_client_ip,other_client_port):
    socket.sendto(message.encode(FORMAT), (other_client_ip, other_client_port))
    

def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"Received from {addr}: {data.decode(FORMAT)}")
        except ConnectionResetError:
            break

def start_client():
    # Create a UDP socket
    client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_udp_socket,))
    receive_thread.start()

    # Send messages, this is the protocl section, so all the ifs for the msgs and stuff like JOIN for server and SEND for sending
    #JOIN <ip> <port> <visibility> <username>
    #SEND <name> <message>
    
    while True:
        msgToSend = input("Enter command (use !help): ")
        msgToSendArr = msgToSend.split(",")
        if len(msgToSendArr) == 1:
            if msgToSend == DISCONNECT_MESSAGE:
                sendToServer(msgToSend)
                break
            else:                   
                sendToServer(msgToSend)     #Only the 1 word commands that the server knows
        else:
            if msgToSendArr[0] == "SEND" and len(msgToSendArr == 3):    #add more protection here
                sendToServer(msgToSendArr[1])   #i.e Ben
                other_client_info = client_socket.recv(2048).decode(FORMAT) #this is receiving the IP and PORT number
                sendToFriend(client_udp_socket,','.join(msgToSendArr[2:]),other_client_info[0],other_client_info[1])    #JESUS FUCKING CHRIST CHECK THIS SHIT
            else:
                print(f"invalid command: {msgToSend}")
                

    # Close the socket
    client_udp_socket.close()
    
def joinCommand():
    joinCommand = "- - -"
    while len(joinCommand.split()) != 4 and joinCommand.split()[0] != "JOIN" and not joinCommand.split()[2].isnumeric():
        joinCommand = input("[Enter this command to join the server: JOIN <ip> <port> <username]: ")
    return joinCommand.lstrip()
    
    
#PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"
#SERVER = get_local_ip()
#ADDRESS = (SERVER,PORT)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    
try:
    clientInfo = joinCommand()
    clientInfoArr = clientInfo.split()   #[JOIN],[123.123.4.5],[5050],Nathan
    PORT = int(clientInfoArr[2])
    SERVER = clientInfoArr[1]
    ADDRESS = (SERVER,PORT)
    client_socket.connect(ADDRESS) #Client connecting to address of server
    sendToServer(clientInfo)
    start_client()
except (socket.error, socket.timeout) as e:
    print(f"Error: Unable to connect to the server. {e}")

finally:
    client_socket.close()

    
    

    
    