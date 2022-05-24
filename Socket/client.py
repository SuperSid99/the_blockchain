from ..blockchain_main import execute_process
import threading
import socket
import json

IP = "client IP"
PORT = "CLIENT Port"
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000


global conn
global addr
global server


# This function will open up a port of listener(with given IP) for the client to recieve the data files
def initiate_socket_listener():
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        'Bind the IP and PORT to the server'
        server.bind(ADDR)
        'Server is Listening, i.e, server is now waiting for the client to get connected.'
        server.listen()
        '''Accepting Connection from Client. '''
        conn, addr = server.accept()
        server.setblocking(1)
        print(f"[New Connection] {addr} connected.")
        print("New Connection Started seeding file")
        func = conn.recv(512).decode(FORMAT)

        if func == 'save_blk_data':
            save_blk_data()
        elif func == 'verify_chain':
            verify_chain()
        else:
            conn.close()


def save_blk_data():
    i = 0
    total_data = []
    while True:
        print(f'Receiving Data Chunk {i}')
        data = conn.recv(512).decode(FORMAT)
        i += 1
        if data:
            total_data.append(data)
        else:
            break
    print("All Data Received")
    data = ''.join(total_data)
    execute_process(data)
    conn.close()
    print(f"Disconnected {addr} disconnected")


def verify_data_with_machine_blockchain(main_server_hash_dict):
    with open('/home/vishwajeet/Travclan/BLK/the_blockchain/hashes.json') as hashes_file:
        machine_blockchain = json.load(hashes_file)
        return 1 if main_server_hash_dict == machine_blockchain else 0


def verify_chain():
    main_server_hash_dict = conn.recv(SIZE).decode(FORMAT)
    conn.send(verify_data_with_machine_blockchain(main_server_hash_dict).encode(FORMAT))


if __name__ == "__main__":
    t1 = threading.Thread(target=initiate_socket_listener)
    t1.daemon = True
    t1.start()

    print("T1 thread Started for Receiving Data from Main server")
