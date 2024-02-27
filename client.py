import socket
import threading
import re
import os

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
    
def sendToServerReturn(msg):
    client_socket.send(msg.encode(FORMAT))    #Encoding it to be sent to the server
    
    #Now to view the message sent from server back to client use
    return (client_socket.recv(2048).decode(FORMAT))
    
def sendToFriend(socket,message,other_client_ip,other_client_port):
    friendAddress = (other_client_ip,other_client_port)
    print(f"SENDING TO FRIENDS ADRESS:  {friendAddress}")
    socket.sendto(message.encode(FORMAT), friendAddress)
    

def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"Received from {addr}: {data.decode(FORMAT)}")
        except socket.error:
            print("THERE IS ERROR")
            break

def start_client(username):
    # Create a UDP socket
    client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_udp_socket.bind(('196.24.189.216',0))
    udpAddress, udpPort = client_udp_socket.getsockname()    #Different port and ip for udp socket
     
    sendToServer(f"UDP {udpAddress} {udpPort} {username}")  
    

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_udp_socket,))
    receive_thread.start()
    
    while True:
        msgToSend = input("Enter command (use !help): ")
        print()
        msgToSendArr = msgToSend.split(" ") #['SEND', 'Nathan','Hi,','howsit']
        if not msgToSend:
            print("Empty commnad")
        elif len(msgToSendArr) == 1:
            if msgToSend == DISCONNECT_MESSAGE:
                sendToServer(msgToSend)
                break
            else:                   
                sendToServer(msgToSend)     #Only the 1 word commands that the server knows
        else:
            if msgToSendArr[0] == "SEND":    #add more protection here
                matches = re.match(r'(\S+)\s+(\S+)\s+(.*)', msgToSend)
                if matches:
                    command = matches.group(1)
                    name = matches.group(2)
                    message = matches.group(3) + '\n'
                    print(name)
                    print(message)
        
                    other_client_info = sendToServerReturn(name)   #i.e Ben, this is receiving the IP and PORT number
                    print(f"Other client info: {other_client_info}")
                    other_client_info = other_client_info.split()
                    sendToFriend(client_udp_socket,message,other_client_info[0],int(other_client_info[1]))
                else:
                    print(f"invalid command: {msgToSend}")
                

    # Close the socket
    client_udp_socket.close()
    
def joinCommand():
    while True:
        user_input = input("[Enter this command to join the server: JOIN <ip> <port> <username]: " )

        # Split the input into words
        words = user_input.split()

        # Check if the input has exactly 4 words
        if len(words) == 4:
            # Check the first word is "JOIN"
            if words[0] == "JOIN":
                # Check the second word is in IP address format
                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', words[1]):
                    # Check the third word contains only digits
                    if words[2].isdigit():
                        break
                    else:
                        print("Invalid input. Third word must contain only digits.")
                else:
                    print("Invalid input. Second word must be in IP address format.")
            else:
                print("Invalid input. First word must be 'JOIN'.")
        else:
            print("Invalid input. Please enter a string with exactly 4 words separated by spaces.")
            
    return user_input.lstrip()
    
    
#PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"
#SERVER = get_local_ip()
#ADDRESS = (SERVER,PORT)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    

clientInfo = joinCommand()
clientInfoArr = clientInfo.split()   #[JOIN],[123.123.4.5],[5050],Nathan
PORT = int(clientInfoArr[2])
SERVER = clientInfoArr[1]
ADDRESS = (SERVER,PORT)
try:
    client_socket.connect(ADDRESS) #Client connecting to address of server
    sendToServer(clientInfo)
    start_client(clientInfoArr[3])
except (socket.error, socket.timeout) as e:
        print(f"Error: Unable to connect to the server. {e}")

finally:
        client_socket.close()

    
    

    
    