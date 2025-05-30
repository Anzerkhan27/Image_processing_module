from qrdet import QRDetector

# Initialize once
detector = QRDetector(model_size='s')  # 'n', 's', 'm', 'l'

def detect_qr_regions_qrdet(img_bgr):
    # QRDet expects BGR if is_bgr=True
    detections = detector.detect(image=img_bgr, is_bgr=True)

    regions = []
    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox_xyxy"])
        confidence = det["confidence"]
        if confidence > 0.4:
            regions.append({
                "bbox": (x1, y1, x2, y2),
                "conf": confidence
            })
    return regions
