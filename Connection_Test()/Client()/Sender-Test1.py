import socket
import os
from tqdm import tqdm

# Host laptop's IP address and port for socket communication
host_ip = "192.168.98.202"  # Loopback address for testing on the same system
port = 12345  # Choose the same port number as the server

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#0
# Connect to the host
client_socket.connect((host_ip, port))

# Send a file to the server
file_path = "Short.rar"  # Replace with the path to the .rar file you want to send
file_size = os.path.getsize(file_path)

# Send the file size to the server
client_socket.send(str(file_size).encode())

# Send the file data to the server with a progress bar
try:
    with open(file_path, "rb") as file:
        progress_bar = tqdm(total=file_size, unit="B", unit_scale=True)
        file_data = file.read(1024)
        while file_data:
            client_socket.send(file_data)
            progress_bar.update(len(file_data))
            file_data = file.read(1024)

        # Send a message indicating file transfer is complete
        client_socket.send(b"FILE_TRANSFER_COMPLETE")
        progress_bar.close()
except Exception as e:
    print(f"Error sending file data: {e}")

print("File sent successfully.")

# Close the connection
client_socket.close()