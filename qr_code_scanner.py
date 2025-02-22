
import cv2
import os

# Configuration
INPUT_FOLDER = "qr_dataset"  # Folder where cropped QR codes are stored

def scan_qr_codes(folder_path):
    """Scans all QR code images in the specified folder and prints their content."""

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' does not exist.")
        return

    # List all image files in the folder
    qr_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not qr_files:
        print("❌ No QR code images found in the folder.")
        return

    qr_detector = cv2.QRCodeDetector()

    for qr_file in qr_files:
        image_path = os.path.join(folder_path, qr_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"⚠ Warning: Could not load image {image_path}")
            continue

        # Detect and decode the QR code
        data, points, _ = qr_detector.detectAndDecode(image)

        if points is not None and data:
            print(f"✅ QR Code detected in '{qr_file}'! Content: {data}")
        else:
            print(f"❌ No QR code detected in '{qr_file}' or could not be decoded.")

# Run QR code scanning
if __name__ == "__main__":
    scan_qr_codes(INPUT_FOLDER)
