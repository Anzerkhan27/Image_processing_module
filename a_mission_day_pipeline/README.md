
---

# ✅ Finalized Image Processing Pipeline (Redesigned)

## 🏁 **Mission Goal**

> For each geological site, detect all QR codes, identify the **smallest QR code region**, and generate a **PDF report** — whether or not decoding is successful.

---

## 🎯 Primary Objectives (Scoring-Aligned)

| Objective                                                    | Description |
| ------------------------------------------------------------ | ----------- |
| ✅ Detect all QR codes in each image                          |             |
| ✅ Extract the **smallest** bounding box region               |             |
| ✅ Attempt decoding (raw + enhanced)                          |             |
| ✅ Save detection/decoding metadata                           |             |
| ✅ Estimate distance to QR (if feasible)                      |             |
| ✅ Generate **per-site PDF report**, always (even on failure) |             |

---

## 🔄 Pipeline Plan — Scoring + Reporting Optimized

### **1. Input Handling**

* Accept a **folder of site images** or a single image
* Prepare output directory structure per site

---

### **2. Detection Stage**

* Use **QRDet** to detect **all QR-like regions**
* Return list of bounding boxes with confidence
* Compute **area** for each bbox

---

### **3. Decoding Stage (per bbox, sorted smallest-first)**

For each bbox:

* Crop region (with margin)
* Try decoding via:

  * `pyzbar`
  * `opencv`
* If failed:

  * Enhance (CLAHE + sharpening)
  * Retry decoding

🧠 **STOP at first successful decode**

---

### **4. Postprocessing**

* If decode succeeded:

  * Parse `site`, `rock`, etc.
* If decode failed:

  * Mark `decoded: false`, still log bbox
* Estimate distance (optional):

  $$
  \text{distance} = \frac{f \cdot \text{QR\_real\_width}}{\text{pixel\_width}}
  $$

---

### **5. Data Aggregation**

* Store:

  * Site image name
  * Number of total detected QR regions
  * Decoded or not
  * Smallest QR bbox + area
  * Estimated distance (if valid)
  * Mark if likely dummy QR
* Save this in `.json` and `.csv` format

---

### **6. PDF Report Generation (per site)**

#### 📄 PDF Layout

| Section         | Contents                                              |
| --------------- | ----------------------------------------------------- |
| 🏷️ Site Header | Site name, image name, date, operator name            |
| 🖼️ Image View  | Annotated site image with all QR regions              |
| 🔎 Smallest QR  | Cropped image of smallest QR, decoded text (if any)   |
| 📊 Stats Table  | Total QR codes, dummy count, decoded status, distance |
| ❌ Notes         | “QR could not be decoded”, “Possible dummy code”      |

> 📁 Output: `site_C3_report.pdf`

---

## 📁 Final Output Structure

```
output/
└── site_C3/
    ├── IMG_003.jpg
    ├── qr_crop.jpg
    ├── annotated.jpg
    ├── summary.json
    ├── summary.csv
    └── site_C3_report.pdf   ✅
```

---

## 🧩 What You'll Need Code-wise

| Script/Module           | Role                                                 |
| ----------------------- | ---------------------------------------------------- |
| `main_runner.py`        | Entry point: handles input folder, triggers pipeline |
| `scanner.py`            | Core logic: detect, decode, enhance                  |
| `bbox_tools.py`         | Area, sorting, margin cropping                       |
| `report_writer.py`      | Writes JSON + CSV summary                            |
| `pdf_reporter.py`       | Generates PDF from summary and images 🆕             |
| `distance_estimator.py` | Optional: simple trig-based estimator                |

---

## ✅ Your Immediate Next Step

Would you like me to:

1. Start with the **`main_runner.py` + `scanner.py` base structure**?
2. Build a **starter template for `pdf_reporter.py`**?
3. Provide a **test dataset + dummy site output folder** to simulate?


Absolutely — here's a full, clear `README.md` to document your current pipeline setup, making it easy to pick up development later or onboard a teammate.

---

## 📘 `README.md` – Olympus QR Processing Pipeline

---

### 🛰️ Project: **Olympus Mission Day – QR Code Detection & Reporting System**

This repo implements the **image processing pipeline** for the Olympus rover competition, focusing on:

* 🔍 Detecting QR codes in aerial rover imagery
* 📦 Decoding QR data for mission scoring
* 🖼 Annotating detections
* 📝 Generating per-site summary reports (PDF & JSON)

> ✔️ Aligns with Airbus scoring rules:
> ✅ Submit the **smallest readable** QR per site
> 🔁 Fallback to **smallest detected QR** if none decode

---

### 📁 Directory Structure

```
.
├── main_runner.py               # 🚀 CLI entrypoint to run the pipeline
├── scanner.py                   # 🔍 Detects, decodes, selects & logs QR info
├── pdf_reporter.py              # 📝 Generates per-site PDF report
├── output/
│   └── C1/                      # Site folder with results & report
│       ├── annotated.jpg
│       ├── qr_crop.jpg
│       ├── summary.json
│       └── C1_report.pdf
├── detectors/
│   ├── qrdet_detector.py        # 📦 YOLOv8-based QR detection
│   ├── pyzbar_qr.py             # 🤖 pyzbar decoder
│   └── opencv_qr.py             # 🧼 OpenCV fallback decoder
├── processors/
│   └── enhance_clahe.py         # ✨ CLAHE + sharpen enhancement
├── utils/
│   ├── bbox_tools.py            # 📐 Sorting, cropping, area utils
│   └── image_io.py              # 💾 Saving images, folders
├── test_images/                 # 🧪 Sample test input images
└── README.md                    # 📘 This doc
```

---

### ⚙️ Requirements

Install once:

```bash
pip install -r requirements.txt
pip install qrdet reportlab pillow opencv-python pyzbar
```

---

### ✅ Running the Pipeline

```bash
python main_runner.py test_images/qr_image_1.png --site C1
```

This will:

* Detect QR regions
* Try decoding all
* Choose the **smallest successful decode**
* Fallback to **smallest overall** if none decode
* Save:

  * Annotated image
  * Crop of chosen QR
  * `summary.json`
  * PDF report

---

### 📝 Generating PDF Report

```bash
python pdf_reporter.py output/C1
```

This creates:

```
output/C1/C1_report.pdf
```

---

### 📂 Output Example

```
output/C1/
├── annotated.jpg         # All boxes drawn, main QR labeled
├── qr_crop.jpg           # Crop of smallest readable QR
├── summary.json          # Metadata (decoded, bbox, area)
└── C1_report.pdf         # 📝 PDF summary
```

---

### 🔍 Summary JSON Structure

```json
{
  "site": "C1",
  "total_detected": 3,
  "submitted_qr_index": 2,
  "regions": [
    {
      "index": 1,
      "bbox": [x1, y1, x2, y2],
      "area": 3600,
      "decoded": false,
      "data": null,
      "decoder": null
    },
    {
      "index": 2,
      "bbox": [x1, y1, x2, y2],
      "area": 4900,
      "decoded": true,
      "data": "site:A2",
      "decoder": "pyzbar"
    }
  ]
}
```

---

### 🔧 In Progress / To Do

* [ ] Add **distance** / **dummy count** from metadata (if available)
* [ ] Add **per-region QR thumbnails** to PDF
* [ ] Batch processing: multiple images, all PDFs
* [ ] Upload-to-server API (if required by final competition rules)

---

### 👤 Contributors

* Anzer Khan — Vision Pipeline Lead
* ChatGPT – Strategic co-pilot & assistant dev 🤖

---

### ✉️ Contact

📬 [anzerkhan27@gmail.com](mailto:anzerkhan27@gmail.com)
🏛️ University of Huddersfield — MSc AI

---


