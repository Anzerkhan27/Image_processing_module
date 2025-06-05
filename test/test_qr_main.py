import cv2
import sys
from test.utils.image_io import init_run_dir, save_image
from test.ml_detector.qrdet_detector import detect_qr_regions_qrdet

def draw_boxes(image, results):
    for r in results:
        x1, y1, x2, y2 = r["bbox"]
        conf = r.get("conf", 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return image

def main(img_path):
    run_dir = init_run_dir()
    img = cv2.imread(img_path)
    if img is None:
        print("[ERROR] Could not load image.")
        return

    detections = detect_qr_regions_qrdet(img)
    if not detections:
        print("[FAIL] No QR codes detected.")
        return

    print(f"[INFO] QRDet detected {len(detections)} region(s).")
    annotated = draw_boxes(img.copy(), detections)
    save_image(annotated, "04_final_annotated.jpg")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m test.test_qr_main <path_to_image>")
    else:
        main(sys.argv[1])
