import cv2
import numpy as np
import json, requests, os
from PIL import Image,features


board_img = cv2.imread('board1.jpeg', cv2.IMREAD_UNCHANGED)
board2_img = cv2.imread('board2.jpeg', cv2.IMREAD_UNCHANGED)
mak_img = cv2.imread('board2.jpeg', cv2.IMREAD_UNCHANGED)
test_img = cv2.imread('./item_images/Medium/Cutlass.png', cv2.IMREAD_UNCHANGED)


def resize_image(image, imageSize):
    # Target dimensions (width, height)
    if imageSize == "Medium":
        new_size = (200,200)
    elif imageSize == "Small":
        new_size = (100,200)
    elif imageSize == "Large":
        new_size = (300,200)
    # Resize
    resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return resized

def display_image(image, imageName): 
    cv2.imshow(imageName, image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def compare_images(board_image, image, imageSize):
    image = resize_image(image, imageSize)
    display_image(image, "candles")
    result = cv2.matchTemplate(board_image, image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    w = image.shape[1]
    h = image.shape[0]
    print(max_val)
    threshold = .6
    yloc, xloc = np.where(result >= threshold)
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, .1)
    for (x, y, w, h) in rectangles:
        cv2.rectangle(board_image, (x,y), (x+w, y+h), (0,255,255), 2)



if __name__ == "__main__":
    compare_images(mak_img, test_img, "Medium")
    display_image(mak_img, "mak")

    


