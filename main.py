import cv2
import numpy as np
import json, os
import concurrent.futures
from operator import itemgetter
from image_processor import ImageProcessor
from item_detector import ItemDetector

if __name__ == "__main__":
    calc_img = ImageProcessor.load_image("./item_images/Small/Bayonet.png")
    mak_img = ImageProcessor.load_image("board2.jpeg")
    small_screen = ImageProcessor.load_image("1920-1080-Bazaar.png")
    stretched_small_screen = ImageProcessor.load_image("2560x1080-Bazaar.png")
    medium_screen = ImageProcessor.load_image("2560x1440-Bazaar.png")
    full_screen = ImageProcessor.load_image("Full_Screen.png")

    # Trying out different screen sizes
    # ImageProcessor.display_image(full_screen)
    # ImageProcessor.display_image(get_center_vertical_strip(full_screen)[0])
    # ImageProcessor.display_image(small_screen)
    # ImageProcessor.display_image(get_center_vertical_strip(small_screen)[0])
    # ImageProcessor.display_image(stretched_small_screen)
    # ImageProcessor.display_image(get_center_vertical_strip(stretched_small_screen)[0])
    # ImageProcessor.display_image(medium_screen)
    # ImageProcessor.display_image(get_center_vertical_strip(medium_screen)[0])
    # calc_img = resize_image(calc_img,"Medium", get_image_dimensions(full_screen))
    # compare_images(full_screen, calc_img, "Small")
    # ImageProcessor.display_image(full_screen)
    # compare_images(medium_screen, calc_img, "Small")
    # ImageProcessor.display_image(medium_screen)
    # compare_images(small_screen, calc_img, "Small")
    # ImageProcessor.display_image(small_screen)
    # compare_images(stretched_small_screen, calc_img, "Small")
    # ImageProcessor.display_image(stretched_small_screen)


    detector = ItemDetector()
    detector.detect_items_on_board(mak_img)
    ImageProcessor.display_image(mak_img, "mak")
    


