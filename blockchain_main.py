from blocks import create_new_block
from blocks import Block
from image import give_encyripted_image
from write_to_json import write_json
import json

if __name__ == '__main__' :


    images=['ok.jpg']
    hash=open('hashes.json','r+')

    x=hash.read()
    y=json.loads(x)
    z=y["hash_data"]
    

    hash_value=list(z[-1].values())[-1]

    en_image=give_encyripted_image(images[-1])


    new_block=create_new_block(hash_value, en_image )
    new_hash=new_block.block_hash
    new_data=new_block.block_data

    hash_data={
        f"hashcode{len(z)}":new_hash
    }
    block_data={
        f"block{len(z)}_hash":new_hash,
        f"block{len(z)-1}_hash":hash_value
    }
    write_json(hash_data,'hashes.json',"hash_data")
    write_json(block_data,'block_data.json',"blockchain_data")

    print(new_hash)

