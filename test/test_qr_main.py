import cv2
import sys

from test.utils.image_io import init_run_dir, save_image
from test.processors.crop_center import crop_center
from test.processors.enhance_clahe import enhance_image
from test.processors.perspective_warp import detect_and_warp_qr
from test.processors.detect_pyzbar import decode_qr as decode_qr_pyzbar
from test.processors.opencv_qr_detector import decode_qr_opencv
from test.ml_detector.qrdet_detector import detect_qr_regions_qrdet

# ▶️ Switch this to: "qrdet", "pyzbar", or "opencv"
DETECTOR = "qrdet"

def draw_polygons(image, results):
    for r in results:
        if "points" in r:
            pts = r["points"]
            for i in range(len(pts)):
                pt1 = tuple(pts[i])
                pt2 = tuple(pts[(i + 1) % len(pts)])
                cv2.line(image, pt1, pt2, (0, 255, 0), 2)
        elif "bbox" in r:
            x1, y1, x2, y2 = r["bbox"]
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return image

def main(img_path):
    init_run_dir()
    img = cv2.imread(img_path)
    if img is None:
        print("[ERROR] Could not load image.")
        return

    results = []
    annotated_img = img.copy()

    if DETECTOR == "qrdet":
        qr_regions = detect_qr_regions_qrdet(img)
        if qr_regions:
            print(f"[INFO] QRDet detected {len(qr_regions)} region(s)")
            for r in qr_regions:
                x1, y1, x2, y2 = r["bbox"]
                cropped = img[y1:y2, x1:x2]
                decoded = decode_qr_pyzbar(cropped)
                if decoded:
                    r["data"] = decoded[0]["data"]
                    print(f"[QR] {r['data']}")
                else:
                    print(f"[WARN] Region at {r['bbox']} not decoded.")
            results = qr_regions
        else:
            print("[FAIL] QRDet found no QR codes.")

    elif DETECTOR == "pyzbar":
        roi, ox, oy = crop_center(img)
        enhanced = enhance_image(roi)
        warped = detect_and_warp_qr(enhanced)
        if warped is not None:
            results = decode_qr_pyzbar(warped)
            annotated_img = warped.copy()
            print("[INFO] QR found using pyzbar (warped).")
        else:
            print("[WARN] No contour found, fallback to pyzbar on ROI.")
            results = decode_qr_pyzbar(enhanced)
            for r in results:
                r["points"] = [(x + ox, y + oy) for (x, y) in r["points"]]
            annotated_img = draw_polygons(annotated_img, results)

        for r in results:
            print(f"[QR] {r['data']}")

    elif DETECTOR == "opencv":
        roi, ox, oy = crop_center(img)
        enhanced = enhance_image(roi)
        results = decode_qr_opencv(enhanced)
        for r in results:
            r["points"] = [(x + ox, y + oy) for (x, y) in r["points"]]
        if results:
            print("[INFO] QR found using OpenCV.")
            annotated_img = draw_polygons(annotated_img, results)
            for r in results:
                print(f"[QR] {r['data']}")
        else:
            print("[FAIL] OpenCV failed to decode QR.")

    if results:
        annotated_img = draw_polygons(annotated_img, results)
        save_image(annotated_img, "04_final_annotated.jpg")
    else:
        print("[FAIL] QR not decoded.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m test.test_qr_main <path_to_image>")
    else:
        main(sys.argv[1])
