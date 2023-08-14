''' Peer Class
    Computer Networking
    (c)2023 Brett Huffman
    To test, in two different console windows start
    different versions (with different File_PATH and 
    SEND/RECV_PORTS).  Will also work across machines.
'''
import socket
import time
from Peer import *

# Configuration
FILE_PATH = "folder1/"
HOST = "127.0.0.1"
SEND_PORT = 12345
RECV_PORT = 12346

# MAIN
if __name__ == "__main__":
    peer = Peer(HOST, RECV_PORT, FILE_PATH)

    # Loop until user selects quit (Q)
    while True:
        # Quick sleep to have menu show correctly
        time.sleep(0.01)
        print('-------------------')
        print("1 List shared files")
        print("q: Quit")
        choice = input("Enter Choice: ")

        if choice == "1":
            # In this case, call the remote server and show returned files
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, SEND_PORT))
                client_socket.send("list".encode())
                file_list = client_socket.recv(1024).decode()
                print("\nShared files:")
                print(file_list)
                print()
        elif choice == 'q':
            # Friendly shutdown of local service
            peer.disconnect()
            break
