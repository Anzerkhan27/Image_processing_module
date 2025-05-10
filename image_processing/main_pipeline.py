#image_processing/main_pipeline.py

from image_processing.config import CONFIG
from image_processing.qr_generator import QRGenerator
from image_processing.image_processor import ImageProcessor

def run_pipeline():
    # Step 1: Generate Image
    generator = QRGenerator(CONFIG)
    generator.generate_random()  # or generator.generate_fixed()

    # Step 2: Detect and Process QR Codes
    processor = ImageProcessor(CONFIG)
    image_path = CONFIG["output_image"]

   # processor.detect_multi_qr_sliding(image_path)
   # processor.detect_with_pyzbar(image_path)
    report = processor.generate_poi_report(image_path, poi_id=1)
    print(report.json(indent=2))
    processor.scan_qr_image(image_path)

if __name__ == "__main__":
    run_pipeline()
