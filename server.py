import string
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from sys import argv
import re
import os
import threading

# define a function to handle each client connection
def handle_client(connectionSocket, addr):
    try:
        # log the accepted connection
        print("SERVER: connection from " + addr[0] + " accepted")

        # receive a message from the client
        message = connectionSocket.recv(4096).decode()

        # check if the message is empty, indicating a client disconnect
        if not message:
            print("SERVER: " + addr[0] + " has disconnected")
            return

        # extract the filename from the received GET request using regex
        filename = re.search(r"GET /(.*?) ", message).group(1)

        # check if the requested file exists
        if os.path.exists(filename):
            # read the file and send it back to the client with a 200 OK response
            with open(filename, 'rb') as f:
                data = f.read(4096)
                connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n" + data)
                print(f"SERVER: sent {filename} to " + addr[0])
        else:
            # send a 404 Not Found response if the file doesn't exist
            connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            print("SERVER: unable to find file: " + filename)
    except:
        # close the connection in case of any exceptions
        connectionSocket.close()


# get the maximum number of connections and the server port from command-line arguments
max_connections = argv[2]
serverPort = argv[1]

# initialize the server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# bind the server socket to the specified port
serverSocket.bind(("", int(serverPort)))

# log the start of the server
print("SERVER: server started on port: ", serverPort)

# set the server socket to listen mode with the specified maximum connections
serverSocket.listen(int(max_connections))

# main server loop to accept and handle client connections
while True:
    try:
        # accept a new client connection
        connectionSocket, addr = serverSocket.accept()

        # start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()
    except Exception as e:
        # log any exceptions that occur while accepting a connection
        print("SERVER: an error occurred while accepting a connection:", e)

# close the server socket when the server is stopped
serverSocket.close()
