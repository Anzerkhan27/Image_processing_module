
import os

# Directory of this file: image_processing/
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Project root is one level up
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

CONFIG = {
    "background_size": (600, 600),
    "qr_code_size": (150, 150),
    "qr_min_size": 100,
    "qr_max_size": 200,
    "qr_images_folder": os.path.join(PROJECT_ROOT, "qr_dataset"),
    "output_folder": os.path.join(PROJECT_ROOT, "qr_code_images"),
    "output_image": os.path.join(PROJECT_ROOT, "qr_code_images", "generated_qr_image.png"),
    "num_qr_codes": 8,
    "cropped_output_folder": os.path.join(PROJECT_ROOT, "cropped_qr_codes"),
    "default_image_name": "generated_qr_image.png",
    "sliding_window_size": 200,
    "sliding_stride": 50,
    "margin": 10
}
