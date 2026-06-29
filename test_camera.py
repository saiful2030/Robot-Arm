import cv2

cap = cv2.VideoCapture(0)

print("Open:", cap.isOpened())

while True:
    ret, frame = cap.read()

    if not ret:
        print("Frame gagal")
        continue

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()