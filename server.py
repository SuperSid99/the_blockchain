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

import socket
import json

from numpy import size
from blockchain_main import execute_process, execute_node_process
import time
import cv2 as cv
import numpy
from image import decyript_image, give_encyripted_image, get_key, give_encyripted_image_for_main_server
from common import chunks, get_data_by_chunks, get_key_by_addr, connect, get_node_hash_data, get_client_key_by_addr
from constants import NODES, CAMERA_MODULES_IPS, WHITELISTED_CLIENT_IPS
from write_to_json import get_image_data

# "IP Address of the main server"
IP = "100.97.221.115"
PORT = 5589
ADDR = (IP, PORT)
SIZE = 10240000000
FORMAT = "utf-8"
MAIN_SERVER_KEY = "1942216"


def save_node_blk_data(conn):
    data = get_data_by_chunks(conn)
    print("All Data Received")
    execute_node_process(data)
    conn.close()
    # print(f"Disconnected {addr} disconnected")


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
    try:
        while True:
            '''Accepting Connection from Client. '''
            conn, addr = server.accept()
            print(f"[New Connection] {addr} connected.")
            print("New Connection Started seeding file")

            # data = conn.recv(512).decode(FORMAT)
            # print(data)
            
            func = conn.recv(51).decode(FORMAT)
            print(func)


            if func == "camera":

                print("reecieved camera")
                conn.send("OK".encode(FORMAT))
                print("authentication sent")
                total_data = get_data_by_chunks(conn)
                print("Received Data from Camera Module")
                data = ''.join(total_data)
                print(len(total_data))
                '''Now Decrypt image from Camera Module'''
                decrypted_data_from_camera_module = get_decrypted_data_of_camera_module(addr[0], data)

                print(len(decrypted_data_from_camera_module))
                print(len(decrypted_data_from_camera_module[0]))
                
                # imggg= (numpy.array(decrypted_data_from_camera_module, dtype=numpy.uint8))
                # print(imggg.shape)
                # cv.imshow("im_numpy", imggg)
                # cv.waitKey(0)

                if verify_chain():
                    key = get_key()
                    final_encrypted_data = give_encyripted_image_for_main_server(decrypted_data_from_camera_module, key)
                    processed_block = execute_process(final_encrypted_data)
                    print(processed_block)
                    print("process finished") # send_blk_data_to_machines(processed_block)
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
    except:
        import traceback
        traceback.print_exc()


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
    print("reaching Here")
    flag = True
    for _ in NODES:
        connection = connect((_[0], _[1]))
        print("CONNECTED")
        time.sleep(2)
        connection.send("get_node_hash_data".encode(FORMAT))
        var = connection.recv(512).decode(FORMAT)
        if var == "OK":
            node_hash_dict = get_data_by_chunks(connection)
            node_hash_dict = "".join(node_hash_dict)
            node_hash_dict = (json.loads(node_hash_dict))
            # print(type(node_hash_dict),node_hash_dict)
            # node_hash_dict = json.loads(node_hash_dict)
            with open('/Users/siddharthsharma/Desktop/the_blockchain/hashes.json') as hashes_file:
                main_server_hash_dict = (json.load(hashes_file))
            # print(type(main_server_hash_dict),json.dumps(main_server_hash_dict))

            print((main_server_hash_dict) == node_hash_dict)
            
            # if len(main_server_hash_dict) == len(node_hash_dict):
            #     current_flag=True
            #     for _ in range(len(main_server_hash_dict)):
            #         if main_server_hash_dict[_] == node_hash_dict[_]:
            #             pass
            #         else:
            #             print(_,main_server_hash_dict[_],node_hash_dict[_])
            #             current_flag=False
                
            # else:
            #     print(main_server_hash_dict,node_hash_dict)
            #     current_flag=False
            current_flag = main_server_hash_dict == node_hash_dict
            print(current_flag)
            if not current_flag:
                print(f"Block Chain Not Verified At Node {_[0]}, {_[1]}. Please check the Machine.")
            flag = flag & current_flag
            connection.close()
        else:
            print("No Acknowledged")
            return flag

    if flag:
        print("********Block Chain Verified****************")

    return(flag)


if __name__ == "__main__":
    main()

