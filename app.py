import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image
import io
import json
from image_processing.config import CONFIG
from image_processing.qr_generator import QRGenerator
from image_processing.image_processor import ImageProcessor

st.title("Team Ray – QR Code Generator & Scanner 🚀")

# Initialize generator and processor
generator = QRGenerator(CONFIG)
processor = ImageProcessor(CONFIG)

# Sidebar for selecting action
option = st.sidebar.radio("Choose an action", ["Generate QR Image", "Scan Uploaded Image"])


def process_and_display_qr(image_path: str):
    """Detect and annotate QR codes, then display the image and diagnostics."""
    image = cv2.imread(image_path)
    from pyzbar.pyzbar import decode
    results = decode(image)

    decoded_results = []
    if results:
        smallest_area = None
        smallest_obj = None

        for obj in results:
            x, y, w, h = obj.rect
            area = w * h
            qr_content = obj.data.decode('utf-8') if obj.data else None
            decoded_results.append((qr_content, x, y, w, h, area))

            if (smallest_area is None) or (area < smallest_area):
                smallest_area = area
                smallest_obj = (x, y, w, h)

        # Draw bounding boxes
        for content, x, y, w, h, area in decoded_results:
            color = (255, 0, 255) if (x, y, w, h) == smallest_obj else (0, 255, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)

        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(processed_image, caption="Processed Image with QR Codes", use_container_width=True)

        # Diagnostics
        st.subheader("📋 Diagnostics:")
        st.info(f"🔹 Total QR Codes Found: {len(results)}")
        st.info(f"🔹 Total Scannable QR Codes: {len(decoded_results)}")
        if decoded_results:
            smallest_qr = min(decoded_results, key=lambda x: x[5])
            st.success(f"🌸 Smallest QR Code Content: {smallest_qr[0]}")
        else:
            st.warning("❌ No scannable QR codes found.")

        st.subheader("🔍 Detected QR Codes:")
        for content, _, _, _, _, _ in decoded_results:
            st.success(f"Decoded: {content}")
    else:
        st.warning("❌ No QR codes detected.")


# Option 1: Generate and then Scan Generated Image
if option == "Generate QR Image":
    st.subheader("🎨 Generate Random QR Code Image")

    if st.button("Generate Image"):
        generator.generate_random()
        img_path = CONFIG["output_image"]
        st.session_state["generated_image_path"] = img_path

        # Display and download generated image
        st.image(img_path, caption="Generated QR Image", use_container_width=True)
        st.success("✅ QR Image generated and displayed above!")

        pil_img = Image.fromarray(cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB))
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        st.download_button(
            label="📥 Download Generated QR Code",
            data=buf.getvalue(),
            file_name="generated_qr_code.png",
            mime="image/png"
        )

    if "generated_image_path" in st.session_state:
        if st.button("Scan Generated Image"):
            st.subheader("📋 Scan Result for Generated Image")
            img_path = st.session_state["generated_image_path"]
            process_and_display_qr(img_path)

            # Generate structured report and display it
            report = processor.generate_poi_report(img_path, poi_id=1)
            st.subheader("🔖 Structured POI Report")
            st.json(report.dict())

            # Save JSON report to disk
            reports_dir = "reports"
            os.makedirs(reports_dir, exist_ok=True)
            ts = report.timestamp.replace(":", "-")
            report_path = os.path.join(reports_dir, f"poi_{report.poi_id}_{ts}.json")
            with open(report_path, "w") as f:
                f.write(report.json(indent=2))
            st.success(f"✅ Report saved to `{report_path}`")
    else:
        st.info("ℹ️ Please generate an image first before scanning.")

# Option 2: Upload and scan an external image
elif option == "Scan Uploaded Image":
    st.subheader("📤 Upload an Image with QR Codes")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Save upload to temp file
        uploaded_path = "temp_upload.png"
        with open(uploaded_path, "wb") as f:
            f.write(uploaded_file.read())

        st.subheader("📋 Scan Result for Uploaded Image")
        process_and_display_qr(uploaded_path)

        # Generate structured report and display it
        report = processor.generate_poi_report(uploaded_path, poi_id=1)
        st.subheader("🔖 Structured POI Report")
        st.json(report.dict())

        # Save JSON report to disk
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        ts = report.timestamp.replace(":", "-")
        report_path = os.path.join(reports_dir, f"poi_{report.poi_id}_{ts}.json")
        with open(report_path, "w") as f:
            f.write(report.json(indent=2))
        st.success(f"✅ Report saved to `{report_path}`")
