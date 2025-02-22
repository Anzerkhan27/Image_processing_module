import cv2
import numpy as np
import random
import os

# Configuration
BACKGROUND_SIZE = (600, 600)  # (width, height)
QR_CODE_SIZE = (150, 150)  # Resize QR codes to fit
QR_IMAGES_FOLDER = "qr_dataset"  # Folder where QR codes are stored
OUTPUT_FOLDER = "qr_code_images"  # Folder to store generated images
OUTPUT_IMAGE = os.path.join(OUTPUT_FOLDER, "generated_qr_image.png")
NUM_QR_CODES = 5  # Number of QR codes to place

def load_qr_images(folder, num_qr):
    """Load random QR images from the dataset folder."""
    qr_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if len(qr_files) < num_qr:
        raise ValueError("Not enough QR images in the folder!")
    
    selected_qrs = random.sample(qr_files, num_qr)
    return [cv2.imread(qr, cv2.IMREAD_UNCHANGED) for qr in selected_qrs]

def generate_qr_image():
    """Generate an image with multiple QR codes placed randomly on a background."""
    
    # Create the output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Create a blank white background
    background = np.ones((BACKGROUND_SIZE[1], BACKGROUND_SIZE[0], 3), dtype=np.uint8) * 255
    
    # Load QR codes
    qr_images = load_qr_images(QR_IMAGES_FOLDER, NUM_QR_CODES)

    # Randomly place QR codes
    placed_positions = []
    for qr_img in qr_images:
        qr_img = cv2.resize(qr_img, QR_CODE_SIZE)  # Resize QR code

        # Generate random position (avoid overlap)
        while True:
            x = random.randint(0, BACKGROUND_SIZE[0] - QR_CODE_SIZE[0])
            y = random.randint(0, BACKGROUND_SIZE[1] - QR_CODE_SIZE[1])
            overlap = any(abs(x - px) < QR_CODE_SIZE[0] and abs(y - py) < QR_CODE_SIZE[1] for px, py in placed_positions)
            if not overlap:
                placed_positions.append((x, y))
                break

        # Place QR code on background
        background[y:y+QR_CODE_SIZE[1], x:x+QR_CODE_SIZE[0]] = qr_img

    # Save the generated image
    cv2.imwrite(OUTPUT_IMAGE, background)
    print(f"Generated image saved as {OUTPUT_IMAGE}")

# Run the generator
if __name__ == "__main__":
    generate_qr_image()
