import cv2
import json
import os

# ===============================
# Kamera
# ===============================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ===============================

areas = {}

current_area = 1

points = []

# ===============================

def save_json():

    if not os.path.exists("data"):
        os.makedirs("data")

    with open("data/area.json", "w") as f:
        json.dump(areas, f, indent=4)

    print("Area berhasil disimpan")


# ===============================

def mouse(event, x, y, flags, param):

    global points
    global current_area

    if event == cv2.EVENT_LBUTTONDOWN:

        points.append((x, y))

        print(f"Klik : {x} {y}")

        if len(points) == 2:

            x1, y1 = points[0]
            x2, y2 = points[1]

            xmin = min(x1, x2)
            xmax = max(x1, x2)

            ymin = min(y1, y2)
            ymax = max(y1, y2)

            areas[str(current_area)] = {

                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax

            }

            print("Area", current_area, "tersimpan")

            current_area += 1

            points.clear()

            if current_area > 5:

                save_json()

# ===============================

cv2.namedWindow("Calibration")

cv2.setMouseCallback("Calibration", mouse)

# ===============================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # gambar area

    for key in areas:

        a = areas[key]

        cv2.rectangle(

            frame,

            (a["xmin"], a["ymin"]),

            (a["xmax"], a["ymax"]),

            (0,255,0),

            2

        )

        cv2.putText(

            frame,

            key,

            (a["xmin"], a["ymin"]-10),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0,0,255),

            2

        )

    # posisi mouse

    if len(points)==1:

        cv2.circle(frame, points[0],5,(255,0,0),-1)

    cv2.putText(

        frame,

        f"Kalibrasi Area : {current_area}",

        (20,40),

        cv2.FONT_HERSHEY_SIMPLEX,

        1,

        (255,0,0),

        2

    )

    cv2.imshow("Calibration", frame)

    key = cv2.waitKey(1)

    if key == 27:

        break

cap.release()

cv2.destroyAllWindows()