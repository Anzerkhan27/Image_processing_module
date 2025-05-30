import cv2
import numpy as np
from test.utils.image_io import save_image

def enhance_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)

    # Sharpen
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(contrast, -1, kernel)
    result = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)
    save_image(result, "02_enhanced.jpg")
    return result
