# image_processing/config.py
import os

# Base directory is always /app in Docker
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

CONFIG = {
    "background_size": (600, 600),
    "qr_code_size": (150, 150),
    "qr_min_size": 100,
    "qr_max_size": 200,
    "qr_images_folder": "/app/qr_dataset",  # Absolute path
    "output_folder": "/app/qr_code_images",
    "output_image": "/app/qr_code_images/generated_qr_image.png",
    "num_qr_codes": 8,
    "cropped_output_folder": "/app/cropped_qr_codes",
    "default_image_name": "generated_qr_image.png",
    "sliding_window_size": 200,
    "sliding_stride": 50,
    "margin": 10
}