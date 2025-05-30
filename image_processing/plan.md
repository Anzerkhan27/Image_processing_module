
### ✅ Summary of the CDR — Software Perspective

#### 🔧 **Your Role (Mohammad Anzer Khan — MSc AI):**

* Develop software for:

  * **Navigation**
  * **Communication**
  * **Autonomous operations**
  * **Integration of AI** (notably for the image processing module)
* Lead the development of the **Image Processing Pipeline** for QR detection and decoding.

---

### 🧠 Key Software Responsibilities from CDR

#### 1. **Embedded Software (ESP32)**

* Manages:

  * Motor control via **PWM** and **stepper driver modules (DRV8825)**
  * Solenoid actuation
  * Battery monitoring (via voltage dividers and ADC)
  * Communication via **HC-12 UART module**
  * Triggering the **digital camera**

#### 2. **Shutdown Logic**

* Uses a clever **latching relay circuit** for startup safety.
* ESP32 evaluates battery health and decides whether to latch the power.
* Needs robust firmware logic to control this early in boot.

#### 3. **Wireless Communication**

* **Primary:** HC-12 at 433MHz for commands + telemetry
* **Image Transmission:** Wi-Fi (ESP32-WROOM-32U) for high-res QR image sending

#### 4. **Camera System**

* **Dual-Camera Setup**:

  * **Analogue camera**: Navigation (Foxeer + Atlatl VTX @ 25mW)
  * **Digital camera (OV5640)**: Still shots for QR scanning

---

### 🧠 AI & Image Processing Module (YOUR BABY)

#### Core Mission

> Detect, decode, and submit the **smallest successful QR code** from rocks for **maximum competition points**.

#### 🔄 Workflow

1. Operator drives rover via analogue feed
2. Operator triggers still photo
3. Image is transmitted to base station
4. **Image Processing Module** runs on laptop:

   * Denoising
   * Contrast enhancement
   * Grayscale conversion
   * QR detection via `pyzbar` or OpenCV's `QRCodeDetector`
5. **Multi-code Detection + Sorting by Size**
6. Select smallest successful QR, log metadata
7. Format & submit as required

#### 🧪 Testing Done

* Synthetic QR dataset generation (`image_generator.py`)
* Single QR detection (`qr_code_detector.py`)
* Multi-QR detection using **sliding window** method (`sliding_window_qr_detector.py`)
* Batch decode + error handling
* Console logging and cropped image verification

#### 📈 Future Work

* Real-time QR detection on **analogue feed** (lightweight, ESP32-compatible)
* Intelligent camera positioning
* Automation of best image capture decision
* Reduce reliance on operator trial-and-error

---

### ⚠️ Critical Dependencies to Watch

* ESP32 RAM & processing limits (image capture + Wi-Fi)
* Network reliability (Wi-Fi + 433MHz UART)
* Power constraints, especially during camera & Wi-Fi operation
* Latency in analogue vs. digital feedback loop
* On-the-day robustness of QR image clarity & transmission

---

### 🧩 What You Might Still Need

* Firmware robustness testing under full rover load
* Resilience to packet loss during Wi-Fi image transfer
* QR scoring pipeline integration with team reporting tool
* Automated fallback when smallest QR fails to decode
* Backup plan if ESP32 crashes mid-mission

---

# ✅ Communication System 1: Analog Video Feed (Navigation)

### 🎯 **Purpose**

To give the operator a **live view** of the terrain while driving the rover — used during navigation and positioning before capturing QR images.

---

## 🧩 Components

| Component                                 | Role                                         |
| ----------------------------------------- | -------------------------------------------- |
| **Foxeer Camera**                         | Captures analog video (NTSC/PAL format)      |
| **Foxeer Atlatl VTX**                     | Transmits the analog video signal wirelessly |
| **5.8 GHz VRX (Receiver)**                | Receives video and outputs via AV or USB     |
| **Display (Goggles, Monitor, or Laptop)** | Shows live video to the operator             |

---

## 📶 Transmission Details

* **Type:** Analog RF video (not digital)
* **Frequency:** 5.8 GHz (standard FPV band)
* **Latency:** Ultra-low (\~<100ms)
* **Range:** \~50–100 meters with small antennas
* **One-way:** No data or feedback — only visual feed

---

## 🧠 Key Points

| Aspect               | Detail                                                              |
| -------------------- | ------------------------------------------------------------------- |
| **Used for**         | Real-time driving and camera positioning                            |
| **Not used for**     | QR scanning, telemetry, commands, or file transfer                  |
| **How to view it**   | Via FPV goggles, portable monitor, or laptop with USB video capture |
| **Not programmable** | Can't access via code unless digitized via AV-to-USB capture device |
| **Bandwidth**        | Enough for smooth video; not suitable for still images or telemetry |

---

## ✅ Why It’s Ideal

* Doesn’t interfere with Wi-Fi or HC-12
* No IP pairing or network setup needed
* Very reliable for real-time situational awareness

---




# ✅ Communication System 2: RC Transmitter + Receiver (Primary Rover Control)

### 🎯 **Purpose**

This channel handles **real-time manual control** of the rover:

* Navigation (movement, steering)
* Triggering actions (camera, solenoid, etc.)

---

## 🧩 Components & Flow

| Component                 | Role                                                       |
| ------------------------- | ---------------------------------------------------------- |
| **RC Transmitter**        | You hold this — sends control signals wirelessly (2.4 GHz) |
| **RC Receiver**           | Mounted on the rover — receives signals from transmitter   |
| **ESP32 Microcontroller** | Reads PWM signals from receiver via GPIO pins              |

---

## 📶 How It Works

1. You move joysticks or flip switches on the **transmitter**
2. Transmitter sends **radio signals (2.4 GHz)** to the **receiver**
3. Receiver outputs **PWM signals (1000–2000 µs pulses)** on each channel
4. **ESP32 reads those PWM signals** and decides how to act (drive, trigger, etc.)

---

## 🧠 Key Characteristics

| Feature                   | Value / Notes                          |
| ------------------------- | -------------------------------------- |
| Frequency                 | 2.4 GHz                                |
| Signal type (to ESP32)    | PWM (one wire per channel)             |
| Coding required on TX/RX? | ❌ No — built-in firmware               |
| Coding required on ESP32? | ✅ Yes — to read and interpret PWM      |
| Latency                   | Very low (great for real-time control) |
| Direction                 | One-way (TX → RX → ESP32)              |
| Feedback/Telemetry?       | ❌ No — use separate system like HC-12  |

---

## ✅ Summary Statement

> The **RC system provides manual, low-latency control** of the rover via **PWM signals** interpreted by the **ESP32**. No programming is required for the transmitter or receiver — only for the **ESP32 to act** on the received signals.

---

