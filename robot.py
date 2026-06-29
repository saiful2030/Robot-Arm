import serial
import time
import json

from config import COM_PORT
from config import BAUDRATE
from config import SERIAL_TIMEOUT
from config import MOVE_DELAY


class RobotArm:

    # ======================================================

    def __init__(self):

        self.ser = None

        self.pose = {}

        self.base = 90
        self.shoulder = 90
        self.elbow = 90
        self.gripper = 90

        self.load_pose()

    # ======================================================

    def load_pose(self):

        with open("data/servo.json", "r") as f:

            self.pose = json.load(f)

        print("Servo Pose Loaded")

    # ======================================================

    def connect(self):

        try:

            self.ser = serial.Serial(
                COM_PORT,
                BAUDRATE,
                timeout=SERIAL_TIMEOUT
            )

            time.sleep(2)

            print("Arduino Connected")

            while self.ser.in_waiting:

                print(
                    self.ser.readline().decode().strip()
                )

            return True

        except Exception as e:

            print(e)

            return False

    # ======================================================

    def disconnect(self):

        if self.ser:

            self.ser.close()

            print("Arduino Disconnected")

    # ======================================================

    def send(self, command):

        if self.ser is None:

            return False

        command += "\n"

        self.ser.write(command.encode())

        time.sleep(MOVE_DELAY)

        if self.ser.in_waiting:

            reply = self.ser.readline().decode().strip()

            print(reply)

            return reply

        return ""

    # ======================================================

    def move_base(self, angle):

        angle = max(0, min(180, int(angle)))

        self.base = angle

        self.send(f"B{angle}")

    # ======================================================

    def move_shoulder(self, angle):

        angle = max(0, min(180, int(angle)))

        self.shoulder = angle

        self.send(f"S{angle}")

    # ======================================================

    def move_elbow(self, angle):

        angle = max(0, min(180, int(angle)))

        self.elbow = angle

        self.send(f"E{angle}")

    # ======================================================

    def move_gripper(self, angle):

        angle = max(0, min(180, int(angle)))

        self.gripper = angle

        self.send(f"G{angle}")

    # ======================================================

    def move(self, base, shoulder, elbow, gripper):

        self.move_base(base)
        self.move_shoulder(shoulder)
        self.move_elbow(elbow)
        self.move_gripper(gripper)

    # ======================================================

    def goto(self, position):

        position = str(position)

        if position not in self.pose:

            print("Pose tidak ditemukan")

            return

        p = self.pose[position]

        print("Goto :", position)

        self.move_base(p["base"])
        self.move_shoulder(p["shoulder"])
        self.move_elbow(p["elbow"])

        if "gripper" in p:
            self.move_gripper(p["gripper"])

    # ======================================================

    def home(self):

        p = self.pose["home"]

        print("HOME")

        self.move_base(p["base"])
        self.move_shoulder(p["shoulder"])
        self.move_elbow(p["elbow"])

        if "gripper" in p:
            self.move_gripper(p["gripper"])

    # ======================================================

    def open(self):

        angle = self.pose["gripper"]["open"]

        self.move_gripper(angle)

    # ======================================================

    def close(self):

        angle = self.pose["gripper"]["close"]

        self.move_gripper(angle)

    # ======================================================

    def status(self):

        self.send("STATUS")

    # ======================================================

    def pick(self, position):

        print("PICK :", position)

        self.goto(position)

        time.sleep(0.5)

        self.close()

        time.sleep(0.5)

    # ======================================================

    def place(self, position):

        print("PLACE :", position)

        self.goto(position)

        time.sleep(0.5)

        self.open()

        time.sleep(0.5)

    # ======================================================

    def pick_and_place(self, source, target):

        self.home()
        time.sleep(1)

        self.goto(source)
        time.sleep(1)

        self.close()
        time.sleep(1)

        self.goto(f"{source}_up")
        time.sleep(1)

        # self.home()
        # time.sleep(1)

        self.goto(target)
        time.sleep(1)

        self.open()
        time.sleep(1)

        self.goto(f"{target}_up")
        time.sleep(1)

        # Baru pulang
        self.home()

    # ======================================================

    def test(self):

        for i in range(1, 6):

            self.goto(i)

            time.sleep(2)

        self.home()


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    robot = RobotArm()

    if robot.connect():

        robot.home()

        time.sleep(2)

        robot.pick_and_place(5,3)

        robot.disconnect()