import cv2 as cv


def give_encyripted_image(name_of_image, key):
    Key_dic = genarate_key(key)
    img = cv.imread(name_of_image)
    encyripted_image = ""
    for _ in img.shape:
        encyripted_image += str(_) + "-"

    for _ in img:
        for i in _:
            for j in i:
                try:
                    for _ in str(j):
                        encyripted_image += Key_dic[_]
                    encyripted_image+="-"
                except:
                    encyripted_image += Key_dic[str(j)]
                    encyripted_image+="-"
    return encyripted_image


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
