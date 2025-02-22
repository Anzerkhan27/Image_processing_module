# 🚀 Team Ray - Initial Rover Specifications

## 🏆 1. Overview
Team Ray's rover for the **UKSEDS Olympus Rover Trials (ORT) 24-25** is designed to meet strict competition requirements while ensuring optimal performance on rugged terrain. The rover must be **lightweight, stable, and capable of image collection, communication, and autonomous navigation**.

---

## 🏗️ 2. Structure & Mechanics
- **⚖️ Total Mass:** ≤ **5kg** (including mounting plate)
- **📏 Volume Limit:** ≤ **0.03m³** (no specific dimensions)
- **🔩 Mounting Requirements:**
  - Custom **mounting plate** (not provided by organizers)
  - Must accommodate **4 x M8 bolts**
  - **40mm** bolt penetration required into the vibration table
- **📡 Stability:**
  - Must remain stable at **30° inclines**
  - No **damping mechanisms** in the mounting plate

---

## 📸 3. Image Collection & Submission
- **🎥 Image Capture:** The rover must be equipped with a **camera** for taking images
- **📡 Transmission:** Must **wirelessly send images** to the team for display on a screen

---

## 🔋 4. Power & Propulsion
- **🏎️ Locomotion:** Must function **without atmospheric reliance** (no drones)
- **🏜️ Terrain Compatibility:**
  - Handles **sand & rocks** (rock height: **5-40cm**, diameter: **5-30cm**)
  - Must traverse **slopes up to 15°**
- **📏 Travel Distance:** At least **60m** required
- **⏳ Operational Time:** Minimum **30 minutes** runtime

---

## 🎮 5. Command & Control
- **📡 Primary Communication:** Must use **UK-legal wireless frequencies**
- **🔌 Backup Communication:** **Ethernet** (for emergency use)
- **🤖 Autonomous Capabilities:**  
  - **Onboard navigation** required  
  - **Must disclose** autonomous functions to judges  

---

## ⚠️ 6. Safety
- **⚡ Live Voltage:** No exposed component should exceed **12V**
- **🔋 Battery Safety:**
  - Only **LiPo batteries** allowed (**No lead-acid!**)
  - Protection from **over-voltage, under-voltage, over-current, short circuits, and overheating** required
  - **Must use CE-marked LiPo charger** & charge bags
- **🛑 Kill Switch:** An **external, easily accessible** hardware **kill switch** required
- **🔧 Motor Protection:** Motors & connections must be **shielded from damage**

---

## ✅ 7. Verification Methods
Each requirement will be **validated** using one or more of the following methods:
- **👀 Inspection (I)** – Visual/manual examination
- **📊 Analysis (A)** – Computational models & calculations
- **🛠️ Demonstration (D)** – Observing system operation
- **⚡ Testing (T)** – Controlled experiments  


---

💡 **This document serves as the baseline specifications for Team Ray’s Rover. Further refinements will be made as development progresses!** 🚀

# 🚀 UKSEDS Olympus Rover Trials 24-25 – The Challenge Breakdown

## 🛰️ Mission Overview
The **Olympus Rover Trials (ORT) 24-25** is a **robotics and engineering competition** simulating a **Martian exploration mission**. University teams must **design, build, and operate a rover** capable of performing scientific research in a **Mars-like environment**.

---

## 🔬 Mission Background – The **TERRA Mission**
Your rover is part of the **TERRA (Terrain Exploration and Remote Reconnaissance for Analysis) Mission**, which simulates a **pre-landing reconnaissance mission** on Mars.  

The mission goals:
✅ **Survey the terrain**  
✅ **Capture high-quality images** of geological points of interest  
✅ **Transmit the images for analysis**  

---

## 🎯 The Challenge Breakdown
The competition is divided into **two core trials**:

### **1️⃣ Mars Yard Navigation & Imaging Task**
Your rover must **navigate the Airbus Mars Yard**, a simulated Martian terrain with:
- **Sandy surfaces**
- **Randomly placed rocks (5-40cm height)**
- **Slopes up to 15°**

📍 **Your Mission:**
🔹 Locate **5 geological points of interest (POIs)**  
🔹 Capture **clear images of QR codes** placed on the rocks  
🔹 Successfully **transmit the images** back to mission control  

🔍 **QR Codes Challenge:**
Each POI has **QR codes of varying sizes**, and **scanning the smallest possible QR code earns the most points**.  
- 🟢 **Useful QR Codes** – Contain **scientific data** about the rock’s composition.  
- 🔴 **Corrupted QR Codes** – **Cannot be scanned** (decoys).  

📌 **Key Challenge:** Extract **valid data** while ignoring decoy QR codes.  

---

### **2️⃣ Vibration Test (Launch Simulation)**
Once the navigation test is complete, the rover must **survive a launch simulation** on a **vibration test bench**.

🚀 **Test Details:**
✅ The rover is **mounted to a vibration table**  
✅ It undergoes **a 60-second random vibration test**  
✅ The goal: **Remain fully operational** after the test  

💥 **Points are deducted for failures:**
- **-50 points** → Minor fastener loss  
- **-250 points** → Loss of one function (e.g., camera failure)  
- **-500 points** → Loss of multiple functions (e.g., driving + communication)  
- **-1000 points** → **Total mission failure (rover inoperable)**  

---

## ⚠️ Constraints & Software Engineering Challenges
As a **Software Engineer** on **Team Ray**, here are your biggest constraints:

### **1️⃣ No Line-of-Sight Navigation**
❌ The control room has **no direct visibility** to the rover.  
✅ The rover must rely on **autonomous navigation** and telemetry feedback.  

### **2️⃣ Limited Wireless Communication**
- The rover must use **UK-legal frequencies**.  
- A **backup Ethernet connection** is allowed **only in case of external interference**.  

### **3️⃣ Efficient Image Processing & Transmission**
- The **QR codes vary in size**, and some are **partially obscured**.  
- Images must be **clear enough for judges to verify the QR content**.  

### **4️⃣ Vibration Resilience**
- Software must **remain stable** even if hardware components experience stress.  
- The **system must not crash** due to sensor disconnections.  

### **5️⃣ Time Constraints**
⏳ **Only 30 minutes** are available for:  
✅ Navigation  
✅ Image capture  
✅ Image submission  

---

## 🏆 Scoring Breakdown
🔹 **Total Possible Score:** **4500 points**  

| Category                 | Maximum Points  |
|--------------------------|---------------:|
| **Test Run** (Mars Yard) | **2000 points** |
| **- Image Collection**   | **1700 points** |
| **- Navigation Checkpoint** | **300 points** |
| **Bonus Image Processing** | **500 points** |
| **Vibration Test**       | **1000 points** |
| **Special Awards** (Innovation, Automation, Public Engagement) | **1000 points** |

📌 **Pro Tip:** The **Best Rover Award** is based on **total competition performance**, not just the test run.

---


### **Clarifying Image Capture & QR Code Scanning Process**

From the **Airbus Statement of Work**, here’s how the **image capture and QR scanning process works** in the **Olympus Rover Trials (ORT) 24-25):**

---

### **📸 1. How Do We Capture and Submit Images?**
✅ **Your rover must take images of QR codes placed on rocks** at each **Point of Interest (POI)**.  
✅ You **must submit a single image per site** (max 5 images for 5 sites).  
✅ The images must be **submitted before the 30-minute time limit ends**.  

> **Key Rule:** You can take multiple images but can **only submit one per POI** for scoring.

---

### **📡 2. How Are the QR Codes Scored?**
Each **Point of Interest (rock)** has **multiple QR codes of different sizes**.  
- 🟢 **Smaller QR codes = More Points**  
- 🔴 **Some QR codes are corrupted (decoys) and cannot be scanned**  

📌 **Scoring Method:**
- 10% of available points are awarded just for **submitting an image of a QR code**.  
- 90% of available points are awarded for **extracting information from the QR code**.  
- The **smallest successfully scanned QR code at each site earns the most points**.  

---

### **🤖 3. Do We Scan the QR Codes Ourselves or Do the Judges Scan Them?**
You **can either**:
1. **Submit just the image**, and the **competition judges** will scan the QR codes from your submission.
2. **Scan the QR codes yourself**, extract the information, and submit the **extracted rock composition data** with the image.

📌 **Important:** Judges **will only scan each image once**. If the scan fails (e.g., blurry image, QR not fully visible), you **lose the Information Extracted points** for that POI.

---

### **🔬 4. Where Do We Get the Rock Composition Data?**
The **useful QR codes** contain **scientific rock composition data**.  
- When scanned, they **reveal geological details about the rock**.  
- Your goal is to **extract this data** and submit it for additional points.  

If your software can **autonomously scan and extract the QR code data**, you can **submit both the image and the extracted rock composition** for maximum points.

---

### **🚀 Best Strategy for Maximum Points**
1. **Take multiple images per POI but submit only the best one.**  
2. **Prioritize scanning smaller QR codes (more points).**  
3. **Try to scan the QR codes yourself to avoid relying on judges.**  
4. **Submit both the image and the extracted data to ensure full scoring.**  

---
### **📸 Understanding QR Code Placement on Each Rock (POI)**  

Each **Point of Interest (POI)** (a rock) will have **multiple QR codes** arranged on its **different faces**.  

🔹 **Each rock (POI) contains multiple QR codes** of varying **sizes and positions**.  
🔹 Some QR codes may be **partially hidden** from certain angles.  
🔹 **Only one QR code per rock will give you the best possible points** (the smallest successfully scanned one).  

---

### **📌 How Many QR Codes Are in Each Image?**
✅ Your rover **must take an image of the rock** where **as many QR codes as possible are visible**.  
✅ Ideally, you want **all QR codes in a single image**, but due to **angles and terrain**, you may need to **adjust the rover’s position**.  
✅ The competition **does not specify an exact number of QR codes per rock**, but each POI **will have multiple QR codes to choose from**.  
✅ Your goal is to **scan and submit the QR code that gives the most points** (the smallest successfully scanned one).

---

### **📡 Image Submission Rules**
- **You can only submit one image per rock (POI).**  
- Judges **will scan a QR code from that image**, or you can scan it yourself and submit the extracted information.  
- If multiple QR codes are visible in the image, **judges will attempt to scan any one of them**.  

---

### **🎯 What’s the Best Strategy?**
- **Capture images where multiple QR codes are visible** in a **single shot** (to increase your chances of a successful scan).  
- **Ensure high image clarity**—blurred or obstructed QR codes **won’t be scannable**.  
- **If possible, scan the QR codes yourself and extract rock composition data** before submitting.  

📌 **Final Takeaway:**  
**Each image should contain as many QR codes as possible, but you only need to extract and submit the smallest one that scans successfully!** 🚀


# 📸 Image Processing Module – Overview

## 📝 1. Introduction
The **Image Processing Module** is responsible for **preprocessing images captured by the high-resolution digital camera** before they are submitted for evaluation in the **UKSEDS Olympus Rover Trials 24-25**. This module ensures that the submitted images are **clear, optimized for QR code recognition, and suitable for extracting rock composition data**.

---

## 🎯 2. Objectives
- **Enhance image clarity** to ensure QR codes are easily scannable.
- **Reduce noise and improve contrast** for better QR code detection.
- **Detect and crop QR codes** to prioritize the most useful data.
- **Minimize image artifacts** that could affect readability.
- **Optimize image size and resolution** for efficient transmission.

---

## 📷 3. Camera System Integration
The module processes images from the **high-resolution digital camera**, which captures still images for QR scanning and geological analysis.  
Additionally, a separate **analog camera provides telemetry via video feed**, which will not be part of this preprocessing pipeline.

---

## 🛠 4. Basic Preprocessing Pipeline
1. **Image Acquisition** – Capture raw images from the high-resolution camera.
2. **Noise Reduction** – Apply filters to remove sensor noise and compression artifacts.
3. **Contrast & Brightness Adjustments** – Enhance image details for better QR recognition.
4. **Edge Detection & Sharpening** – Improve QR code visibility and readability.
5. **Region of Interest (ROI) Extraction** – Detect and crop QR codes for efficient scanning.
6. **Image Resizing & Compression** – Optimize image dimensions and file size for transmission.

---

## 🚀 5. Next Steps
- **Develop a prototype preprocessing script** using OpenCV.
- **Test different filtering techniques** for optimal QR detection.
- **Integrate with onboard processing hardware** for real-time performance.

---
💡 *This document will be expanded with technical details as development progresses.*



# 📜 QR Code Image Generator – Brief Documentation

## 📝 Overview
This script generates an **image with a randomly placed QR code** on a blank white background. It is useful for testing **QR code detection and recognition algorithms**.

## 🛠️ Functionality
- Loads a **random QR code** from the `qr_dataset/` directory.
- Resizes the QR code to a **fixed dimension (150x150 pixels)**.
- Places the QR code **randomly** on an **800x800 pixel** white background.
- Ensures **QR codes do not overlap**.
- Saves the generated image to the **`qr_code_images/`** folder as `generated_qr_image.png`.

## 📂 File Structure
```
qr_code_images/      # Folder for generated images
qr_dataset/          # Folder containing QR code images
image_generator.py   # This script
```

## 🚀 How to Use
1. Place QR code images in `qr_dataset/`.
2. Run the script:
   ```bash
   python image_generator.py
   ```
3. The generated image will be saved in `qr_code_images/generated_qr_image.png`.

## 🔜 Future Improvements
- Support for **multiple QR codes** in one image.
- Option to **vary background colors**.
- Enhanced positioning to **prevent QR code clipping**.

💡 **This script provides a quick way to generate QR code test images for machine vision applications! 🚀**

---

# 📜 QR Code Detector – Code Explanation

## 📝 1. Introduction
This script is a **simple QR code detector** that:
- **Detects a single QR code** in an image.
- **Draws a bounding box** around the detected QR code.
- **Prints the bounding box coordinates** in the console.

The program **uses OpenCV’s built-in `QRCodeDetector()`** for quick and efficient QR code detection.

---

## 📂 2. Project Structure
```
qr_code_detector.py
qr_code_images/
   ├── generated_qr_image.png
qr_dataset/  # (Contains QR codes used for generating test images)
```
- `qr_code_detector.py` → Contains the QR code detection logic.
- `qr_code_images/` → Stores test images for detection.
- `qr_dataset/` → (Optional) Stores QR codes for generating test data.

---

## 🛠️ 3. Code Breakdown

### **🔹 Importing Required Libraries**
```python
import cv2
import os
```
- **cv2 (OpenCV)** → Used for **image processing and QR code detection**.
- **os** → Handles **file paths**.

---

### **🔹 Configuring Image Paths**
```python
INPUT_FOLDER = "qr_code_images"
IMAGE_NAME = "generated_qr_image.png"
INPUT_IMAGE_PATH = os.path.join(INPUT_FOLDER, IMAGE_NAME)
```
- **Defines the folder (`qr_code_images/`)** where test images are stored.
- **Creates the full path to the test image**.

---

### **🔹 Defining the QR Code Detection Function**
```python
def detect_qr_code(image_path):
```
This function:
1. **Loads the input image**.
2. **Detects a QR code** using OpenCV.
3. **Draws a bounding box** around the detected QR code.
4. **Prints the QR code's coordinates**.

---

### **🔹 Loading the Image**
```python
image = cv2.imread(image_path)
if image is None:
    print(f"❌ Error: Could not load image {image_path}")
    return
```
- **`cv2.imread(image_path)`** → Reads the image.
- If **image is missing or unreadable**, it **displays an error and exits**.

---

### **🔹 Converting Image to Grayscale**
```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```
- QR codes are **black-and-white patterns**, so we **convert the image to grayscale** for better detection.

---

### **🔹 Initializing OpenCV’s QR Code Detector**
```python
qr_detector = cv2.QRCodeDetector()
```
- This **creates an instance** of OpenCV’s **QR code detector**.

---

### **🔹 Detecting a QR Code**
```python
retval, points = qr_detector.detect(gray)
```
- **`retval` (Boolean)** → `True` if a QR code is detected, `False` otherwise.
- **`points` (NumPy array)** → Contains **coordinates of the QR code’s four corners**.

---

### **🔹 Processing Detected QR Codes**
```python
if retval and points is not None:
    points = points.astype(int)  # Convert floating-point coordinates to integers
```
- If **a QR code is detected**, we:
  - Convert its **coordinates from floating-point to integers** (necessary for drawing).

---

### **🔹 Printing QR Code Coordinates**
```python
print("✅ QR Code detected with coordinates:")
for i, point in enumerate(points[0]):
    print(f"Point {i+1}: {tuple(point)}")
```
- **Each coordinate is printed in `(x, y)` format**.
- Example **console output**:
  ```
  ✅ QR Code detected with coordinates:
  Point 1: (120, 300)
  Point 2: (250, 300)
  Point 3: (250, 450)
  Point 4: (120, 450)
  ```

---

### **🔹 Drawing the Bounding Box**
```python
for i in range(4):
    cv2.line(image, tuple(points[0][i]), tuple(points[0][(i + 1) % 4]), (0, 255, 0), 3)
```
- **Loops through all 4 corner points**.
- **Draws green lines** between them to form a bounding box.

---

### **🔹 Displaying the Image**
```python
cv2.imshow("QR Code Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
- **`cv2.imshow()`** → Displays the processed image.
- **`cv2.waitKey(0)`** → Waits for a key press before closing.
- **`cv2.destroyAllWindows()`** → Closes all OpenCV windows.

---

### **🔹 Running the Script**
```python
if __name__ == "__main__":
    detect_qr_code(INPUT_IMAGE_PATH)
```
- This ensures the script **only runs when executed directly** (not when imported).

---

## 🎯 4. How to Use
1. **Ensure the test image exists** at:
   ```
   qr_code_images/generated_qr_image.png
   ```
2. **Run the script**:
   ```bash
   python qr_code_detector.py
   ```
3. **Check the console** for QR code coordinates.
4. **See the output image** with a **green bounding box** around the QR code.

---

## 🔥 5. Example Output
### **✅ Console Output**
```
✅ QR Code detected with coordinates:
Point 1: (120, 300)
Point 2: (250, 300)
Point 3: (250, 450)
Point 4: (120, 450)
```
### **🖼️ Image Output**
✔ The detected QR code will be **highlighted with a green bounding box**.

---

## 🔜 6. Next Steps
- **Improve detection for multiple QR codes**.
- **Enhance robustness** for different lighting conditions.
- **Add QR code decoding** to extract embedded information.

---

💡 **This is the simplest yet effective OpenCV QR code detector! 🚀🔥**
```