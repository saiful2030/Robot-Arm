# ==========================================================
# CAMERA
# ==========================================================

CAMERA_ID = 0

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080

CAMERA_FPS = 30

# ==========================================================
# ARDUINO
# ==========================================================

COM_PORT = "COM13"      # Ganti sesuai Arduino
BAUDRATE = 9600

SERIAL_TIMEOUT = 1

# ==========================================================
# HSV KUNING (Default)
# Nilai ini nanti bisa diganti dari hsv.json
# ==========================================================

LOWER_YELLOW = (20, 100, 100)
UPPER_YELLOW = (35, 255, 255)

# ==========================================================
# DETEKSI OBJEK
# ==========================================================

MIN_OBJECT_AREA = 500
MAX_OBJECT_AREA = 50000

BLUR_SIZE = 5

# ==========================================================
# ROBOT ARM
# ==========================================================

HOME_BASE = 90
HOME_SHOULDER = 90
HOME_ELBOW = 90
HOME_GRIPPER = 90

GRIPPER_OPEN = 90
GRIPPER_CLOSE = 20

# Delay antar perintah ke Arduino (detik)
MOVE_DELAY = 0.30

# Tunggu servo selesai bergerak (detik)
SERVO_WAIT = 0.80

# ==========================================================
# FILE
# ==========================================================

HSV_FILE = "data/hsv.json"
AREA_FILE = "data/area.json"
SERVO_FILE = "data/servo.json"

# ==========================================================
# WARNA (BGR OpenCV)
# ==========================================================

COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)

# ==========================================================
# FONT
# ==========================================================

import cv2

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2

# ==========================================================
# WINDOW
# ==========================================================

WINDOW_NAME = "Robot Arm Vision"

# ==========================================================
# DEBUG
# ==========================================================

SHOW_FPS = True
SHOW_CENTER = True
SHOW_BOUNDING_BOX = True
SHOW_AREA = True

# ==========================================================
# POSISI AREA
# ==========================================================

AREA_NAME = {
    1: "Posisi 1",
    2: "Posisi 2",
    3: "Posisi 3",
    4: "Posisi 4",
    5: "Posisi 5"
}