import cv2 as cv
import numpy
import json
from write_to_json import get_image_data


def get_key():

    key_json = open('block_data.json', 'r+')

    a = key_json.read()
    b = json.loads(a)
    return(b["blockchain_data"][0]['Key'])

def give_encyripted_image(name_of_image, key):
    Key_dic = genarate_key(key)
    img = cv.imread(name_of_image)
    encyripted_image = ""
    for _ in img.shape:
        try:
            for x in str(_):
                encyripted_image += Key_dic[str(x)]
            encyripted_image+="-"
        except:
            encyripted_image +=  f"{Key_dic[str(_)]}-"

    for _ in img:
        for i in _:
            for j in i:
                try:
                    for _ in str(j):
                        encyripted_image += Key_dic[_]
                    encyripted_image+="-"
                except:
                    encyripted_image += f"{Key_dic[str(j)]}-"
    return encyripted_image



def decyript_image(hashcode):

    im_data=get_image_data(hashcode)

    key=get_key()

    im_arr=im_data.split("-")

    Key_dic = genarate_key(key)

    new_dic={}
    for _ in Key_dic:
        new_dic[Key_dic[_]]=_
    
    im_arr_decyripted=[]
    for i in im_arr:
        a=''
        for _ in i:
            a+=new_dic[_]
        im_arr_decyripted.append(a)

    row=int(im_arr_decyripted[0])
    coll=int(im_arr_decyripted[1])
    rgb=int(im_arr_decyripted[2])
    c4=3
    im_arr_decyripted_ndimentional=[]

    for i in range(row):
        im_arr_decyripted_ndimentional.append([])
        for j in range(coll):
            im_arr_decyripted_ndimentional[i].append([])
            for _ in range(rgb):
                im_arr_decyripted_ndimentional[i][j].append(int(im_arr_decyripted[c4]))
                c4+=1
    return(numpy.array(im_arr_decyripted_ndimentional, dtype=numpy.uint8))



def genarate_key(key):

    dic = {}
    count = 0
    c1 = 0
    arr = []
    for _ in str(key):
        if int(_) not in arr:
            dic[str(count)] = _
            arr.append(int(_))
            count += 1
        else:
            continue

    for _ in range(10 - len(dic)):
        nono = True
        while nono:

            if 9 - c1 not in arr:
                dic[str(count)] = str(9 - c1)
                arr.append(9 - c1)
                count += 1
                c1 += 1
                nono = False
            else:
                c1 += 1
    return(dic)

if __name__=="__main__":
    sasti = decyript_image("7a5a7a83ee28c7a7a95295664486637e0c476b0d84e8a0281ecab997795a9445")

    vj=cv.imshow("sasti", sasti)
    cv.waitKey(0)
