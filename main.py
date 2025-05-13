import cv2
import numpy as np
from PIL import Image,features

board_img = cv2.imread('VanessaBoard.png', cv2.IMREAD_UNCHANGED)
mak_img = cv2.imread('MakBoard.png', cv2.IMREAD_UNCHANGED)
aludel_img = cv2.imread('aludel.jpg', cv2.IMREAD_UNCHANGED)
starchart_img = cv2.imread('Starchart.png', cv2.IMREAD_UNCHANGED)
calcinator_img = cv2.imread('calcinator.jpeg', cv2.IMREAD_UNCHANGED)
calcinator_gray = cv2.imread('calcinator.jpeg', cv2.IMREAD_GRAYSCALE)
mak_gray2 = cv2.imread('MakBoard.png', cv2.IMREAD_GRAYSCALE)

def resize_image(image):
    # Target dimensions (width, height)
    new_size = (300,300)
    # Resize
    resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return resized

def convert_image_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)

def display_image(image, imageName): 
    cv2.imshow(imageName, image)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    img = resize_image(calcinator_img)
    resize_calc_gray = resize_image(calcinator_gray)
    img = convert_image_grayscale(img)
    mak_gray = convert_image_grayscale(mak_img)
    result = cv2.matchTemplate(mak_gray2, resize_calc_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    w = starchart_img.shape[1]
    h = starchart_img.shape[0]
    print(max_val)
    threshold = .75
    yloc, xloc = np.where(result >= threshold)
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, .2)
    for (x, y, w, h) in rectangles:
        cv2.rectangle(mak_img, (x,y), (x+w, y+h), (0,255,255), 2)
    display_image(mak_img, "mak")

    


