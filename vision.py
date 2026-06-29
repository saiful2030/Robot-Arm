import json
import os
import cv2

from config import AREA_FILE
from config import FONT
from config import FONT_SCALE
from config import FONT_THICKNESS
from config import COLOR_GREEN
from config import COLOR_RED


class Vision:

    def __init__(self):

        self.areas = {}

        self.load_area()

    # ======================================================

    def load_area(self):

        if not os.path.exists(AREA_FILE):

            print("area.json tidak ditemukan")

            return

        with open(AREA_FILE, "r") as f:

            self.areas = json.load(f)

        print("Area Loaded")

    # ======================================================

    def draw_area(self, frame):

        for key, value in self.areas.items():

            xmin = value["xmin"]
            ymin = value["ymin"]
            xmax = value["xmax"]
            ymax = value["ymax"]

            cv2.rectangle(
                frame,
                (xmin, ymin),
                (xmax, ymax),
                COLOR_GREEN,
                2
            )

            cv2.putText(
                frame,
                key,
                (xmin + 10, ymin + 30),
                FONT,
                FONT_SCALE,
                COLOR_RED,
                FONT_THICKNESS
            )

        return frame

    # ======================================================

    def get_position(self, center):

        if center is None:

            return None

        cx, cy = center

        for key, value in self.areas.items():

            if (value["xmin"] <= cx <= value["xmax"] and
                value["ymin"] <= cy <= value["ymax"]):

                return int(key)

        return None

    # ======================================================

    def process(self, frame, center):

        frame = self.draw_area(frame)

        posisi = self.get_position(center)

        if posisi is not None:

            cv2.putText(
                frame,
                f"OBJECT : AREA {posisi}",
                (20, 80),
                FONT,
                1,
                (255, 0, 0),
                2
            )

        else:

            cv2.putText(
                frame,
                "OBJECT : NOT FOUND",
                (20, 80),
                FONT,
                1,
                (0, 0, 255),
                2
            )

        return frame, posisi


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    from camera import Camera

    cam = Camera()

    vision = Vision()

    while True:

        frame = cam.read()

        if frame is None:
            continue

        center = cam.get_center()

        frame, posisi = vision.process(frame, center)

        cv2.imshow("Vision Test", frame)

        if cv2.waitKey(1) == 27:
            break

    cam.release()

    cv2.destroyAllWindows()