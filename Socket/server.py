from fileinput import filename
import socket
import sys
import errno

# "IP Address of the main server"
IP = "100.81.249.49"
PORT = 5589
ADDR = (IP, PORT)
SIZE = 10240000000
FORMAT = "utf-8"
from blockchain_main import execute_process
import time


def main():
    print("*[STARTING] The server is Starting")
    '''Starting the socket'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    'Bind the IP and PORT to the server'
    server.bind(ADDR)
    'Server is Listening, i.e, server is now waiting for the client to get connected.'
    server.listen()
    print(f'Listening to port {PORT}')
    while True:
        '''Accepting Connection from Client. '''
        conn, addr = server.accept()
        print(f"[New Connection] {addr} connected.")
        print("New Connection Started seeding file")
        # dat = conn.recv(512).decode(FORMAT)
        # print(dat)
        i = 0
        total_data = [];
        while True:
            print(f'Receiving Data Chunk {i}')
            data = conn.recv(512).decode(FORMAT)
            i += 1
            if data:
                total_data.append(data)
            else:
                break
        print("All Data Recieved")
        data = ''.join(total_data)
        execute_process(data)
        conn.close()
        print(f"Disconnected {addr} disconnected")


if __name__ == "__main__":
    main()
