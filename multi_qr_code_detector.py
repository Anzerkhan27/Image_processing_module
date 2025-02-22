import cv2
import os
import numpy as np

# Configuration
INPUT_FOLDER = "qr_code_images"
IMAGE_NAME = "generated_qr_image.png"
INPUT_IMAGE_PATH = os.path.join(INPUT_FOLDER, IMAGE_NAME)

WINDOW_SIZE = 200  # Fixed sliding window size
STRIDE = 50  # Step size for moving the window

def detect_qr_codes_sliding_window(image_path):
    """Detect multiple QR codes using a simple sliding window approach."""

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Error: Could not load image {image_path}")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    qr_detector = cv2.QRCodeDetector()
    
    height, width = gray.shape
    detected_qrs = []

    # Slide the window across the image
    for y in range(0, height - WINDOW_SIZE + 1, STRIDE):
        for x in range(0, width - WINDOW_SIZE + 1, STRIDE):
            window = gray[y:y + WINDOW_SIZE, x:x + WINDOW_SIZE]
            retval, points = qr_detector.detect(window)

            if retval and points is not None:
                points = np.squeeze(points).astype(int)  # Remove extra dimension

                # Debugging: Print the shape of points
                print(f"🔍 Detected QR Code at ({x}, {y}) - Points Shape: {points.shape}")

                # Ensure points has exactly 4 points before processing
                if points.shape == (4, 2):
                    # Convert local window coordinates to full image coordinates
                    adjusted_points = points + np.array([x, y])

                    # Store detected QR code coordinates
                    detected_qrs.append(adjusted_points)

                    # Draw bounding box
                    for i in range(4):
                        cv2.line(image, tuple(adjusted_points[i]), tuple(adjusted_points[(i + 1) % 4]), (0, 255, 0), 3)
                else:
                    print(f"⚠ Unexpected points shape after squeeze: {points.shape}, skipping.")

    if not detected_qrs:
        print("❌ No QR codes detected.")

    # Display the image with detected QR codes
    cv2.imshow("Sliding Window QR Code Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Run the sliding window QR detector
if __name__ == "__main__":
    detect_qr_codes_sliding_window(INPUT_IMAGE_PATH)
