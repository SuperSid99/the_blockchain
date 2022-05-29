# from fileinput import filename
# import socket
# import sys
# import errno
#
# IP = "100.81.249.49"
# PORT = 5589
# ADDR = (IP, PORT)
# SIZE = 10240000000
# FORMAT = "utf-8"
# from blockchain_main import execute_process
# import time
#
#
# def main():
#     print("*[STARTING] The server is Starting")
#     '''Starting the socket'''
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     'Bind the IP and PORT to the server'
#     server.bind(ADDR)
#     'Server is Listening, i.e, server is now waiting for the client to get connected.'
#     server.listen()
#     print(f'Listening to port {PORT}')
#     while True:
#         '''Accepting Connection from Client. '''
#         conn, addr = server.accept()
#         print(f"[New Connection] {addr} connected.")
#         print("New Connection Started seeding file")
#         # dat = conn.recv(512).decode(FORMAT)
#         # print(dat)
#         i = 0
#         total_data = [];
#         while True:
#             print(f'Receiving Data Chunk {i}')
#             data = conn.recv(512).decode(FORMAT)
#             i += 1
#             if data:
#                 total_data.append(data)
#             else:
#                 break
#         print("All Data Recieved")
#         data = ''.join(total_data)
#         execute_process(data)
#         conn.close()
#         print(f"Disconnected {addr} disconnected")
#
#
# if __name__ == "__main__":
#     main()

from fileinput import filename
import socket
import sys
import json
import errno
from blockchain_main import execute_process
import time
from image import decyript_image, give_encyripted_image
from common import chunks, get_data_by_chunks, get_key_by_addr, connect, get_node_hash_data, get_client_key_by_addr
from constants import NODES, CAMERA_MODULES_IPS, WHITELISTED_CLIENT_IPS
from write_to_json import get_image_data

# "IP Address of the main server"
IP = "100.81.249.49"
PORT = 5589
ADDR = (IP, PORT)
SIZE = 10240000000
FORMAT = "utf-8"
MAIN_SERVER_KEY = ""


def get_decrypted_data_of_camera_module(addr, data):
    key = get_key_by_addr(addr, CAMERA_MODULES_IPS)
    decrypted_image_data = decyript_image(data, key)
    return decrypted_image_data


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

        func = conn.recv(SIZE).decode(FORMAT)

        if func == "camera":
            total_data = get_data_by_chunks(conn)
            print("Receiving Data from Camera Module")
            data = ''.join(total_data)
            '''Now Decrypt image from Camera Module'''
            decrypted_data_from_camera_module = get_decrypted_data_of_camera_module(addr, data)
            if verify_chain():
                final_encrypted_data = give_encyripted_image(decrypted_data_from_camera_module)
                processed_block = execute_process(final_encrypted_data)
                send_blk_data_to_machines(processed_block)
            else:
                print("Block Chain is Corrupted")
            print(f"Disconnected {addr} disconnected")
        elif func == "authenticate":
            flag = authenticate(addr)
            conn.send(flag.encode(FORMAT))
        elif func == "get_hash_data":
            hashes_data = get_node_hash_data("file/path/to/be/added")
            print("Sending data in Chunks")
            i = 0
            for chunk in chunks(hashes_data, 100):
                print(f"Sending chunk {i}")
                conn.send(chunk.encode(FORMAT))
                i += 1
            print("All Data Sent")
        elif func == "get_en_data":
            hash_value = conn.recv(SIZE).decode(FORMAT)
            send_en_data_by_hash_value(hash_value, conn, addr)
            print("Data Sent")

        else:
            print("Invalid connection")
            conn.close()


def authenticate(addr):
    for _ in WHITELISTED_CLIENT_IPS:
        if _[0] == addr:
            return 1
    return 0


def send_blk_data_to_machines(data):
    for _ in NODES:
        connection = connect((_[0], _[1]))
        connection.send("save_node_blk_data".encode(FORMAT))
        time.sleep(2)
        i = 0
        print("Sending data in Chunks")
        for chunk in chunks(data, 100):
            print(f"Sending chunk {i}")
            connection.send(chunk.encode(FORMAT))
            i += 1

        print("All Data sent")

        connection.close()


def send_en_data_by_hash_value(hash_value, conn, addr):
    en_data = get_image_data(hash_value)
    decrypted_data_of_main_server = decyript_image(en_data, MAIN_SERVER_KEY)
    client_key = get_client_key_by_addr(addr)
    encrypted_image_for_given_machine = give_encyripted_image(decrypted_data_of_main_server, client_key)
    print("Sending data in Chunks")
    i = 0
    for chunk in chunks(encrypted_image_for_given_machine, 100):
        print(f"Sending chunk {i}")
        conn.send(chunk.encode(FORMAT))
        i += 1
    print("All Data Sent")


def verify_chain():
    flag = 0
    for _ in NODES:
        connection = connect((_[0], _[1]))
        connection.send("get_node_hash_data".encode(FORMAT))
        time.sleep(2)
        node_hash_dict = connection.recv(SIZE).decode(FORMAT)
        with open('/home/vishwajeet/Travclan/BLK/the_blockchain/hashes.json') as hashes_file:
            main_server_hash_dict = json.load(hashes_file)
        current_flag = main_server_hash_dict == node_hash_dict
        if not current_flag:
            print(f"Block Chain Not Verified At Node {_[0]}, {_[1]}. Please check the Machine.")
        flag = flag & current_flag
        connection.close()

    if flag:
        print("********Block Chain Verified****************")

    print("Block chain is corrupted please check the Data")


if __name__ == "__main__":
    main()

