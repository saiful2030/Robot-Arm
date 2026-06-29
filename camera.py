import cv2
import numpy as np
import time


class Camera:

    def __init__(self, camera_id=0):

        self.cap = cv2.VideoCapture(camera_id)
        print("Open :", self.cap.isOpened())

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.lower_yellow = np.array([20, 100, 100])
        self.upper_yellow = np.array([35, 255, 255])

        self.frame = None
        self.center = None

        self.fps = 0
        self.prev = time.time()

    # ======================================================

    def set_hsv(self, lower, upper):

        self.lower_yellow = np.array(lower)
        self.upper_yellow = np.array(upper)

    # ======================================================

    def read(self):

        ret, frame = self.cap.read()


        if not ret:
            return None

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(
            hsv,
            self.lower_yellow,
            self.upper_yellow
        )

        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        self.center = None

        if len(contours) > 0:

            biggest = max(contours, key=cv2.contourArea)

            area = cv2.contourArea(biggest)

            if area > 500:

                x, y, w, h = cv2.boundingRect(biggest)

                cx = x + w // 2
                cy = y + h // 2

                self.center = (cx, cy)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (cx, cy),
                    5,
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    f"({cx},{cy})",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        now = time.time()

        self.fps = 1 / (now - self.prev)

        self.prev = now

        cv2.putText(
            frame,
            f"FPS : {int(self.fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

        self.frame = frame

        return frame

    # ======================================================

    def get_center(self):

        return self.center

    # ======================================================

    def get_frame(self):

        return self.frame

    # ======================================================

    def release(self):

        self.cap.release()


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    cam = Camera()

    while True:

        frame = cam.read()

        if frame is None:
            continue

        cv2.imshow("Robot Arm Camera", frame)

        key = cv2.waitKey(1)

        if key == 27:
            break

    cam.release()

    cv2.destroyAllWindows()