import cv2
import numpy as np
import os

class ImageProcessor:
    def load_image(imagePath) -> np.ndarray:
        image = cv2.imread(imagePath, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Failed to load image: {imagePath}")
        return image

    def resize_image(image, image_size, board_dimensions) -> np.ndarray:
        # Target dimensions (width, height)
        if image_size == "Medium":
            h = int(board_dimensions[0]  * .34)
            w = int(board_dimensions[0] * .34)
        elif image_size == "Small":
            h = int(board_dimensions[0] * .33)
            w = int(board_dimensions[0] * .16)
        elif image_size == "Large":
            h = int(board_dimensions[0] * .34)
            w = int(board_dimensions[0] * .52)
        # Resize
        resized = cv2.resize(image, (w,h), interpolation=cv2.INTER_AREA)
        return resized
    
    def display_image(image, imageName="image"): 
        cv2.imshow(imageName, image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def get_image_dimensions(image):
        return image.shape[0], image.shape[1]
    
    def get_center_vertical_strip(image, height_scale=0.55, width_scale=0.6):
        h, w = image.shape[:2]  # Get height and width of the image
        roi_h = int(h * height_scale)  # Calculate the height of the ROI
        roi_w = int(w * width_scale) # Calculate the width of the ROI
        y_start = (h - roi_h) // 2      # Calculate the top Y-coordinate to center it vertically
        x_start = (w - roi_w) // 2 # Calculate top X-coordinate
        return image[y_start:y_start+roi_h, x_start:x_start+roi_w], (x_start, y_start)