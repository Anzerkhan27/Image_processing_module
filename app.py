# app.py


try:
    import streamlit as st
    import os
    import cv2
    import numpy as np
    from PIL import Image
    import io  # For in-memory download
    from image_processing.config import CONFIG
    from image_processing.qr_generator import QRGenerator
    from image_processing.image_processor import ImageProcessor

    print("✅ Streamlit server booting...")
except Exception as e:
    print(f" Failed at import-time: {e}")

# --- Title ---
st.title("Team Ray – QR Code Generator & Scanner 🚀")

# --- Initialize classes ---
generator = QRGenerator(CONFIG)
processor = ImageProcessor(CONFIG)

# --- Sidebar for options ---
option = st.sidebar.radio("Choose an action", ["Generate QR Image", "Scan Uploaded Image"])


# --- Helper function to process and display QR codes ---
def process_and_display_qr(image_path):
    """Process a given image path for QR detection and display results."""
    image = cv2.imread(image_path)
    from pyzbar.pyzbar import decode
    results = decode(image)

    if results:
        decoded_results = []
        smallest_area = None
        smallest_obj = None

        for obj in results:
            x, y, w, h = obj.rect
            area = w * h
            qr_content = obj.data.decode('utf-8')
            decoded_results.append((qr_content, x, y, w, h, area))

            if (smallest_area is None) or (area < smallest_area):
                smallest_area = area
                smallest_obj = (x, y, w, h)

        # Draw bounding boxes
        for qr_content, x, y, w, h, area in decoded_results:
            if (x, y, w, h) == smallest_obj:
                color = (255, 0, 255)  # Pink for the smallest
            else:
                color = (0, 255, 0)    # Green for normal

            cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)

        # Convert processed image to RGB
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Show the processed image
        st.image(processed_image, caption="Processed Image with QR Codes", use_container_width=True)

        # Diagnostics
        st.subheader("📋 Diagnostics:")
        st.info(f"🔹 Total QR Codes Found: {len(results)}")
        st.info(f"🔹 Total Scannable QR Codes: {len(decoded_results)}")

        if decoded_results:
            smallest_qr = min(decoded_results, key=lambda x: x[5])  # area
            st.success(f"🌸 Smallest QR Code Content: {smallest_qr[0]}")
        else:
            st.warning("❌ No scannable QR codes found.")

        # List all decoded QR codes
        st.subheader("🔍 Detected QR Codes:")
        for qr_content, _, _, _, _, _ in decoded_results:
            st.success(f"Decoded: {qr_content}")

    else:
        st.warning("❌ No QR codes detected.")


# --- Option 1: Generate QR Image ---
if option == "Generate QR Image":
    st.subheader("🎨 Generate Random QR Code Image")

    if st.button("Generate Image"):
        generator.generate_random()
        img_path = CONFIG["output_image"]

        # Save to session state for later scanning
        st.session_state["generated_image_path"] = img_path

        # Show generated image
        st.image(img_path, caption="Generated QR Image")
        st.success("✅ QR Image generated and displayed above!")

        # Download button
        generated_image = cv2.imread(img_path)
        generated_image = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(generated_image)
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Download Generated QR Code",
            data=byte_im,
            file_name="generated_qr_code.png",
            mime="image/png"
        )

    # --- Scan generated image button (below Generate + Download) ---
    if "generated_image_path" in st.session_state:
        if st.button("🔎 Scan Generated Image"):
            st.subheader("📋 Scan Result for Generated Image")
            img_path = st.session_state["generated_image_path"]
            process_and_display_qr(img_path)
    else:
        st.info("ℹ️ Please generate an image first before scanning.")

# --- Option 2: Scan Uploaded Image ---
elif option == "Scan Uploaded Image":
    st.subheader("📤 Upload an Image with QR Codes")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        uploaded_path = os.path.join("temp_upload.png")
        with open(uploaded_path, "wb") as f:
            f.write(uploaded_file.read())

        st.subheader("📋 Scan Result for Uploaded Image")
        process_and_display_qr(uploaded_path)
