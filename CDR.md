Below is a **revised outline** for your Image Processing Module section, **integrating** the newly provided information about your rover’s **microcontroller**, **telemetry**, and how images are **transferred and processed**. This ensures the final CDR text (about 1500 words) will accurately reflect your updated design.

---

## **Revised Outline for Image Processing Module (~1500 words)**

You can place this under Section 3.4 (Software Design) in the CDR or make it a standalone chapter—whatever fits best with your overall document structure.

---

### **3.4.1 Overview & Objectives**

1. **Mission Context**  
   - Summarize the rover’s main tasks in the **UKSEDS Olympus Rover Trials**: traveling to multiple sites, capturing QR code images, decoding them for points.  
   - Mention the time constraints (30 minutes for the run) and the importance of scanning **smaller QR codes** for higher points.  

2. **Relevance of the Image Processing Module**  
   - Highlight how the new **microcontroller**-based design impacts or interfaces with the image processing pipeline.  
   - State the **module’s core objectives**: to **receive digital images** from the rover, preprocess them, detect multiple QR codes, and decode the smallest one for maximum competition points.

*(Approx. 150–200 words)*

---

### **3.4.2 System Architecture & Data Flow**

1. **Hardware Overview**  
   - **Microcontroller** handles steering, actuator control, basic telemetry, and triggers the **digital camera**.  
   - **Analog Camera Feed** is used for live driving perspective but **not** for QR code scanning.  
   - **Digital Camera** captures high-resolution still images.  

2. **Communication Setup**  
   - **Digital Images** are transmitted from the microcontroller (or a companion board) via a wireless communication module to the **base station laptop/PC**.  
   - Once received, the images are processed by the **Image Processing Module** running on the laptop/PC.

3. **Module Integration**  
   - Show how the software modules link together:  
     1. Rover microcontroller → captures image → sends via radio/Wi-Fi.  
     2. Base station → receives image → runs preprocessing/detection → returns results (e.g., decoded QR text) to rover or logs it for submission.

*(Approx. 200–250 words)*

---

### **3.4.3 Image Capture & Preprocessing**

1. **Triggering the Digital Camera**  
   - The **microcontroller** triggers image capture at each site.  
   - Possibly multiple captures from slightly different angles or distances.

2. **Transfer & Storage**  
   - Outline how many images you can store onboard vs. how quickly you send them to the laptop for processing.  
   - Mention any file format decisions (JPEG vs. PNG) for quick wireless transmission.

3. **Preprocessing Techniques**  
   - **Noise Reduction**: mild filtering if images arrive with sensor noise or compression artifacts.  
   - **Contrast Adjustment**: e.g., adaptive histogram equalization (CLAHE) for bright or dim scenes.  
   - **Color Space**: note if you convert to grayscale or keep RGB for further analysis (some QR libraries handle color fine).

4. **Reliability in Varying Conditions**  
   - The environment may have dusty or bright conditions, especially near rocks.  
   - The microcontroller must ensure good **exposure** and **focus** before capture.

*(Approx. 250–300 words)*

---

### **3.4.4 Multi-QR Code Detection & Decoding**

1. **Library Choice & Rationale**  
   - If using **pyzbar** or **ZXing**: mention it’s due to robust multi-QR detection and better performance under partial occlusion.  
   - If using OpenCV’s `QRCodeDetector`, explain any custom fallback (e.g., sliding window approach) or post-processing to reliably find smaller codes.

2. **Algorithmic Flow**  
   - **Receive image** → **Preprocess** → **Run detection** → **Decode bounding boxes**.  
   - Emphasize how the system will **detect all visible QR codes** in the frame.

3. **Selecting the Smallest QR Code**  
   - Retrieve bounding-box dimensions for each decoded code.  
   - Choose the code with the **lowest bounding-box area** that yields **valid** (non-corrupted) data.  
   - Describe how you handle a scenario if the smallest code fails to decode (fallback to larger code).

4. **Edge Cases**  
   - Partially hidden codes or heavily rotated codes.  
   - Potential duplicates or false positives if the background contains patterns.

*(Approx. 300–400 words)*

---

### **3.4.5 Integration with Rover Autonomy**

1. **Microcontroller Coordination**  
   - Detail how the microcontroller decides when to capture an image (e.g., “We’ve arrived at a site” signal from navigation system).  
   - The microcontroller then **uploads** the captured image to the communication module.

2. **Real-Time vs. Batch Processing**  
   - Clarify if images are processed **in near-real time** (as soon as they arrive) or if you queue them and process after capturing multiple shots.  
   - Mention any **latency** considerations (e.g., it might take a few seconds to transmit each image).

3. **Data Feedback Loop**  
   - Once the code is decoded, the **base station** can confirm a successful detection and instruct the rover to **move on** or re-capture if the smallest code wasn’t decoded properly.

*(Approx. 150–200 words)*

---

### **3.4.6 Testing & Validation**

1. **Simulation & Bench Testing**  
   - Use mock rocks with known-size QR codes in controlled lighting.  
   - Evaluate detection success rates (smallest code dimension that’s reliably detectable).  
2. **Field Trials**  
   - Outdoor or dusty environment to mimic competition conditions.  
   - Test the microcontroller-laptop communication chain to ensure images come through promptly.  
3. **Performance Metrics**  
   - Decoding time per image (must be fast enough for the 30-minute limit).  
   - % of codes correctly identified on first attempt.  

*(Approx. 200–250 words)*

---

### **3.4.7 Risk Analysis & Mitigation**

1. **Risk: Incomplete Transmission**  
   - If wireless link fails or images get corrupted.  
   - **Mitigation**: Attempt to re-send or store partial backups on the rover.  
2. **Risk: Camera Misalignment**  
   - Inadvertent servo or bracket damage after vibration test.  
   - **Mitigation**: Calibrate camera alignment post-vibration if time allows.  
3. **Risk: Overloaded Microcontroller**  
   - Microcontroller being busy with navigation tasks might cause delayed image captures.  
   - **Mitigation**: Use separate threads or dedicated resources for image capture.  

*(Approx. 150–200 words)*

---

### **3.4.8 Compliance with Competition Requirements**

1. **Scoring Relevance**  
   - Tie the multi-QR detection approach to the **Competition Day Marking Guidelines** – scanning the smallest QR code yields max site points.  
   - Confirm that scanning is automatic, thus maximizing attempts within the 30-minute limit.  
2. **Hardware Constraints**  
   - Reassure compliance with the **12 V** max exposure rule (camera, microcontroller, and any associated modules are protected).  
   - No additional cooling or heavy components that risk the 5 kg limit.

*(Approx. 100–150 words)*

---

### **3.4.9 Conclusion & Future Improvements**

1. **Summary**  
   - Reiterate how the pipeline is integrated with the microcontroller and ensures robust detection of multiple codes.  
2. **Next Steps**  
   - Could add more advanced error-correction or AI-based methods.  
   - Explore further optimization to handle extreme angles, partial occlusions more reliably.  

*(Approx. 100–150 words)*

---

## **Word Count Guidance**

- **3.4.1**: 150–200 words  
- **3.4.2**: 200–250 words  
- **3.4.3**: 250–300 words  
- **3.4.4**: 300–400 words  
- **3.4.5**: 150–200 words  
- **3.4.6**: 200–250 words  
- **3.4.7**: 150–200 words  
- **3.4.8**: 100–150 words  
- **3.4.9**: 100–150 words  

Following these ranges should yield about **1500 words total**. You can shift a bit between sections as needed.

---

## **How to Incorporate the New Design Changes**

- **Microcontroller**: Emphasize it **triggers** the digital camera, manages basic controls, and sends data via the communication module.  
- **Analog vs. Digital Feeds**: Clearly state that the **analog camera** is purely for pilot/telemetry, while the **digital camera** is for high-res QR scanning.  
- **Comms Pipeline**: Clarify that **the final decoding** happens on the **laptop/PC** (because it presumably has more processing power than the microcontroller).

These clarifications help reviewers see how your team has partitioned tasks (capture on the rover vs. processing on the base station) for efficiency and reliability.

---

### **Final Tips**

1. **Reference the Additional Documents**  
   - Mention the “Competition Day Marking Guidelines” or “Example Rock Drawings” to show your design aligns with the known environment.  
2. **Keep the Text Technical but Accessible**  
   - The CDR should be detailed enough to show your engineering approach, but not overburdened with code snippets.  
3. **Tables & Diagrams**  
   - Consider a system data flow diagram (Rover Microcontroller → Wireless → Laptop → Image Processing → Decoded Data).  
   - Use short tables for risk or test planning to avoid inflating the word count.

Integrating all these details will ensure that your **CDR** demonstrates a thorough, competition-focused Image Processing Module design, reflecting **the latest hardware changes** (microcontroller-based approach) and **scoring priorities** (detecting the smallest QR code for maximum points).