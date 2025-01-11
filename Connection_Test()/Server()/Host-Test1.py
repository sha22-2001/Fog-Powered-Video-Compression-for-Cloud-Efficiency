import socket

# Host laptop's IP address and port for socket communication
host_ip = "127.0.0.1"  # Loopback address for testing on the same system
port = 12345  # Choose a port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host_ip, port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on port {port}...")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # Receive and save a file from the client
    try:
        file_size = client_socket.recv(1024).decode(errors='ignore')
        if file_size.isdigit():
            file_size = int(file_size)
            file_data = b""

            while len(file_data) < file_size:
                data = client_socket.recv(1024)
                if not data:
                    break
                file_data += data

            # Save the received file
            with open("Short_received.rar", "wb") as file:
                file.write(file_data)

            print("File received and saved.")
    except Exception as e:
        print(f"Error receiving file: {e}")

    # Close the connection with the current client
    print(f"Connection with {client_address} closed.")
    client_socket.close()
