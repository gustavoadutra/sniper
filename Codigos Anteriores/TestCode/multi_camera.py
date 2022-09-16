import cv2
# (1920,1080)
HIGH_VALUE = 900
WIDTH = HIGH_VALUE
HEIGHT = HIGH_VALUE

webcam_zer = cv2.VideoCapture(0)

webcam_zer.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
webcam_zer.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
width = int(webcam_zer.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(webcam_zer.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(width, height)



# --- WebCam1
# webcam_zer = cv2.VideoCapture(0)  # SNIPER
# webcam_zer.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# webcam_zer.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# --- WebCam2
# webcam_one = cv2.VideoCapture(0)
# webcam_one.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
# webcam_one.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)


cam = cv2.VideoCapture(0)

# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # set new dimensionns to cam object (not cap)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


if webcam_zer.isOpened():  # and webcam_one.isOpened():
    _, frame_zer = webcam_zer.read()
    # print(frame_zer.shape, 'frame_zer')

    # _, frame_one = webcam_one.read()
    # print(frame_one.shape, 'frame_one')

    while True:
        _, frame_zer = webcam_zer.read()
        # _, frame_one = webcam_one.read()

        cv2.imshow('frame 0', frame_zer)
        # cv2.imshow('frame 1', frame_one)

        if cv2.waitKey(1) == ord('q'):
            break

webcam_zer.release()
# webcam_one.release()
cv2.destroyAllWindows()
