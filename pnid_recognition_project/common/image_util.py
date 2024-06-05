import cv2
import numpy as np

def get_symbol_cropped_image(img, symbol_object):
    x, y, w, h = symbol_object.get_aabb()  # x,y,w,h
    crop_img = img[y:y + h, x:x + w]
    if h <= 0 or w <= 0:
        return None

    if symbol_object.degree != 0:  # if rotated, invert the rotation
        (cX, cY) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), -symbol_object.degree, 1.0)

        # new image size
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        rotated_img = cv2.warpAffine(crop_img, M, (nW, nH))

        origin_width = (symbol_object.max_point.x - symbol_object.min_point.x)
        origin_height = (symbol_object.max_point.y - symbol_object.min_point.y)

        rotated_minx = int((nW // 2) - origin_width / 2)
        rotated_miny = int((nH // 2) - origin_height / 2)
        crop_img = rotated_img[rotated_miny:rotated_miny + origin_height, rotated_minx:rotated_minx + origin_width]

    return crop_img