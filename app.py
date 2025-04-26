# app.py

import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image
import io  # NEW IMPORT for in-memory file
from image_processing.config import CONFIG
from image_processing.qr_generator import QRGenerator
from image_processing.image_processor import ImageProcessor

st.title("Team Ray – QR Code Generator & Scanner 🚀")

# Initialize classes
generator = QRGenerator(CONFIG)
processor = ImageProcessor(CONFIG)

# Sidebar for options
option = st.sidebar.radio("Choose an action", ["Generate QR Image", "Scan Uploaded Image"])

if option == "Generate QR Image":
    st.subheader("🎨 Generate Random QR Code Image")
    if st.button("Generate Image"):
        generator.generate_random()
        img_path = CONFIG["output_image"]

        # Show generated image
        st.image(img_path, caption="Generated QR Image")
        st.success("QR Image generated and displayed above!")

        # ✅ ADD THIS: Enable download of generated QR image
        # Read the image back
        generated_image = cv2.imread(img_path)
        # Convert BGR to RGB
        generated_image = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
        # Convert to PIL image
        pil_image = Image.fromarray(generated_image)
        # Save to in-memory file
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Streamlit download button
        st.download_button(
            label="📥 Download Generated QR Code",
            data=byte_im,
            file_name="generated_qr_code.png",
            mime="image/png"
        )

elif option == "Scan Uploaded Image":
    st.subheader("📤 Upload an Image with QR Codes")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        # Save uploaded image to disk
        uploaded_path = os.path.join("temp_upload.png")
        with open(uploaded_path, "wb") as f:
            f.write(uploaded_file.read())
            st.image(uploaded_path, caption="Uploaded Image", use_container_width=True)
      
        st.markdown("---")
        st.subheader("🔍 Detected QR Codes")

        # Pyzbar decoding
        st.text("Pyzbar Decoding:")
        image = cv2.imread(uploaded_path)
        from pyzbar.pyzbar import decode
        results = decode(image)
        if results:
            for obj in results:
                st.success(f"Decoded: {obj.data.decode('utf-8')}")
        else:
            st.warning("No QR codes decoded by Pyzbar.")

        # OpenCV fallback
        st.text("OpenCV Detection:")
        processor.scan_qr_image(uploaded_path)
