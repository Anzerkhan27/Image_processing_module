
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


