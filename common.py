from blockchain_main import execute_node_process
from image import decyript_image

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
        data = conn.recv(512).decode(FORMAT)
        i += 1
        if data:
            total_data.append(data)
        else:
            break
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
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    conn.connect(addr)
    return conn


def save_node_blk_data(conn):
    data = get_data_by_chunks(conn)
    print("All Data Received")
    execute_node_process(data)
    conn.close()
    # print(f"Disconnected {addr} disconnected")

