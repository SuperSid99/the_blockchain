from email.mime import image
import json


def write_json(new_data, filename, key_name=None):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        file_data[key_name].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def get_image_data(hashcode):

    image = open('images.json', 'r+')

    x = image.read()
    y = json.loads(x)
    z = y["image_data"]
    
    count=0

# this function is to send the blockchain to the server
def get_blockchain():
    pass

# print(z.values())

    for _ in z:
        if _[f'hashcode{count}'] == hashcode :
            return(_[f'image{count}'])
        count+=1
    
    return("no results found")
