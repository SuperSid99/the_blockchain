# from http import client
# import socket
# import sys
# import errno
# IP = "100.81.249.49"
# PORT = 5589
# ADDR = (IP, PORT)
# FORMAT = "utf-8"
# SIZE = 10240000000
# import time
# from image import give_encyripted_image, get_key
#
#
# def chunks(lst, n):
#     "Yield successive n-sized chunks from lst"
#     for i in range(0, len(lst), n):
#         yield lst[i:i + n]
#
#
# def main():
#     """ Staring a TCP socket. """
#     f = []
#     import os
#     from os import listdir
#
#     # get the path or directory
#     folder_dir = ""
#     for images in os.listdir(folder_dir):
#
#         # check if the image end swith png or jpg or jpeg
#         if (images.endswith(".png") or images.endswith(".jpg")
#                 or images.endswith(".jpeg")):
#             # display
#             f.append(images)
#             print(images)
#     print("Available Files Are::")
#     print(f)
#
#     for image in f:
#         print(f"Sending Image {image}")
#         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         '''socket.SOCK_STREAM. ===> TCP ProtocolIs -> reliable(no data lost) -> Has in-order data delivery: Data is
#         read by your application in the order it was written by the sender.
#         AF_INET ===> IPv4
#         socket.socket() creates a socket object that supports the context manager type, so you can use it in a with
#         statement.
#         Further Notes ==> https://realpython.com/python-sockets/ '''
#         """ Connecting to the server. """
#         try:
#             client.connect(ADDR)
#             key = get_key()
#
#             # client.send(image.encode(FORMAT))
#
#             en_image = give_encyripted_image(f"path to folder/{image}", key)
#             i = 0
#             print("Sending data in Chunks")
#             for chunk in chunks(en_image, 100):
#                 print(f"Sending chunk {i}")
#                 client.send(chunk.encode(FORMAT))
#                 i += 1
#
#             print("All Data sent")
#
#             client.close()
#
#             time.sleep(2)
#         except Exception as e:
#             print("There was a problem while running the Script ")
#             print(e)
#
# if __name__ == "__main__":
#     main()
#
#
from image import decyript_image
import socket
import time
from common import get_data_by_chunks
import numpy
import cv2 as cv
import json
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('')

MAIN_SERVER_IP = "100.97.221.115"
MAIN_SERVER_PORT = 5589
MACHINE_KEY = 123456
IP = "100.81.249.49"
PORT = 4569
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000


# # This function will open up a port of listener(with given IP) for the client to recieve the data files
# def initiate_socket_listener():
#     global conn
#     global addr
#     global server
#     while True:
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         'Bind the IP and PORT to the server'
#         server.bind(ADDR)
#         'Server is Listening, i.e, server is now waiting for the client to get connected.'
#         server.listen()
#         '''Accepting Connection from Client. '''
#
#         print(f"Server is Listening in The thread on {ADDR}")
#
#         conn, addr = server.accept()
#         server.setblocking(True)
#         print(f"[New Connection] {addr} connected.")
#         print("New Connection Started seeding file")
#         func = conn.recv(512).decode(FORMAT)
#
#         if func == 'save_blk_data':
#             save_blk_data()
#             print(f"Block Data saved!!")
#         elif func == 'get_hash_data':
#             hash_data = get_hash_data()
#             conn.send(hash_data.encode(FORMAT))
#
#         else:
#             conn.close()
#
#


def connect_to_main_server():
    try:
        main_server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """ Connecting to the server. """
        main_server_connection.connect((MAIN_SERVER_IP, MAIN_SERVER_PORT))
        return main_server_connection
    except Exception as e:
        log.error(f"An Error Occurred While Connecting To Main Server. Error ==> {e}")
        raise e


flag = False


def cli():
    global flag
    while True:
        print("\n********Client Interface*********")
        print("1.) Authenticate With Main Server")
        print("2.) Get All Hashes")
        print("3.) Get Hash Data")
        print("4.) Return To Main Interface")
        print("5.) Exit")
        print("*********************************")
        print("\n>>Enter Your Choice:")
        x = int(input())
        if x == 1:
            flag = authenticate()
        elif x == 2:
            get_hashes(flag)
        elif x == 3:
            print("Give the hash Value")
            hash_value = input()
            get_data(flag, hash_value)
        elif x == 4:
            print("\nReturning")
        elif x == 5:
            print("\nThanks Exiting!!")
            # connection.close()
            break
        else:
            print("\nInvalid choice. Please Enter A valid Choice")


def authenticate():
    connection = connect_to_main_server()
    connection.send("authenticate".encode(FORMAT))
    var = connection.recv(512).decode(FORMAT)
    if var == "OK":
        # connection.send(IP.encode(FORMAT))
        log.info("Please wait while we are authenticating You.")
        authentication_flag = connection.recv(SIZE).decode(FORMAT)
        print(authentication_flag)
        if not authentication_flag:
            log.info("Invalid Client. Please Try Again")
        else:
            log.info("You Are Authenticated.")
        connection.close()
    else:
        log.error("Connection Not Acknowledged.")
    return authentication_flag


def get_hashes(authentication_flag):
    if authentication_flag:
        log.info("Please Wait While We are Fetching Info of Hashes From Main Server")
        get_hashes_data(authentication_flag)
    else:
        log.error("\nYou Are Not Authenticated. Please Authenticate Yourself First.")


def get_hashes_data(authentication_flag):
    connection = connect_to_main_server()
    if authentication_flag:
        connection.send("get_hash_data".encode(FORMAT))
        time.sleep(1)
        var = connection.recv(512).decode(FORMAT)
        if var == "OK":
            data = get_data_by_chunks(connection)
            data = "".join(data)
            data = json.loads(data)
            log.info("The Available Hashes are-->>>")
            print(data)
        else:
            log.error("Connection Not Acknowledged.")
    else:
        log.error("\nYou Are Not Authenticated. Please Authenticate Yourself First.")
    connection.close()


def get_data(authentication_flag, hash_value):
    connection = connect_to_main_server()
    if authentication_flag:
        connection.send("get_en_data".encode(FORMAT))
        time.sleep(1)
        var = connection.recv(512).decode(FORMAT)
        if var == "OK":
            connection.send(hash_value.encode(FORMAT))
            data = get_data_by_chunks(connection)
            data = ''.join(data)
            decrypted_data = decyript_image(data, MACHINE_KEY)
            img = (numpy.array(decrypted_data, dtype=numpy.uint8))
            cv.imshow("im_numpy", img)
            cv.waitKey(0)
            cv.destroyAllWindows()
            cv.waitKey(1)
        else:
            log.error("Connection Not Acknowledged.")
        return 1

    else:
        log.error("\nYou Are Not Authenticated. Please Authenticate Yourself First.")
    connection.close()


if __name__ == "__main__":
    # print("reaching")
    # t1 = threading.Thread(target=initiate_socket_listener)
    # t1.daemon = True
    # t1.start()
    cli()

    log.info("Connection Closed")
