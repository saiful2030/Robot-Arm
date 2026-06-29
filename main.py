import cv2
import threading

from camera import Camera
from vision import Vision
from robot import RobotArm


# ==========================================================
# INIT
# ==========================================================

cam = Camera()

vision = Vision()

robot = RobotArm()

if not robot.connect():

    print("Arduino tidak terhubung!")

    exit()


print("-------------------------------------")
print("Robot Arm Sorting System")
print("-------------------------------------")
print("1 = Target Posisi 1")
print("2 = Target Posisi 2")
print("3 = Target Posisi 3")
print("4 = Target Posisi 4")
print("5 = Target Posisi 5")
print()
print("SPACE = Pick & Place")
print("H = HOME")
print("R = Reload servo.json")
print("ESC = Exit")
print("-------------------------------------")


# ==========================================================
# VARIABLE
# ==========================================================

TARGET = 3

current_position = None

last_position = None

busy = False


# ==========================================================
# LOOP
# ==========================================================

def robot_worker(source, target):
    global busy

    robot.pick_and_place(source, target)

    busy = False

while True:

    frame = cam.read()

    if frame is None:
        continue

    center = cam.get_center()

    frame, current_position = vision.process(frame, center)

    # ======================================================
    # Informasi
    # ======================================================

    cv2.putText(
        frame,
        f"TARGET : {TARGET}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        2
    )

    cv2.putText(
        frame,
        f"OBJECT : {current_position}",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    if busy:

        cv2.putText(
            frame,
            "STATUS : ROBOT WORKING",
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2
        )

    else:

        cv2.putText(
            frame,
            "STATUS : READY",
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    # ======================================================
    # Posisi berubah
    # ======================================================

    if current_position != last_position:

        if current_position is not None:

            print(f"Objek berada di Area {current_position}")

        last_position = current_position

    # ======================================================

    cv2.imshow("Robot Arm Sorting", frame)

    key = cv2.waitKey(1) & 0xFF

    # ======================================================
    # EXIT
    # ======================================================

    if key == 27:

        break

    # ======================================================
    # TARGET
    # ======================================================

    elif key == ord('1'):

        TARGET = 1

        print("Target =", TARGET)

    elif key == ord('2'):

        TARGET = 2

        print("Target =", TARGET)

    elif key == ord('3'):

        TARGET = 3

        print("Target =", TARGET)

    elif key == ord('4'):

        TARGET = 4

        print("Target =", TARGET)

    elif key == ord('5'):

        TARGET = 5

        print("Target =", TARGET)

    # ======================================================
    # HOME
    # ======================================================

    elif key == ord('h'):

        print("HOME")

        robot.home()

    # ======================================================
    # RELOAD servo.json
    # ======================================================

    elif key == ord('r'):

        robot.load_pose()

    # ======================================================
    # PICK & PLACE
    # ======================================================

    elif key == 32:

        if busy:

            continue

        if current_position is None:

            print("Objek tidak ditemukan")

            continue

        if current_position == TARGET:

            print("Objek sudah berada di target")

            continue

        busy = True

        print("--------------------------------")
        print("START PICK & PLACE")
        print("FROM :", current_position)
        print("TO   :", TARGET)
        print("--------------------------------")

        threading.Thread(
            target=robot_worker,
            args=(current_position, TARGET),
            daemon=True
        ).start()


# ==========================================================
# CLOSE
# ==========================================================

cam.release()

robot.disconnect()

cv2.destroyAllWindows()