import cv2
import sys
from test.utils.image_io import init_run_dir, save_image
from test.processors.crop_center import crop_center
from test.processors.enhance_clahe import enhance_image
from test.processors.perspective_warp import detect_and_warp_qr
from test.processors.detect_pyzbar import decode_qr
from test.processors.opencv_qr_detector import decode_qr_opencv


def draw_polygons(image, results):
    for r in results:
        points = r["points"]
        for i in range(len(points)):
            pt1 = tuple(points[i])
            pt2 = tuple(points[(i + 1) % len(points)])
            cv2.line(image, pt1, pt2, (0, 255, 0), 2)
    return image

def main(img_path):
    init_run_dir()
    img = cv2.imread(img_path)
    if img is None:
        print("[ERROR] Could not load image.")
        return

    roi, ox, oy = crop_center(img)
    enhanced = enhance_image(roi)
    warped = detect_and_warp_qr(enhanced)

    results = []
    annotated_img = img.copy()

    if warped is not None:
        results = decode_qr(warped)
        if results:
            print("[INFO] QR decoded from warped image.")
            annotated_img = warped.copy()
    else:
        print("[WARN] No contour found, fallback to ROI decoding.")
        results = decode_qr(enhanced)
            # Step 1: Try OpenCV on enhanced ROI
    results = decode_qr_opencv(enhanced)
    if results:
        print("[INFO] QR decoded using OpenCV.")
        for r in results:
            r["points"] = [(x + ox, y + oy) for (x, y) in r["points"]]
        annotated_img = draw_polygons(img.copy(), results)
    else:
        # Step 2: Try perspective-warp + pyzbar
        warped = detect_and_warp_qr(enhanced)
        if warped is not None:
            results = decode_qr(warped)
            if results:
                print("[INFO] QR decoded from warped image using pyzbar.")
                annotated_img = warped.copy()
        else:
            print("[WARN] No contour found, fallback to pyzbar on ROI.")
            results = decode_qr(enhanced)
            if results:
                for r in results:
                    r["points"] = [(x + ox, y + oy) for (x, y) in r["points"]]
                annotated_img = draw_polygons(img.copy(), results)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m test.test_qr_main <path_to_image>")
    else:
        main(sys.argv[1])
