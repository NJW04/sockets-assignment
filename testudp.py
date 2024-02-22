import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"Received from {addr}: {data.decode('utf-8')}")
        except ConnectionResetError:
            break

def start_client():
    # Get the IP address and port number of the other client
    other_client_ip = input("Enter the other client's IP address: ")
    other_client_port = int(input("Enter the other client's port number: "))

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific port (optional)
    #client_socket.bind(("0.0.0.0", 0))

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Send messages to the other client
    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client_socket.sendto(message.encode('utf-8'), (other_client_ip, other_client_port))

    # Close the socket
    client_socket.close()


start_client()