from blocks import create_new_block
from blocks import Block
from image import give_encyripted_image
from image import get_key
from write_to_json import write_json
from common import get_key_by_addr
from constants import CAMERA_MODULES_IPS

import json
import time


def execute_process(en_image):
    hash = open('hashes.json', 'r+')

    x = hash.read()
    y = json.loads(x)
    z = y["hash_data"]

    key = get_key()

    hash_value = list(z[-1].values())[-1]

    '''commenting the code as we are now operating this in main server'''
    '''To be uncommented for main server and commented for remaining ones'''

    # sttime=time.time()
    # print(f"encryption started at {sttime}\n")
    #
    # en_image = give_encyripted_image(image_path,key)
    #
    # endtime=time.time()
    # print(f"encryption ended at {endtime}\n")
    # print(f"total time taken to encrypt = {endtime-sttime}\n")

    new_block = create_new_block(hash_value, en_image)
    new_hash = new_block.block_hash

    hash_data = {
        f"hashcode{len(z)}": new_hash
    }
    block_data = {
        f"block{len(z)}_hash": new_hash,
        f"block{len(z) - 1}_hash": hash_value
    }
    image_data = {
        f"hashcode{len(z)}": new_hash,
        f"image{len(z)}": en_image
    }

    write_json(hash_data, 'hashes.json', "hash_data")
    write_json(block_data, 'block_data.json', "blockchain_data")
    write_json(image_data, 'images.json', "image_data")

    print(new_hash)

    return {
        "previous_hash": hash_value,
        "new_hash": new_hash,
        "en_image": en_image
    }


def execute_node_process(en_image):
    hash = open('hashes.json', 'r+')

    x = hash.read()
    y = json.loads(x)
    z = y["hash_data"]

    hash_value = list(z[-1].values())[-1]

    new_block = create_new_block(hash_value, en_image)
    new_hash = new_block.block_hash

    hash_data = {
        f"hashcode{len(z)}": new_hash
    }
    block_data = {
        f"block{len(z)}_hash": new_hash,
        f"block{len(z) - 1}_hash": hash_value
    }
    image_data = {
        f"hashcode{len(z)}": new_hash,
        f"image{len(z)}": en_image
    }

    write_json(hash_data, 'hashes.json', "hash_data")
    write_json(block_data, 'block_data.json', "blockchain_data")
    write_json(image_data, 'images.json', "image_data")

    print("New Block Added To Node")
    print(new_hash)


def execute_camera_module_process(im_path, ip):
    key = get_key_by_addr(ip, CAMERA_MODULES_IPS)
    en_camera_image = give_encyripted_image(im_path, key)
    return en_camera_image

