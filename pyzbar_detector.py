import cv2
from pyzbar.pyzbar import decode

# Path to the image
image_path = "qr_code_images/image.png"


# Load the image
image = cv2.imread(image_path)
if image is None:
    print(f"Error: Unable to load image from {image_path}")
    exit(1)

# Decode the QR codes in the image
decoded_objects = decode(image)



# Loop over all detected QR codes and draw bounding boxes
for obj in decoded_objects:
    # Get the bounding box coordinates
    points = obj.polygon
    # If the points form a quad (expected), convert to a list of tuples
    pts = [(point.x, point.y) for point in points]
    
    # Draw the bounding box by connecting the points
    if len(pts) > 0:
        for i in range(len(pts)):
            pt1 = pts[i]
            pt2 = pts[(i + 1) % len(pts)]
            cv2.line(image, pt1, pt2, (0, 255, 0), 2)
    
    # Print the decoded data
    print("Decoded Data:", obj.data.decode("utf-8"))

# Display the output image with bounding boxes
cv2.imshow("Detected QR Codes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
