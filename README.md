
# 🤖 Team Ray – QR Code Detection & Analysis Module

Welcome to the **QR Code Detection & Image Processing Module** for **Team Ray**, the University of Huddersfield’s aerospace team competing in the **UKSEDS Olympus Rover Trials (ORT) 2024–25**.

This codebase powers the **AI-driven vision system** for our Mars Rover prototype. It simulates how the rover detects, decodes, and prioritizes QR codes placed on Martian rocks at geological points of interest (POIs).

> 📌 **Built & Maintained by:**  
> 🧑‍💻 *Mohammad Anzer Khan* – Software Lead, Team Ray  
> 🎓 *MSc Artificial Intelligence, University of Huddersfield*

---

## 🧠 Project Purpose

This module enables our rover to:
- 📸 Capture still images of Martian terrain (rocks with QR codes)
- 🧠 Detect **multiple QR codes** per image
- 🔍 Decode all QR codes and **select the smallest valid one**
- 📦 Generate a structured summary packet for submission

It is a **mission-critical component** of the imaging pipeline, directly influencing scoring in the competition.

---

## 🌌 Bigger Mission Context: Olympus Rover Trials 2024–25

The UKSEDS ORT simulates a **Mars pre-landing reconnaissance mission**. The rover must:
- Navigate rugged Martian terrain 🌄
- Detect rocks with QR codes 🪨📷
- Send back images and decoded data via wireless comms 🌐

🔬 **Scoring is highest** when we:
- Capture the smallest successfully scanned QR 📈
- Submit both the image and decoded content 📑

This repository simulates the **AI-powered image processing** part of that workflow.

---

## 🛠️ What’s in This Repo?

| Module/File                     | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| `image_processing/`            | Core logic: QR detection, cropping, decoding, summary generation            |
| `qr_dataset/`                  | QR images used for generating test scenarios                                |
| `qr_code_images/`              | Output folder for generated composite test images                           |
| `cropped_qr_codes/`            | Saved cropped versions of detected QR codes                                 |
| `app.py`                       | 🧪 **Streamlit web app** for testing the pipeline interactively              |
| `main_pipeline.py`             | CLI-based execution of the core pipeline                                    |
| `config.py`                    | Configurable parameters (QR sizes, paths, stride, margin, etc.)             |
| `Dockerfile`                   | Container config for reproducible deployment                                |
| `requirements.txt`             | Python dependencies                                                         |

---

## 🚀 How the Pipeline Works

1. **Image Input**: Accepts either:
   - Generated synthetic image with multiple QR codes
   - Uploaded real-world test image (simulating camera capture)

2. **Detection**: Detects all visible QR codes using OpenCV and Pyzbar

3. **Decoding & Ranking**:
   - Decodes each QR code
   - Calculates bounding box area
   - Chooses the **smallest successfully decoded QR**

4. **Summary Packet**:
   - Stores QR data and metadata in a `.json` file
   - Saves a bounding-box annotated image
   - Optionally saves cropped version of QR

5. **Visualization**:
   - Streamlit app allows team to test, visualize, and download results live

---


## 🧪 Live Testing with Streamlit

You can try out the interactive web app here:

👉 **[Live Streamlit App – Try It Now](https://imageprocessingmodule-production.up.railway.app/)**

To run locally:

```bash
streamlit run app.py




### ✅ Features:

* Generate and download random QR images
* Upload real rover images for detection
* Annotate and view all detected QR codes
* Automatically highlight the best-scoring QR
* View or download the `.json` summary

---

## 📦 JSON Output Example

```json
{
  "timestamp": "2025-05-04T15:23:00",
  "image": "temp_upload.png",
  "total_detected": 3,
  "decoded_qrs": [
    {"content": "SiO2-78%", "bbox": [100,120,80,80], "area": 6400},
    {"content": "Fe2O3-12%", "bbox": [230,180,60,60], "area": 3600}
  ],
  "best_qr": {
    "content": "Fe2O3-12%",
    "bbox": [230,180,60,60],
    "area": 3600
  }
}
```

---

## 🧩 How This Fits Into the Full Rover Pipeline

| Stage                   | System                        | Description                                       |
| ----------------------- | ----------------------------- | ------------------------------------------------- |
| Image Capture           | 📷 Digital Camera (OV5640)    | Triggered via ESP32, takes still shot of POI rock |
| Image Transmission      | 📡 Wi-Fi Module               | Sends image to base station                       |
| Image Processing (this) | 💻 Python + OpenCV + Pyzbar   | Detects, decodes, and summarizes QR code data     |
| Command Submission      | 🧠 Manual or automated upload | Image + data sent to judges                       |

---

## 🛠️ What I'm Currently Working On

* ✅ Sliding window multi-QR detection
* ✅ Smallest QR selection based on bounding box area
* ✅ Streamlit app for testing
* 🔄 **Next Up**:

  * JSON submission generation
  * Camera integration simulation (OV5640 → pipeline hook)
  * Resilience testing on noisy/blurred images

---

## 👨‍💻 Skills Demonstrated

* 🧠 **Computer Vision** – OpenCV pipelines, multi-object detection
* 🤖 **AI Readiness** – Laying groundwork for ML-based quality scoring
* 🌐 **Software Engineering** – Modular code, config-driven design
* ⚙️ **Tooling** – Docker, Streamlit, real-time testing UX
* 📈 **Team Collaboration** – Used by teammates to validate detection success

---

## 📌 Future Improvements

* [ ] Real-time camera feed integration via socket or FTP
* [ ] Confidence scoring for ambiguous QR scans
* [ ] Integration with mission control dashboard

---

## 👋 Get in Touch

📧 [anzerkhan27@gmail.com](mailto:anzerkhan27@gmail.com)
🔗 [LinkedIn – Anzer Khan](https://linkedin.com/in/anzer-khan-31a14a209)
🏛️ University of Huddersfield – MSc Artificial Intelligence

---

*This repository is proudly maintained as part of the Mars Rover mission by Team Ray. Built with clarity, purpose, and space-grade ambition.* 🚀



