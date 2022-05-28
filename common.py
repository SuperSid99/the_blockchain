from blk_client import execute_process
from image import decyript_image

import json

MAIN_SERVER_IP = ""
MAIN_SERVER_PORT = ""
IP = "client IP"
PORT = "CLIENT Port"
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000



def get_hash_data(file_path):
    with open(file_path) as hashes_file:
        machine_blockchain = json.load(hashes_file)
        return machine_blockchain


def save_blk_data(conn):
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
    # print(f"Disconnected {addr} disconnected")

