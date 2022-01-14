from blocks import create_new_block
from blocks import Block
from image import give_encyripted_image
from image import get_key
from write_to_json import write_json

import json




def execute_process(image_path):

    hash = open('hashes.json', 'r+')

    x = hash.read()
    y = json.loads(x)
    z = y["hash_data"]

    key = get_key()

    hash_value = list(z[-1].values())[-1]

    en_image = give_encyripted_image(image_path,key)

    new_block = create_new_block(hash_value, en_image)
    new_hash = new_block.block_hash
    

    hash_data = {
        f"hashcode{len(z)}": new_hash
    }
    block_data = {
        f"block{len(z)}_hash": new_hash,
        f"block{len(z) - 1}_hash": hash_value
    }
    image_data={
        f"hashcode{len(z)}": new_hash,
        f"image{len(z)}": en_image
    }

    write_json(hash_data, 'hashes.json', "hash_data")
    write_json(block_data, 'block_data.json', "blockchain_data")
    write_json(image_data, 'images.json', "image_data")

    print(new_hash)
