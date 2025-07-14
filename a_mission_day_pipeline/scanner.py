# scanner.py

import os
import cv2
from detectors.qrdet_detector import detect_qr_regions_qrdet
from processors.enhance_clahe import enhance_image
from detectors.pyzbar_qr import decode_qr as decode_pyzbar
from detectors.opencv_qr import decode_qr_opencv
from utils.image_io import save_image
from utils.bbox_tools import crop_with_margin, compute_area, sort_by_smallest

def try_decoders(image_crop):
    # Try both decoders
    result = decode_pyzbar(image_crop)
    if result:
        return result[0]['data'], 'pyzbar'
    
    result = decode_qr_opencv(image_crop)
    if result:
        return result[0]['data'], 'opencv'

    return None, None

def process_site_image(image_path, output_dir, site_name="unknown"):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image load failed: {image_path}")

    all_detections = detect_qr_regions_qrdet(image)
    total_qrs = len(all_detections)
    print(f"[INFO] QR regions detected: {total_qrs}")

    decoded = False
    smallest_qr_data = {
        "decoded": False,
        "data": None,
        "decoder": None,
        "bbox": None,
        "area": None
    }

    if not all_detections:
        print("[WARN] No QR regions found.")
        return {**smallest_qr_data, "site": site_name, "total_detected": 0}

    # Sort by smallest bbox area first
    sorted_detections = sort_by_smallest(all_detections)

    for det in sorted_detections:
        bbox = det["bbox"]
        crop = crop_with_margin(image, bbox)
        save_image(crop, os.path.join(output_dir, "qr_crop.jpg"))

        decoded_text, decoder = try_decoders(crop)
        if not decoded_text:
            # Try enhanced image
            enhanced = enhance_image(crop)
            decoded_text, decoder = try_decoders(enhanced)

        # Set result (decoded or not)
        area = compute_area(bbox)
        smallest_qr_data.update({
            "bbox": bbox,
            "area": area,
            "data": decoded_text,
            "decoder": decoder,
            "decoded": bool(decoded_text)
        })
        break  # Only the smallest QR is relevant

    # Save final annotated image
    annotated = image.copy()
    if smallest_qr_data["bbox"]:
        x1, y1, x2, y2 = smallest_qr_data["bbox"]
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = smallest_qr_data["data"] if smallest_qr_data["decoded"] else "UNREADABLE"
        cv2.putText(annotated, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    save_image(annotated, os.path.join(output_dir, "annotated.jpg"))

    return {
        "site": site_name,
        "decoded": smallest_qr_data["decoded"],
        "data": smallest_qr_data["data"],
        "decoder": smallest_qr_data["decoder"],
        "bbox": smallest_qr_data["bbox"],
        "area": smallest_qr_data["area"],
        "total_detected": total_qrs
    }
