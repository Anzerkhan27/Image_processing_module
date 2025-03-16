import cv2
import os

# Configuration
INPUT_FOLDER = "qr_code_images"  # Folder where original images are stored
OUTPUT_FOLDER = "cropped_qr_codes"  # Folder to store cropped QR codes
IMAGE_NAME = "test.jpg"  # Name of the image to process
INPUT_IMAGE_PATH = os.path.join(INPUT_FOLDER, IMAGE_NAME)
OUTPUT_IMAGE_PATH = os.path.join(OUTPUT_FOLDER, "qr_1.png")
MARGIN = 10  # Extra pixels to add around the cropped QR code

def detect_and_crop_qr(image_path, output_path, margin=MARGIN):
    """Detects a single QR code in an image, crops it with margin, prints its size, and saves it."""

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Error: Could not load image {image_path}")
        return False

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize OpenCV's QR Code Detector
    qr_detector = cv2.QRCodeDetector()

    # Detect QR code
    retval, points = qr_detector.detect(gray)

    if retval and points is not None:
        points = points.astype(int)

        # Extract bounding box coordinates with margin
        x_min = max(0, min(points[0][:, 0]) - margin)
        x_max = min(image.shape[1], max(points[0][:, 0]) + margin)
        y_min = max(0, min(points[0][:, 1]) - margin)
        y_max = min(image.shape[0], max(points[0][:, 1]) + margin)

        # Crop the QR code from the image with margin
        cropped_qr = image[y_min:y_max, x_min:x_max]

        # Get dimensions of cropped QR code
        height, width = cropped_qr.shape[:2]

        # Print size of cropped QR code
        print(f"📏 Cropped QR code size: {width}x{height} pixels")

        # Create output directory if not exists
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # Save cropped QR code
        cv2.imwrite(output_path, cropped_qr)
        print(f"✅ Cropped QR code saved as {output_path} with {margin}px margin")
        return True

    else:
        print("❌ No QR code detected.")
        return False

# Run QR code detection and cropping
if __name__ == "__main__":
    detect_and_crop_qr(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH)
