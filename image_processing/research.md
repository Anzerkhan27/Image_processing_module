Below is a **draft write-up** of the **Image Processing Module** for your Critical Design Review (CDR). The text is structured according to the outline provided, with some modifications to reflect your **manual control** approach and **manual photo capture** of each region of interest (ROI). The total length is approximately **1,500 words**.

---

## **3.4 Image Processing Module – Detailed Design**

### **3.4.1 Overview & Objectives**  
The Image Processing Module is central to the mission goal of scanning QR codes for maximum points in the UKSEDS Olympus Rover Trials (ORT). Given the competition format, each site contains multiple QR codes of varying sizes; detecting and decoding the **smallest successful code** is critical for achieving the highest possible score. Our system therefore prioritizes **robust** detection of multiple codes within a single image, ensuring we can identify and decode the smallest code that yields valid data.

Unlike some fully autonomous designs, our rover is **manually controlled**, meaning an operator drives and positions the rover at each point of interest (POI). The operator also **manually captures** digital still images using an onboard camera. While this approach simplifies certain navigation aspects, it imposes strict time management: with only 30 minutes for the entire run, we must quickly acquire and process images to ensure we do not miss any site’s potential points.

In addition to maximizing points by focusing on smaller codes, this module also aims to handle edge cases such as partial occlusions, varied lighting, and potential motion blur from the rover’s movement. The new design changes—where a microcontroller coordinates camera actuation and data transmission—further integrate the module into the rover’s overall architecture. Ultimately, these objectives guide our software’s technical choices, from preprocessing methods to detection and decoding algorithms.

### **3.4.2 System Architecture & Data Flow**  
The rover incorporates a **microcontroller** responsible for fundamental tasks: steering, telemetry, basic actuator control (including digital camera triggering), and radio communication. Alongside this, we have two cameras:

1. **Analog Feed**: Used primarily for live feedback to the operator’s laptop—helping the pilot see the terrain, avoid obstacles, and position near POIs. This analog stream does not feed into the image-processing pipeline for QR scanning.

2. **Digital Camera**: High-resolution still images are captured upon operator command. Once an image is taken, the microcontroller transmits it via the rover’s wireless communication module to a base station (a laptop or PC). Here, the **Image Processing Module** runs locally, leveraging the computational power of the PC for rapid detection and decoding.

This flow is depicted as follows:
1. **Operator** maneuvers the rover to the POI using the **analog feed**.
2. **Microcontroller** triggers the digital camera upon operator input.  
3. **Digital Image** is sent wirelessly to the **base station**.  
4. **Image Processing Software** on the base station preprocesses and scans the image, decoding any QR codes found.  
5. The decoded data is **logged** or displayed immediately. If the results are unsatisfactory (e.g., the smallest code is not detected), the operator may capture additional images from different angles.

This structure balances the microcontroller’s limited processing capabilities by offloading intensive image analysis to the laptop, where specialized libraries can run efficiently.

### **3.4.3 Image Capture & Preprocessing**  
Because the rover is controlled manually, the operator visually determines when to capture an image of the rock or region of interest. At each site, we **may capture multiple images** to ensure that smaller QR codes—often hidden by rock edges or partially obscured—are adequately photographed. This is particularly important since the competition rules allow multiple scanning attempts to find the smallest code.

**Image Storage & Transfer**  
- Our digital camera stores a raw or JPEG-compressed image briefly onboard.  
- The rover’s microcontroller immediately transmits that file via a radio/Wi-Fi link to the laptop.  
- We balance file size vs. resolution, typically capturing at a moderate resolution that reliably shows details of small QR codes without overloading the link.

**Preprocessing Pipeline**  
Upon receipt, the module performs:
1. **Noise Reduction**: Mild filtering (e.g., OpenCV’s `fastNlMeansDenoisingColored`) if compression artifacts or sensor noise are high.  
2. **Contrast Enhancement**: Adaptive histogram equalization (CLAHE) or gamma adjustments to highlight the QR code edges, especially if lighting is uneven around rocks.  
3. **Optional Thresholding**: If background glare or irregular illumination is present, adaptive thresholding can boost code visibility.  
4. **Color to Grayscale**: Many QR detection libraries work just as well in grayscale, reducing computational overhead.

We consider real-world constraints such as dust on the camera lens or shadows cast by the rover. The operator can reposition or clean the lens if images appear subpar, but we aim for automated methods that can handle moderate image defects.

### **3.4.4 Multi-QR Code Detection & Decoding**  
Given the competition’s emphasis on scanning the **smallest QR code** at each site, we need a robust approach capable of detecting **multiple QR codes** in a single image, then identifying and decoding each code. From there, we select whichever is smallest but still yields valid data.

1. **Library Choice**  
   We currently plan to use a specialized QR detection library like **pyzbar** (Python) or **ZXing**, which are known for more reliable multi-code detection than OpenCV’s built-in `QRCodeDetector()`. These libraries can handle partial occlusions and rotation better, as well as read multiple codes in a single pass.

2. **Algorithmic Flow**  
   - The image is loaded into memory after preprocessing.  
   - `pyzbar.decode()` (or a similar function) processes the entire frame and returns a list of detection objects. Each object typically includes bounding-box coordinates, the decoded text/string, and confidence scores.  
   - If one or more codes are detected, we measure bounding-box dimensions `(w × h)` to infer approximate code size.  
   - Each code is validated to confirm it is **not corrupted** (e.g., partial decode, nonsensical data).  

3. **Selecting the Smallest**  
   - Among valid detections, we pick the bounding box with the smallest area—assuming that code is physically smaller on the rock.  
   - We store or display that code’s data as the “best candidate.” If the smallest code fails to decode properly (for instance, a partial read or extremely fuzzy image), the operator may attempt to reposition the rover or settle for a slightly larger code.

4. **Edge Cases**  
   - **Partial Occlusion**: If the code is cut off by the rock’s curvature, detection might fail entirely. We mitigate by capturing multiple angles.  
   - **Reflections**: Rocks may be shiny or angled. Adjusting the camera angle helps reduce glare.  
   - **Multiple Decoys**: Some codes may be intentionally corrupted. We rely on the library’s decoding checks; if data is unreadable, that code is discarded.

This strategy ensures we comprehensively scan each image for all codes and systematically choose the smallest valid result, directly aligning with the ORT scoring rules.

### 3.4.5 Integration with Rover Operations

Although the rover is manually driven, the process of image capture, transmission, QR detection, and data submission follows a well-defined sequence. The microcontroller handles actuator control and telemetry, while the base station laptop performs all image analysis.

1. **Arrival at the POI**
- The operator manually drives the rover to a Point of Interest (POI) using the analog feed displayed on the laptop.
- Once the operator confirms a clear view of the rock, they manually trigger the rover’s digital camera to capture a still image.
2. **Image Transmission**
- The microcontroller transmits the captured image wirelessly to the base station.
- The base station queues the image for immediate processing.

3. **Processing & Feedback**
- The Image Processing Module runs the multi-QR detection pipeline on the received image.
- The system selects the smallest successfully decoded QR code from the dataset.
- If a valid smallest QR code is found, the decoded data (e.g., rock composition) is logged and displayed to the operator.
- If detection is unsuccessful, the operator may capture additional images from different angles to improve scanning accuracy.

### **3.4.6 Testing & Validation**  
Testing the Image Processing Module involves a mix of **bench tests** (with printed QR codes in a controlled environment) and **field trials** in conditions similar to the competition:

1. **Bench Tests**  
   - We print a series of QR codes in different sizes (e.g., 3×3 mm up to 10×10 mm) and place them on a mock “rock” surface with mild curvature or angled surfaces.  
   - We evaluate detection rates for each code size at varying camera distances and angles, measuring time to decode and success rate.

2. **Field Trials**  
   - Outdoor testing where lighting changes, dust, and potential reflections from uneven terrain are present.  
   - The rover pilot manually drives to a test site, captures images, and transmits them to a laptop for real-time decoding.

3. **Performance Metrics**  
   - **Detection Accuracy**: Percentage of successful decodes for the smallest code present.  
   - **Processing Time**: Typical decoding time on the laptop (e.g., < 1 second is ideal).  
   - **Transmission Reliability**: Rate of packet drops or corrupted images.  

By iterating on these tests, we refine not only the detection parameters but also the camera capture routine. This ensures that, come competition day, we can confidently identify the smallest valid code in minimal time.

### **3.4.7 Risk Analysis & Mitigation**  
Several risks could threaten successful code detection:

1. **Poor Image Quality**  
   - **Risk**: Dust, glare, or lens misalignment lead to blurred or low-contrast images.  
   - **Mitigation**: Regular lens cleaning, careful manual alignment, short exposure times to reduce motion blur, or retakes if the first attempt fails.

2. **Communication Failures**  
   - **Risk**: Wireless signals drop or images are partially corrupted en route.  
   - **Mitigation**: Implement robust error checking or re-transmission. If the code data is time-critical, the operator can recapture quickly.

3. **Limited Competition Time**  
   - **Risk**: Spending too long capturing multiple images at each site might hamper the rover’s ability to visit all sites.  
   - **Mitigation**: Practicing efficient manual driving, capturing only as many images as needed, and ensuring the base station decodes rapidly.

4. **Hardware Damage Post-Vibration Test**  
   - **Risk**: The camera mount or microcontroller connections loosen, degrading image capture quality.  
   - **Mitigation**: Secure mounting, verifying alignment before re-entering the field, possible re-calibration steps if time allows.

### **3.4.8 Compliance with Competition Requirements**  
The Image Processing Module supports the **UKSEDS ORT** rules and constraints in multiple ways:

- **Smallest QR Code Priority**: The software automatically locates and decodes each visible code, then selects the smallest valid code for maximum site points. This aligns directly with the Marking Guidelines that award 100% of site points for scanning the smallest code.
- **No Exposed High Voltage**: All hardware, including camera interfaces and microcontrollers, operate at or below 12 V DC with appropriate casing and wiring, complying with the safety rules.
- **Time Efficiency**: Manual control is within the competition framework; images can be captured quickly, and the code detection library runs on a dedicated laptop, ensuring minimal processing delay.
- **Rock Constraints**: Because codes can be tilted or partially hidden on a sloped rock surface, the detection 

---


### **3.4.9 Future Improvements**

While the current system effectively **detects, stores, and selects the smallest QR code** through manual image capture, future improvements will focus on **automating the image capture process**. This will eliminate operator guesswork and ensure **optimal QR code detection and framing** before capturing the digital image.

#### **1. Real-Time QR Code Detection on the Analogue Feed**
- A separate **real-time QR detection module** will be integrated into the **analogue live feed**.  
- Instead of waiting for digital still images, this module will continuously scan the **low-latency video feed** for QR codes.  
- It will **only perform detection** (not decoding) to **quickly identify** potential QR locations.  

#### **2. Identifying the Best QR Code Candidate in Real Time**
- As the system detects multiple QR codes in the analogue feed, it will:
  - **Track the smallest QR code** within the field of view.
  - Continuously **adjust position recommendations** to frame the QR code more clearly.  
  - Disc **real-time detection module** will be lightweight, allowing it to run **directly on the rover** instead of waiting for transmission to the base station.  
- The **best candidate QR code** will be **pre-validated in real-time**, reducing the need for multiple redundant captures and improving efficiency.  
- This will **shorten the decision-making loop** from **detection → capture → processing**, making the entire workflow more time-efficient.

### **Expected Benefits**
✅ **Minimizes operator intervention**, reducing errors in positioning.  
✅ **Ensures consistently sharp and well-framed images** of the smallest QR code.  
✅ **Optimizes mission time usage**, allowing the rover to complete scans more efficiently.  
✅ **Reduces unnecessary image transmissions**, improving bandwidth usage and processing speed.

By integrating **real-time QR detection on the analogue feed** and **automating digital image capture**, we can significantly improve the accuracy, speed, and efficiency of our QR code scanning workflow for future iterations of the rover system.
ard **decoys or corrupted QR codes** before capturing an image.  

#### **3. Automating Digital Image Capture Based on Contextual Information**
- Instead of relying on the operator to manually trigger the camera, the system will:
  - Determine the **best moment to capture the image** using:
    - **Sensor Data** (e.g., camera tilt, distance to target).  
    - **Rover Arm Positioning** (ensuring the QR code is not at an extreme angle).  
    - **Contextual Clues** (such as stability or avoiding glare).  
  - Once an **optimal frame** is detected, the **microcontroller will automatically trigger the digital camera**, ensuring the **sharpest image with the smallest QR code** is captured.

#### **4. Improved Integration with the Image Processing Pipeline**
- This new
**Word Count (Approx.):** ~1,500 words

This completes the draft text for your CDR’s Image Processing Module. Adjust headings or word counts as needed to integrate seamlessly with the rest of your Critical Design Review document. Good luck with finalizing your submission!



