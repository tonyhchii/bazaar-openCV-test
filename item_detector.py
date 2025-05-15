import cv2
import numpy as np
import os, json
from operator import itemgetter
import concurrent.futures
from typing import List, Dict
from image_processor import ImageProcessor

class ItemDetector:
    def __init__(self, item_images_path: str = "item_images"):
        self.ITEM_IMAGES_PATH = item_images_path
        self.sizes = ["Small", "Medium", "Large"]

    def extract_file_string(self, file_path):
        filename = os.path.basename(file_path)             
        name = os.path.splitext(filename)[0] 
        pretty_name = name.replace('_', ' ') 
        return pretty_name

    def compare_images(self, board_image, image, image_size, threshold = .6):    
        roi, offset = ImageProcessor.get_center_vertical_strip(board_image) # Get region of interest and offset
        offset_x, offset_y = offset

        board_dimensions = ImageProcessor.get_image_dimensions(roi)
        image = ImageProcessor.resize_image(image, image_size, board_dimensions) # Change image to relative size of board
        # ImageProcessor.display_image(image)
        result = cv2.matchTemplate(roi, image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        w = image.shape[1]
        h = image.shape[0]

        # print(max_val, max_loc)

        yloc, xloc = np.where(result >= threshold)
        rectangles = []
        rectangle_scores = []
        
        for (x, y) in zip(xloc, yloc):
            score = result[y, x]
            rect = [int(x + offset_x), int(y + offset_y), int(w), int(h)]
            rectangles.append(rect)
            rectangles.append(rect.copy())  # Duplicate for grouping
            rectangle_scores.append(score)
        
        # Group rectangles (using only coordinates)
        grouped_rects, _ = cv2.groupRectangles(rectangles, 1, .2)
        
        # For each grouped rectangle, find the maximum score
        final_results = []
        for (x, y, w, h) in grouped_rects:
            # Find all original rectangles that overlap with this grouped rectangle
            max_score = 0
            for i, (rx, ry, rw, rh) in enumerate(rectangles[::2]):  # Skip duplicates
                if (abs(x - rx) < w and abs(y - ry) < h):
                    if rectangle_scores[i] > max_score:
                        max_score = rectangle_scores[i]
            
            # Draw rectangle (optional)
            cv2.rectangle(board_image, (x, y), (x+w, y+h), (0, 255, 255), 2)
            
            # Store rectangle with its MAX score
            final_results.append({
                'rect': (x, y, w, h),
                'score': max_score
            })
        return final_results

    
    def process_image(self, file_path: str, size: str, board_img: np.ndarray) -> list:
        """Process a single item image and return detected items"""
        img = ImageProcessor.load_image(file_path)
        if img is None:
            print(f"Error reading {file_path} (file may be corrupt or not a valid image)")
            return []
        
        items = self.compare_images(board_img, img, size)
        detected = []
        if items:
            for item in items:
                detected.append({
                    "name": self.extract_file_string(file_path),
                    "x_coord": int(item['rect'][0]),
                    "y_coord": int(item['rect'][1]),
                    "score": float(item['score'])
                })
        return detected



    def process_folder(self, folder_path: str, size: str, board_img: np.ndarray) -> list:
        """Process all images in a folder using threads and combine results"""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit all image processing tasks
            futures = []
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    futures.append(executor.submit(self.process_image, file_path, size, board_img))
            
            # Collect results as they complete
            all_detected = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    detected_items = future.result()
                    all_detected.extend(detected_items)
                except Exception as e:
                    print(f"Error processing image: {e}")
        
        return all_detected


    def detect_items_on_board(self, board_img):
        detected_items = []
        for size in self.sizes:
            folder_path = os.path.join(self.ITEM_IMAGES_PATH, size)
            if not os.path.exists(folder_path):
                continue  # Skip if folder doesn't exist
            detected = self.process_folder(folder_path, size, board_img)
            detected_items.extend(detected)
        self.sort_items(detected_items, board_img.shape[0])
        with open("detected_items.json", "w") as f:
            json.dump(detected_items, f, indent=2)

    def sort_items(self, items, board_height):
        for item in items:
            item["board"] = "your_board" if item["y_coord"] > board_height / 2 else "enemies_board"

        your_board_items = [item for item in items if item["board"] == "your_board"]
        enemy_board_items = [item for item in items if item["board"] == "enemies_board"]

        # Sort by x-coordinate and assign positions
        for board_items in [your_board_items, enemy_board_items]:
            board_items.sort(key=itemgetter("x_coord"))
            for idx, item in enumerate(board_items, start=1):
                item["position"] = idx
        
        items = your_board_items + enemy_board_items
        return items