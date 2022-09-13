from __future__ import print_function
from pynput.keyboard import Controller
import cv2  # opencv-contrib-python
import serial
import datetime
import mediapipe as mp
import os

# For USB input:
cap0 = cv2.VideoCapture(0)  # frame_sniper
arduino = serial.Serial(port="COM3", baudrate=57600)

# Variables
key_g = [0, False]
key_x = [0, False]
key_r = [0, False]
key_b = [0, False]
key_p = [0, False]
mouseX = 0
mouseY = 0
r_ROI_X = 30  # Range ROI
r_ROI_Y = 60  # Range ROI

# Google MediaPipe Stuff
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


#  Define list here

# Mouse Parameters
def mouse_detection(event, mouse_x, mouse_y, flag, param):
    global mouseX, mouseY, r_ROI_X, r_ROI_Y, bbox

    if event == cv2.EVENT_RBUTTONDOWN:

        print('R BUTTON DOWN', param)

    # Press LEFT Mouse Button - Create ROI Square
    if event == cv2.EVENT_LBUTTONDOWN and (key_g[1] is True):
        print('L BUTTON DOWN - ROI SELECTION')
        bbox = (ret_xi, ret_yi, (r_ROI_X * 2), (r_ROI_Y * 2))  # (Xi,Yi,Width,Height)
        tracker.init(frame_sniper, bbox)
        print('Tracker initializing{}'.format(bbox))
        Controller().press('g')

    # MouseWheel Grow the Square ROI
    if event == cv2.EVENT_MOUSEWHEEL:
        if flag > 0:
            r_ROI_X = r_ROI_X + 3
            r_ROI_Y = r_ROI_Y + 3
        if flag < 0:
            r_ROI_X = r_ROI_X - 3
            r_ROI_Y = r_ROI_Y - 3

        print('new range: ROI X =', r_ROI_X, 'ROI Y =', r_ROI_Y)

    mouseX, mouseY = mouse_x, mouse_y
    r_ROI_X, r_ROI_Y = r_ROI_X, r_ROI_Y

#  with... (cap0)
if cap0.isOpened():
    _, frame_sniper = cap0.read()

    tracker = cv2.legacy.TrackerTLD_create()

    center_x = int(frame_sniper.shape[1] * 0.5)
    center_y = int(frame_sniper.shape[0] * 0.5)

    while True:  # while 'process webcam and track objects'
        _, frame_sniper = cap0.read()

        cv2.namedWindow('View')
        cv2.setMouseCallback('View', mouse_detection)





        # get updated location of objects in subsequent frames
        _, bbox = tracker.update(frame_sniper)

        # Draw tracked objects
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame_sniper, p1, p2, (255, 0, 0), 2, 1)

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # Reset the ROI
        if key_r[1] is True:
            tracker = cv2.legacy.TrackerTLD_create()
            print('Tracker Reseted')
            Controller().press('r')

        # Turn ON Green Laser Pointer
        if key_b[1] is True:
            arduino.write(b'a')

        # Print Sniper View
        if key_p[1] is True:
            # now = datetime.datetime.now()
            # cv2.imwrite((os.path.join('guest', 'target{}{}{}{}.jpg'.format(now.day, now.hour, now.minute, now.second))),
                    # image_sniper[Yinit:Yout, Xinit:Xout])
            Controller().press('p')

        #
        if key_x[1] is True:

            Controller().press('x')

        # Turn ON the Selection of a ROI
        if key_g[1] is True:
            # Create a DRAW rectangle of a ROI
            ret_xi = mouseX - r_ROI_X
            ret_yi = mouseY - r_ROI_Y
            ret_xo = mouseX + r_ROI_X
            ret_yo = mouseY + r_ROI_X
            cv2.rectangle(frame_sniper, (int(ret_xi), int(ret_yi)), (int(ret_xo), int(ret_yo)), (100, 130, 20), 2)

        # show frame
        cv2.imshow('View', frame_sniper)

        # KEYBOARD CONTROL
        key = cv2.waitKey(1) & 0xFF

        # Turn ON Green Laser Pointer
        if key == ord('b'):  # 98
            key_b[0] = 1 + key_b[0]
            if (key_b[0] % 2) == 0:
                key_b[1] = False
                arduino.write(b'c')
            if (key_b[0] % 2) != 0:
                key_b[1] = True
            print('b', key, key_b[0], key_b[1])

        #  Reset the ROI
        if key == ord('r'):  # 114
            key_r[0] = 1 + key_r[0]
            if (key_r[0] % 2) == 0:
                key_r[1] = False
            if (key_r[0] % 2) != 0:
                key_r[1] = True
            print('r', key, key_r[0], key_r[1])

        if key == ord('x'):  # 120
            key_x[0] = 1 + key_x[0]
            if (key_x[0] % 2) == 0:
                key_x[1] = False
            if (key_x[0] % 2) != 0:
                key_x[1] = True
            print('x', key, key_x[0], key_x[1])

        # Turn ON the Selection of a ROI
        if key == ord('g'):  # 119
            key_g[0] = 1 + key_g[0]
            if (key_g[0] % 2) == 0:
                key_g[1] = False
            if (key_g[0] % 2) != 0:
                key_g[1] = True
            print('g', key, key_g[0], key_g[1])

        if key == 27:  # Esc
            arduino.close()
            print('End of process', key)
            break

cap0.release()
cv2.destroyAllWindows()
