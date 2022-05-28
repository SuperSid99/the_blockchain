import socket
from common import save_node_blk_data, get_node_hash_data

NODE_IP = ""
NODE_PORT = ""
SIZE = 10240000000
FORMAT = "utf-8"

# This function will open up a port of listener(with given IP) for the client to recieve the data files


def initiate_socket_listener():
    global conn
    global addr
    global server
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        'Bind the IP and PORT to the server'
        server.bind((NODE_IP, NODE_PORT))
        'Server is Listening, i.e, server is now waiting for the client to get connected.'
        server.listen()
        '''Accepting Connection from Client. '''

        print(f"Server is Listening in The thread on {NODE_IP, NODE_PORT}")
        conn, addr = server.accept()
        server.setblocking(True)
        print(f"[New Connection] {addr} connected.")
        print("New Connection Started seeding file")
        func = conn.recv(512).decode(FORMAT)

        if func == 'save_node_blk_data':
            save_node_blk_data()
            print(f"Block Data saved!!")
        elif func == 'get_node_hash_data':
            hash_data = get_node_hash_data("path to file to be sent here")
            conn.send(hash_data.encode(FORMAT))

        else:
            conn.close()


def main():
    initiate_socket_listener()


if __name__ == '__main__':
    main()

