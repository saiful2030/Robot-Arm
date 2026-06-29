import pygame
import serial
import time
import os

# ============================================
# SERIAL
# ============================================

PORT = "COM13"
BAUDRATE = 9600

ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)

# ============================================
# GAMEPAD
# ============================================

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Gamepad tidak ditemukan!")
    exit()

joy = pygame.joystick.Joystick(0)
joy.init()

print("Gamepad :", joy.get_name())

# ============================================
# SERVO
# ============================================

base = 90
shoulder = 90
elbow = 90
gripper = 90

STEP = 1
DEADZONE = 0.30

# ============================================

last_base = base
last_shoulder = shoulder
last_elbow = elbow
last_gripper = gripper

# ============================================

def kirim():

    global last_base
    global last_shoulder
    global last_elbow
    global last_gripper

    if base != last_base:
        ser.write(f"B{base}\n".encode())
        last_base = base

    if shoulder != last_shoulder:
        ser.write(f"S{shoulder}\n".encode())
        last_shoulder = shoulder

    if elbow != last_elbow:
        ser.write(f"E{elbow}\n".encode())
        last_elbow = elbow

    if gripper != last_gripper:
        ser.write(f"G{gripper}\n".encode())
        last_gripper = gripper

# ============================================

def tampil():

    os.system("cls")

    print("===================================")
    print("   ROBOT ARM CALIBRATION")
    print("===================================")
    print()

    print(f"Base      : {base}")
    print(f"Shoulder  : {shoulder}")
    print(f"Elbow     : {elbow}")
    print(f"Gripper   : {gripper}")

    print()
    print(f"STEP      : {STEP}")
    print()
    print("START = HOME")
    print("BACK  = EXIT")

# ============================================

tampil()

# ============================================

while True:

    pygame.event.pump()

    # -------------------------
    # Analog
    # -------------------------

    lx = joy.get_axis(0)
    ly = joy.get_axis(1)

    rx = joy.get_axis(2)
    ry = joy.get_axis(3)

    berubah = False

    # BASE

    if lx > DEADZONE:

        base = min(180, base + STEP)
        berubah = True

    elif lx < -DEADZONE:

        base = max(0, base - STEP)
        berubah = True

    # SHOULDER

    if ly > DEADZONE:

        shoulder = max(0, shoulder - STEP)
        berubah = True

    elif ly < -DEADZONE:

        shoulder = min(180, shoulder + STEP)
        berubah = True

    # ELBOW

    if ry > DEADZONE:

        elbow = max(0, elbow - STEP)
        berubah = True

    elif ry < -DEADZONE:

        elbow = min(180, elbow + STEP)
        berubah = True

    # GRIPPER

    if rx > DEADZONE:

        gripper = min(180, gripper + STEP)
        berubah = True

    elif rx < -DEADZONE:

        gripper = max(0, gripper - STEP)
        berubah = True

    # -------------------------
    # BUTTON
    # -------------------------

    # LB = Step -

    if joy.get_button(4):

        STEP = max(1, STEP - 1)

        tampil()

        time.sleep(0.2)

    # RB = Step +

    if joy.get_button(5):

        STEP = min(10, STEP + 1)

        tampil()

        time.sleep(0.2)

    # START = HOME

    if joy.get_button(7):

        base = 90
        shoulder = 90
        elbow = 90
        gripper = 90

        berubah = True

        time.sleep(0.2)

    # BACK = EXIT

    if joy.get_button(6):

        break

    # -------------------------

    if berubah:

        kirim()

        tampil()

        time.sleep(0.03)

# ============================================

ser.close()

pygame.quit()

print("Program selesai.")