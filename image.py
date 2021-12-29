import cv2 as cv


def give_encyripted_image(name_of_image):
    img = cv.imread(name_of_image)
    encyripted_image = ""
    for _ in img.shape:
        encyripted_image = encyripted_image + str(_) + "-"

    for _ in img:
        for i in _:
            for j in i:
                encyripted_image = encyripted_image + str(j)
    return encyripted_image
