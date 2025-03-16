import cv2
import numpy as np
import random
import os

# Configuration
BACKGROUND_SIZE = (600, 600)  # (width, height)
# Define the range of QR code sizes (in pixels)
QR_MIN_SIZE = 100
QR_MAX_SIZE = 200
QR_IMAGES_FOLDER = "qr_dataset"  # Folder where QR codes are stored
OUTPUT_FOLDER = "qr_code_images"  # Folder to store generated images
OUTPUT_IMAGE = os.path.join(OUTPUT_FOLDER, "generated_qr_image.png")
NUM_QR_CODES = 5  # Number of QR codes to place

def load_qr_images(folder, num_qr):
    """Load random QR images from the dataset folder."""
    qr_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if len(qr_files) < num_qr:
        raise ValueError("Not enough QR images in the folder!")
    
    selected_qrs = random.sample(qr_files, num_qr)
    return [cv2.imread(qr, cv2.IMREAD_UNCHANGED) for qr in selected_qrs]

def generate_qr_image():
    """Generate an image with multiple QR codes of random sizes placed randomly on a background."""
    
    # Create the output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Create a blank white background
    background = np.ones((BACKGROUND_SIZE[1], BACKGROUND_SIZE[0], 3), dtype=np.uint8) * 255
    
    # Load QR codes
    qr_images = load_qr_images(QR_IMAGES_FOLDER, NUM_QR_CODES)

    # List to keep track of placed QR code bounding boxes (x, y, width, height)
    placed_boxes = []

    for qr_img in qr_images:
        # Choose a random size within the range
        random_size = random.randint(QR_MIN_SIZE, QR_MAX_SIZE)
        qr_resized = cv2.resize(qr_img, (random_size, random_size))

        # Attempt to find a non-overlapping position
        max_attempts = 100
        for attempt in range(max_attempts):
            x = random.randint(0, BACKGROUND_SIZE[0] - random_size)
            y = random.randint(0, BACKGROUND_SIZE[1] - random_size)
            new_box = (x, y, random_size, random_size)
            # Check if new_box overlaps any previously placed boxes
            overlap = False
            for box in placed_boxes:
                # Unpack boxes
                bx, by, bw, bh = box
                if (x < bx + bw and x + random_size > bx and 
                    y < by + bh and y + random_size > by):
                    overlap = True
                    break
            if not overlap:
                placed_boxes.append(new_box)
                break
        else:
            print("Warning: Could not find non-overlapping position for a QR code; skipping this one.")
            continue

        # Place QR code on background; if the QR image has an alpha channel, blend it properly
        # Check if QR code image has alpha channel (4 channels)
        if qr_resized.shape[2] == 4:
            alpha_channel = qr_resized[:, :, 3] / 255.0
            for c in range(0, 3):
                background[y:y+random_size, x:x+random_size, c] = (
                    alpha_channel * qr_resized[:, :, c] +
                    (1 - alpha_channel) * background[y:y+random_size, x:x+random_size, c]
                )
        else:
            background[y:y+random_size, x:x+random_size] = qr_resized

    # Save the generated image
    cv2.imwrite(OUTPUT_IMAGE, background)
    print(f"Generated image saved as {OUTPUT_IMAGE}")

# Run the generator
if __name__ == "__main__":
    generate_qr_image()
