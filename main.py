import cv2
import numpy as np
import json, os
from PIL import Image,features
import concurrent.futures
from operator import itemgetter


board_img = cv2.imread('board1.jpeg', cv2.IMREAD_UNCHANGED)
board2_img = cv2.imread('board2.jpeg', cv2.IMREAD_UNCHANGED)
mak_img = cv2.imread('board2.jpeg', cv2.IMREAD_UNCHANGED)
test_img = cv2.imread('./item_images/Medium/Calcinator.png', cv2.IMREAD_UNCHANGED)
base_path = "item_images"
sizes = ["Small", "Medium", "Large"]
detected_items = []


def resize_image(image, imageSize):
    # Target dimensions (width, height)
    if imageSize == "Medium":
        new_size = (225,220)
    elif imageSize == "Small":
        new_size = (100,220)
    elif imageSize == "Large":
        new_size = (350,220)
    # Resize
    resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return resized

def display_image(image, imageName): 
    cv2.imshow(imageName, image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def process_image(file_path, size, board_img):
    img = cv2.imread(file_path)
    if img is None:
        print(f"Error reading {file_path} (file may be corrupt or not a valid image)")
        return
    items = compare_images(board_img, img, size)
    if len(items) > 0:
        for item in items:
            detected_items.append({"name": extract_file_string(file_path), "x-coord": int(item[0]), "y-coord": int(item[1])})

def extract_file_string(file_path):
    filename = os.path.basename(file_path)             
    name = os.path.splitext(filename)[0] 
    pretty_name = name.replace('_', ' ') 
    return pretty_name

def process_folder(folder_path, size, board_img):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                executor.submit(process_image, file_path, size, board_img)

def get_center_vertical_strip(image, height_scale=0.55, width_scale=0.65):
    h, w = image.shape[:2]  # Get height and width of the image
    roi_h = int(h * height_scale)  # Calculate the height of the ROI
    roi_w = int(w * width_scale) # Calculate the width of the ROI
    y_start = (h - roi_h) // 2      # Calculate the top Y-coordinate to center it vertically
    x_start = (w - roi_w) // 2 # Calculate top X-coordinate
    return image[y_start:y_start+roi_h, x_start:x_start+roi_w], (x_start, y_start)

def compare_images(board_image, image, imageSize, threshold = .6):
    image = resize_image(image, imageSize)
    roi, offset = get_center_vertical_strip(board_image)
    offset_x, offset_y = offset
    result = cv2.matchTemplate(roi, image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    w = image.shape[1]
    h = image.shape[0]

    # print(max_val, max_loc)

    yloc, xloc = np.where(result >= threshold)
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x + offset_x), int(y + offset_y), int(w), int(h)])
        rectangles.append([int(x + offset_x), int(y + offset_y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, .1)
    for (x, y, w, h) in rectangles:
        cv2.rectangle(board_image, (x,y), (x+w, y+h), (0,255,255), 2)
    
    return rectangles

def detect_items_on_board(board_img):
    for size in sizes:
        folder_path = os.path.join(base_path, size)
        if not os.path.exists(folder_path):
            continue  # Skip if folder doesn't exist
        process_folder(folder_path, size, board_img)

    sort_items(detected_items,board_img.shape[0])
    with open("detected_items.json", "w") as f:
        json.dump(detected_items, f, indent=2)

def sort_items(items, board_height):
    for item in items:
        item["board"] = "your_board" if item["y-coord"] > board_height / 2 else "enemies_board"

    your_board_items = [item for item in items if item["board"] == "your_board"]
    enemy_board_items = [item for item in items if item["board"] == "enemies_board"]

    # Sort by x-coordinate and assign positions
    for board_items in [your_board_items, enemy_board_items]:
        board_items.sort(key=itemgetter("x-coord"))
        for idx, item in enumerate(board_items, start=1):
            item["position"] = idx
    
    items = your_board_items + enemy_board_items
    return items

if __name__ == "__main__":
    detect_items_on_board(mak_img)
    display_image(mak_img, "mak")

    


