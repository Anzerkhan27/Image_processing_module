import cv2

def decode_qr_opencv(img):
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)

    if data and points is not None:
        # Format points to match pyzbar-style
        points = points.astype(int).reshape(-1, 2)
        return [{
            "data": data,
            "points": [(int(x), int(y)) for (x, y) in points]
        }]
    else:
        return []
