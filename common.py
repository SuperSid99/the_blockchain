import socket
from constants import WHITELISTED_CLIENT_IPS
import json

MAIN_SERVER_IP = ""
MAIN_SERVER_PORT = ""
IP = "client IP"
PORT = "CLIENT Port"
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000


def get_data_by_chunks(conn):
    i = 0
    total_data = []
    while True:
        print(f'Receiving Data Chunk {i}')
        data = conn.recv(100).decode(FORMAT)
        i += 1
        if data :
            total_data.append(data)
        # elif data.split(" ")[1]=="END":
        #     print("END Recieved")
        #     break
        else:
            break
        print(data)
    return total_data


def chunks(lst, n):
    """Yield successive n-sized chunks from lst"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_node_hash_data(file_path):
    with open(file_path) as hashes_file:
        machine_blockchain = json.load(hashes_file)
        return machine_blockchain


def get_key_by_addr(addr, lst):
    for _ in lst:
        if _[0] == addr:
            return _[1]

    return ValueError("No Key Found")


def connect(addr):
    print(addr)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    print(conn)
    conn.connect(addr)
    return conn



def save_node_blk_data(conn):
    data = get_data_by_chunks(conn)
    print("All Data Received")
    data = ''.join(data)
    execute_node_process(data)
    conn.close()
    # print(f"Disconnected {addr} disconnected")


def get_client_key_by_addr(addr):
    for _ in WHITELISTED_CLIENT_IPS:
        if _[0] == addr:
            return _[2]
    return ValueError("No key Found")

