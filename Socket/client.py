import socket
IP = "192.168.0.190"
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000
from ..image import give_encyripted_image , get_key


def main():
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    client.connect(ADDR)
    key = get_key()
    en_image = give_encyripted_image("/Users/siddharthsharma/Desktop/the_blockchain/images/Kela.jpg",key)
    client.send(en_image.encode(FORMAT))
    """ Sending the file data to the server. """
    # file = open("data/image.jpeg", "rb")
    # im_data = file.read(SIZE)
    # while im_data:
    #     client.send(im_data)
    #     im_data = file.read(SIZE)
    # file.close()
    client.close()

if __name__ == "__main__":
    main()