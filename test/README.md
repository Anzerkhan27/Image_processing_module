

### 📁 `test/README.md`


# 🧪 QR Code Detection Test Module

This module provides a robust and modular testing pipeline for evaluating different QR code detection and decoding methods on real-world or synthetic images.

It is built for **Team Ray's Mars Rover Vision System**, enabling experimentation with classical and ML-based QR detectors in various image conditions (blurred, warped, low-contrast, etc.).

---

## 🚀 Purpose

- 📸 Process raw rover images to find QR codes
- 🤖 Compare multiple detection strategies:
  - OpenCV built-in detector
  - Pyzbar (ZBar-based)
  - QRDet (YOLOv8-based ML detector)
- 🔍 Visualize detection regions
- 📦 Log decoded results and save annotated images

---

## 🛠 Folder Structure

```

test/
│
├── test\_qr\_main.py              # 🔁 Main entrypoint with DETECTOR switch
├── ml\_detector/
│   └── qrdet\_detector.py        # 🧠 YOLOv8-based QR detector (QRDet)
├── processors/
│   ├── crop\_center.py           # 📐 Crops center region (ROI)
│   ├── enhance\_clahe.py         # ✨ Contrast enhancement via CLAHE
│   ├── perspective\_warp.py      # 🌀 Optional warp-to-rect for pyzbar
│   ├── detect\_pyzbar.py         # 🧾 QR decoding via pyzbar
│   └── opencv\_qr\_detector.py    # 🔍 QR decoding via OpenCV
├── utils/
│   └── image\_io.py              # 📁 Run folder creation, image saving
└── output\_images/
└── \[timestamped folders]    # 🖼 Annotated + enhanced outputs

````

---

## ✅ Supported Detectors

| Detector   | Module                    | Description                              |
|------------|---------------------------|------------------------------------------|
| `pyzbar`   | `detect_pyzbar.py`        | ZBar-based classical decoder             |
| `opencv`   | `opencv_qr_detector.py`   | OpenCV's QRCodeDetector (basic)          |
| `qrdet`    | `qrdet_detector.py`       | YOLOv8 ML model for QR region detection  |

---

## ⚙️ How to Use

### 1. Install dependencies:

```bash
pip install -r requirements.txt
pip install qrdet
````

### 2. Run the module on a test image:

```bash
python -m test.test_qr_main qr_code_images/IMG-20250530-WA0010.jpg
```

### 3. Choose detection strategy:

Edit this in `test_qr_main.py`:

```python
DETECTOR = "qrdet"  # or "pyzbar", "opencv"
```

---

## 🖼 Output Files

Each run creates a folder:
📁 `test/output_images/YYYYMMDD_HHMMSS/`
Which may include:

* `02_enhanced.jpg` – CLAHE-enhanced ROI
* `04_final_annotated.jpg` – Detections with bounding boxes

---

## 🧩 Extending

* Add new detectors to `processors/` or `ml_detector/`
* Integrate with `summary.json` generator
* Add batch mode to test all images in a folder

---

## 📬 Contact

Built by **Anzer Khan** – Software Lead, Team Ray
📧 [anzerkhan27@gmail.com](mailto:anzerkhan27@gmail.com)
🏛️ University of Huddersfield – MSc AI

---

*Built for planetary precision.* 🚀

```

```
