from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from sys import argv

# defining server port and IP
serverIP = '127.0.0.1'
serverPort = argv[1]

# initializing the socket and connection to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, int(serverPort)))
print("CLIENT: connection established.")

# using some formatting to pull the filename from the arguments, as well as the server IP
requestToSend = f"GET /{argv[2]} HTTP/1.1\r\nHost: {serverIP}\r\n\r\n".encode()
# seconding the GET request to the server, encoded as bytes
clientSocket.send(requestToSend)
# listening for the server's response as bytes and decoding the data
response = clientSocket.recv(4096).decode()
data = response.split("HTTP/1.1 200 OK\r\n\r\n")

# should the file be found, the header code will be 200 OK, we then write the file and save it
if "200 OK" in response:
    with open(argv[2], 'w') as f:
        f.write(data[1])
# if unsuccessful, display an error message
elif "404 Not Found" in response:
    print("CLIENT: server unable to find file: " + argv[2])

# remembering to close the connection after finishing
clientSocket.close()