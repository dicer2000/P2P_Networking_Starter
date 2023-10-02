
''' Peer Class
    Computer Networking
    (c)2023 Brett Huffman
'''
import threading
import socket
import glob

class Peer:
    ''' Peer class to handle all Peer connection logic '''
    def __init__(self, host, port, filepath):
        # Initialization
        self.host = host
        self.port = port
        self.filepath = filepath
        self.files = []  # List to store shared files
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def run_server(self):
        ''' Start the server running
        Create a server socket to receive connections'''
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True  # Flag to control the server thread

        print(f"\nServer listening on {self.host}:{self.port}\n")

        try:
            while self.running:
                # When a connection is received, put it onto a seperate
                # thread for handling.  Then recycle to get more connections
                client_socket, _ = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except OSError:
            pass  # The server socket has been closed

    def handle_client(self, client_socket):
        '''# Handle client requests'''
        request = client_socket.recv(1024).decode()

        if request == "list":
            self.send_file_list(client_socket)
        else:
            client_socket.send("Invalid request".encode())

        client_socket.close()

    def send_file_list(self, client_socket):
        ''' Send a file list '''
        print('\n * Sending file list *')
        file_list = ''
        files = glob.glob(self.filepath + '*.*')
        file_list = "\n".join(files)
        client_socket.send(file_list.encode())

    def disconnect(self):
        ''' Handle disconnects gracefully
        Stop the server thread and clean up resources'''
        self.running = False
        self.server_socket.close()
        # Wait for the server thread to finish
        self.server_thread.join()
