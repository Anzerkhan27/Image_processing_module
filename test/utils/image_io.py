import cv2
import os
from datetime import datetime

# Global variable to hold the run directory
run_folder = None

def init_run_dir():
    global run_folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = os.path.join("test", "output_images", timestamp)
    os.makedirs(run_folder, exist_ok=True)
    print(f"[INFO] Test run directory: {run_folder}")
    return run_folder

def save_image(img, filename):
    global run_folder
    if run_folder is None:
        raise RuntimeError("Run directory not initialized. Call init_run_dir() first.")
    path = os.path.join(run_folder, filename)
    cv2.imwrite(path, img)
    print(f"[SAVED] {path}")
