# image_processing/image_processor.py

import cv2
import os
import numpy as np
from pyzbar.pyzbar import decode
# At the top
from datetime import datetime
from image_processing.report_models import QRCodeModel, POIReportModel

class ImageProcessor:
    def __init__(self, config):
        self.config = config
        self.margin = config["margin"]
        self.sliding_window_size = config["sliding_window_size"]
        self.stride = config["sliding_stride"]
        self.output_folder = config["cropped_output_folder"]
        os.makedirs(self.output_folder, exist_ok=True)
        self.qr_detector = cv2.QRCodeDetector()

    def detect_single_qr(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not load image {image_path}")
            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        retval, points = self.qr_detector.detect(gray)

        if retval and points is not None:
            points = points.astype(int)
            x_min = max(0, min(points[0][:, 0]) - self.margin)
            x_max = min(image.shape[1], max(points[0][:, 0]) + self.margin)
            y_min = max(0, min(points[0][:, 1]) - self.margin)
            y_max = min(image.shape[0], max(points[0][:, 1]) + self.margin)

            cropped = image[y_min:y_max, x_min:x_max]
            output_path = os.path.join(self.output_folder, "qr_1.png")
            cv2.imwrite(output_path, cropped)
            print(f"✅ Single QR cropped and saved at {output_path} ({x_max - x_min}x{y_max - y_min}px)")
            return cropped
        else:
            print("❌ No QR code detected in image.")
            return None

    def detect_multi_qr_sliding(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not load image {image_path}")
            return

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        detected_qrs = []

        for y in range(0, height - self.sliding_window_size + 1, self.stride):
            for x in range(0, width - self.sliding_window_size + 1, self.stride):
                window = gray[y:y+self.sliding_window_size, x:x+self.sliding_window_size]
                retval, points = self.qr_detector.detect(window)

                if retval and points is not None:
                    points = np.squeeze(points).astype(int)
                    if points.shape == (4, 2):
                        adjusted = points + np.array([x, y])
                        detected_qrs.append(adjusted)
                        for i in range(4):
                            cv2.line(image, tuple(adjusted[i]), tuple(adjusted[(i+1)%4]), (0, 255, 0), 2)

        if detected_qrs:
            print(f"✅ Detected {len(detected_qrs)} QR codes using sliding window.")
        else:
            print("❌ No QR codes detected.")

        cv2.imshow("Multi-QR Detection (Sliding Window)", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detect_with_pyzbar(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not load image {image_path}")
            return

        decoded = decode(image)
        for obj in decoded:
            points = [(point.x, point.y) for point in obj.polygon]
            for i in range(len(points)):
                cv2.line(image, points[i], points[(i + 1) % len(points)], (0, 255, 0), 2)
            print(f"🔍 Pyzbar decoded: {obj.data.decode('utf-8')}")

        if decoded:
            cv2.imshow("Pyzbar QR Detection", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("❌ No QR codes detected by pyzbar.")

    def scan_qr_directory(self, folder_path):
        if not os.path.exists(folder_path):
            print(f"❌ Directory {folder_path} does not exist.")
            return

        files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not files:
            print("❌ No QR code images found in the folder.")
            return

        for f in files:
            path = os.path.join(folder_path, f)
            self.scan_qr_image(path)

    def scan_qr_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"⚠ Could not load image: {image_path}")
            return

        data, points, _ = self.qr_detector.detectAndDecode(image)
        if data:
            print(f"✅ Scanned '{os.path.basename(image_path)}': {data}")
        else:
            print(f"❌ No QR code decoded in '{os.path.basename(image_path)}'")




# Add this new method inside the ImageProcessor class
    def generate_poi_report(self, image_path: str, poi_id: int = 1) -> POIReportModel:
        from pyzbar.pyzbar import decode

        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not load image at {image_path}")

        decoded = decode(image)
        valid_qrs = []
        corrupted_qrs = []

        for obj in decoded:
            x, y, w, h = obj.rect
            area = w * h
            content = obj.data.decode('utf-8') if obj.data else None
            model = QRCodeModel(
                content=content,
                bbox=(x, y, w, h),
                area=area,
                is_valid=bool(content),
                quality_score=None  # Optional: add sharpness later
            )

            if model.is_valid:
                valid_qrs.append(model)
            else:
                corrupted_qrs.append(model)

        best_qr = min(valid_qrs, key=lambda qr: qr.area, default=None)
        score_estimate = 0.0
        if best_qr:
            max_area = max(qr.area for qr in valid_qrs)
            score_estimate = round(10 + 90 * (1 - best_qr.area / max_area), 2) if max_area else 90.0

        report = POIReportModel(
            poi_id=poi_id,
            timestamp=datetime.utcnow().isoformat(),
            image_name=os.path.basename(image_path),
            total_detected=len(decoded),
            valid_qrs=valid_qrs,
            corrupted_qrs=corrupted_qrs,
            best_qr=best_qr,
            score_estimate=score_estimate
        )

        return report

