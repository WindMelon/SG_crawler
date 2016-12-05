# -*- coding:utf-8 -*-

import pytesseract
from PIL import Image

def img2code(img):
    str1 = pytesseract.image_to_string(img)
    return str1

if __name__ == "__main__":
    img = Image.open("vv.jpg")
    print(img2code(img))