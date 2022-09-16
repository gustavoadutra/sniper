import cv2

cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    cv2.imshow('video output', img)

    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
