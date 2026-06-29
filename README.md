# 🤖 Robot Arm 4 DOF Vision Pick and Place

Robot Arm 4 DOF berbasis **Arduino Nano**, **Python**, dan **OpenCV** yang mampu mendeteksi objek berwarna kuning menggunakan webcam dari atas kemudian memindahkannya secara otomatis ke posisi tujuan.

---

## Features

- 🎥 Real-time object detection menggunakan OpenCV
- 🟨 Deteksi objek berwarna kuning
- 📍 Penentuan posisi objek pada 5 area
- 🤖 Kontrol Robot Arm 4 DOF
- 🎮 Servo calibration menggunakan Gamepad
- 💾 Posisi servo disimpan pada file JSON
- 🔌 Komunikasi Serial Arduino Nano
- 📷 Kamera 1280x720 / 1920x1080
- ⚡ Mudah dikembangkan untuk object sorting

---

## Hardware

- Arduino Nano
- MG90S Servo (Base)
- SG90 Servo (Shoulder, Elbow & Gripper)
- USB Webcam
- External Power Supply 6V
- [Robot Arm 4 DOF](https://www.printables.com/model/449747-brazo-robotico-robotic-arm)

---

## Software

- Python 3.12+
- Arduino IDE
- OpenCV
- NumPy
- PySerial
- Pygame

---

## Project Structure

```
RobotArm/
│
├── main.py
├── robot.py
├── camera.py
├── vision.py
├── calibration.py
├── servo_calibration.py
├── config.py
├── test_camera.py
├── test_gamepad.py
│
├── data/
│   ├── area.json
│   └── servo.json
├── arm/
└── arm.ino
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone repository

```bash
git clone https://github.com/saiful2030/Robot-Arm.git
```

Masuk ke folder project

```bash
cd RobotArm
```

Install library

```bash
pip install -r requirements.txt
```

---

## Arduino

Upload sketch Arduino ke **Arduino Nano** menggunakan **Arduino IDE**.
File sketch dapat ditemukan pada direktori berikut:

```text
arm/
└── arm.ino
```
Sesuaikan COM Port pada `config.py`

```python
COM_PORT = "COM13"
```

---

## Run

### 1. Servo Calibration

Jalankan program kalibrasi servo untuk mengatur posisi **Base**, **Shoulder**, **Elbow**, dan menggunakan gamepad. Nilai sudut servo yang ditampilkan pada terminal digunakan sebagai referensi untuk memperbarui file `data/servo.json`.

```bash
python servo_calibration.py
```

Contoh output:

```text
Base      : 40
Shoulder  : 70
Elbow     : 120
```

Salin hasil tersebut ke `data/servo.json` sesuai dengan posisi yang ingin disimpan.

---

### 2. Camera Calibration

Kalibrasi area robot.

```bash
python calibration.py
```

---

### 3. Main Program

```bash
python main.py
```

---

## Serial Command

Robot menerima perintah melalui Serial.

```
B90
```

Move Base

```
S80
```

Move Shoulder

```
E120
```

Move Elbow

```
G30
```

Move Gripper

```
HOME
```

Return Home

```
STATUS
```

Current Position

---

## servo.json

Contoh konfigurasi servo

```json
{
    "home": {
        "base": 90,
        "shoulder": 90,
        "elbow": 90
    },

    "1": {
        "base": 40,
        "shoulder": 70,
        "elbow": 120
    },

    "2": {
        "base": 14,
        "shoulder": 0,
        "elbow": 33
    },

    "3": {
        "base": 57,
        "shoulder": 0,
        "elbow": 33
    },

    "4": {
        "base": 108,
        "shoulder": 0,
        "elbow": 33
    },

    "5": {
        "base": 155,
        "shoulder": 0,
        "elbow": 23
    },
    "1_up": {
        "base": 40,
        "shoulder": 90,
        "elbow": 90
    },

    "2_up": {
        "base": 14,
        "shoulder": 90,
        "elbow": 90
    },

    "3_up": {
        "base": 57,
        "shoulder": 90,
        "elbow": 90
    },

    "4_up": {
        "base": 108,
        "shoulder": 90,
        "elbow": 90
    },

    "5_up": {
        "base": 155,
        "shoulder": 90,
        "elbow": 90
    },

    "gripper": {
        "open": 90,
        "close": 20
    }
}
```

---

## Workflow

```
Webcam
    │
    ▼
OpenCV
    │
    ▼
Detect Yellow Cube
    │
    ▼
Find Current Position
    │
    ▼
Python
    │
    ▼
Arduino Nano
    │
    ▼
Robot Arm
    │
    ▼
Move Cube to Target
```

---

## Dependencies

```
opencv-python
numpy
pyserial
pygame
```

---


## Author

Muhammad Saiful Aji

Computer Engineering 
