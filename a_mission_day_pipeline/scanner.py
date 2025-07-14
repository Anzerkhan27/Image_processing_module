# scanner.py

import os
import cv2
import json
from detectors.qrdet_detector import detect_qr_regions_qrdet
from processors.enhance_clahe import enhance_image
from detectors.pyzbar_qr import decode_qr as decode_pyzbar
from detectors.opencv_qr import decode_qr_opencv
from utils.image_io import save_image
from utils.bbox_tools import crop_with_margin, compute_area, sort_by_smallest


def try_decoders(image_crop):
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

    if not all_detections:
        print("[WARN] No QR regions found.")
        return {
            "site": site_name,
            "decoded": False,
            "data": None,
            "decoder": None,
            "bbox": None,
            "area": None,
            "total_detected": 0
        }

    sorted_detections = sort_by_smallest(all_detections)
    region_logs = []
    decoded_candidates = []

    for idx, det in enumerate(sorted_detections):
        bbox = det["bbox"]
        area = compute_area(bbox)
        crop = crop_with_margin(image, bbox)

        decoded_text, decoder = try_decoders(crop)
        if not decoded_text:
            enhanced = enhance_image(crop)
            decoded_text, decoder = try_decoders(enhanced)

        region_logs.append({
            "index": idx + 1,
            "bbox": bbox,
            "area": area,
            "decoded": bool(decoded_text),
            "data": decoded_text if decoded_text else None,
            "decoder": decoder
        })

        if decoded_text:
            decoded_candidates.append({
                "index": idx + 1,
                "bbox": bbox,
                "area": area,
                "data": decoded_text,
                "decoder": decoder,
                "decoded": True,
                "crop": crop
            })

    # Determine which to submit
    if decoded_candidates:
        final = sorted(decoded_candidates, key=lambda d: d["area"])[0]
        crop_out = os.path.join(output_dir, "qr_crop.jpg")
        save_image(final["crop"], crop_out)
    else:
        fallback = sorted_detections[0]
        bbox = fallback["bbox"]
        area = compute_area(bbox)
        crop = crop_with_margin(image, bbox)
        crop_out = os.path.join(output_dir, "qr_crop.jpg")
        save_image(crop, crop_out)
        final = {
            "index": 1,
            "bbox": bbox,
            "area": area,
            "data": None,
            "decoder": None,
            "decoded": False
        }

    # Annotate and save
    annotated = image.copy()
    x1, y1, x2, y2 = final["bbox"]
    label = final["data"] if final["decoded"] else "UNREADABLE"
    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(annotated, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    save_image(annotated, os.path.join(output_dir, "annotated.jpg"))

    # Write full summary JSON
    summary_json = {
        "site": site_name,
        "total_detected": total_qrs,
        "submitted_qr_index": final["index"],
        "regions": region_logs
    }

    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(summary_json, f, indent=2)

    return {
        "site": site_name,
        "decoded": final["decoded"],
        "data": final["data"],
        "decoder": final["decoder"],
        "bbox": final["bbox"],
        "area": final["area"],
        "total_detected": total_qrs
    }
