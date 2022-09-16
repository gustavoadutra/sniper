import cv2
#  import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
#cap.set(4, 800)


if cap.isOpened():
    _, frame = cap.read()

    while True:
        _, frame = cap.read()

        cv2.imshow('View', frame)
        print(frame.shape[0],frame.shape[1])

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Esc
            print('Esc', key)
            break

cap.release()
cv2.destroyAllWindows()
