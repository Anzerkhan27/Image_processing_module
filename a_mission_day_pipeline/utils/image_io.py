import os
import cv2
import datetime

def save_image(image, path):
    cv2.imwrite(path, image)

def init_output_folder(site_name):
    base = os.path.join("output", site_name)
    os.makedirs(base, exist_ok=True)
    return base
