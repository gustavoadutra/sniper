# import pyautogui as pg
from __future__ import print_function
import datetime
import cv2
import mediapipe as mp
import os

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# For webcam input:
cap0 = cv2.VideoCapture(0)  # frame_sniper
#cap1 = cv2.VideoCapture(1)  # frame_observer

# Variables
key_g = [0, False]
mouseX = 0
mouseY = 0
range_ROI = 50


# Define list here
def holistic_aim(frame_sniper):  # MediaPipe in the Sniper View

    image_sniper = cv2.cvtColor(frame_sniper, cv2.COLOR_BGR2RGB)
    image_sniper.flags.writeable = False
    results = holistic.process(image_sniper)
    image_sniper.flags.writeable = True
    image_sniper = cv2.cvtColor(image_sniper, cv2.COLOR_RGB2BGR)


    mp_drawing.draw_landmarks(image_sniper, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # mp_holistic.POSE_CONNECTIONS <= lines/connections
    # landmark_drawing_spec <= pointers

    if results.pose_landmarks is not None:  # no math if no target

        # coordinates = (left eye + right eye / 2) * screen center
        x_sniper = int((results.pose_landmarks.landmark[2].x + results.pose_landmarks.landmark[5].x) * center_x)
        y_sniper = int((results.pose_landmarks.landmark[2].y + results.pose_landmarks.landmark[5].y) * center_y)

        distance_sniper_center_x = center_x - x_sniper
        distance_sniper_center_y = center_y - y_sniper

        cv2.line(image_sniper, (x_sniper, y_sniper), (center_x, center_y), (100, 130, 20), 4)
        cv2.putText(image_sniper, f'x:{x_sniper} y:{y_sniper}', (x_sniper, y_sniper - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (17, 70, 244), 2)  # hypotenuse

        cv2.line(image_sniper, (x_sniper, center_y), (center_x, center_y), (100, 130, 20), 2)
        cv2.putText(image_sniper, f'{distance_sniper_center_x}', (x_sniper, center_y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (17, 70, 244), 2)  # x

        cv2.line(image_sniper, (center_x, y_sniper), (center_x, center_y), (100, 130, 20), 4)
        cv2.putText(image_sniper, f'{distance_sniper_center_y}', (center_x + 20, y_sniper + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (17, 70, 244), 2)  # y

        aim_sq = 50
        if distance_sniper_center_x in range(-aim_sq, aim_sq) and distance_sniper_center_y in range(-aim_sq, aim_sq):
            mp_drawing.draw_landmarks(image_sniper, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                                  landmark_drawing_spec=None,
                                  connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

    return image_sniper


def mouse_detection(event, mouse_x, mouse_y, flag, param):  # Mouse Parameters
    global mouseX, mouseY, range_ROI

    if event == cv2.EVENT_RBUTTONDOWN:
        print('R DOWN', mouse_x, mouse_y)

    elif (event == cv2.EVENT_LBUTTONDOWN) and (key_g[1] is True):

        now = datetime.datetime.now()
        print('L DOWN, ROI Add ON')  # Region of Interest
        cv2.imwrite((os.path.join('guest', 'target{}{}{}{}.jpg'.format(now.day, now.hour, now.minute, now.second))),
                    image_sniper[mouse_y - range_ROI:mouse_y + range_ROI, mouse_x - range_ROI:mouse_x + range_ROI])

    elif event == cv2.EVENT_MOUSEWHEEL:
        if flag > 0:
            range_ROI = range_ROI +1
        if flag < 0:
            range_ROI = range_ROI - 1
        print('range_ROI =', range_ROI)

    mouseX, mouseY = mouse_x, mouse_y


with mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8) as holistic:

    if cap0.isOpened():# and cap1.isOpened():
        _, frame_sniper = cap0.read()
        frame_sniper = cv2.flip(frame_sniper, 1)

        #_, frame_observer = cap1.read()

        center_x = int(frame_sniper.shape[1] * 0.5)
        center_y = int(frame_sniper.shape[0] * 0.5)

        while True:  # while 'process webcam and track objects'
            _, frame_sniper = cap0.read()
            frame_sniper = cv2.flip(frame_sniper, 1)

            #_, frame_observer = cap1.read()

            cv2.namedWindow('Sniper View')
            cv2.setMouseCallback('Sniper View', mouse_detection)

            image_sniper = holistic_aim(frame_sniper)
            if key_g[1] is True:
                cv2.rectangle(image_sniper, (mouseX - (range_ROI+2), mouseY - (range_ROI+2)),
                              (mouseX + (range_ROI+1), mouseY + (range_ROI+1)), (100, 130, 20), 2)


            cv2.imshow('Sniper View', image_sniper)

            #cv2.imshow('Observer View', frame_observer)

            # KEYBOARD CONTROL
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):  # 113
                print('q', key)

            # Adjustment on Screen
            elif key == ord('a'):  #
                print('X',frame_sniper.shape[1])
                print('Y', frame_sniper.shape[0])
                print('a', key)

            # Turn ON/OFF the ROI images
            elif key == ord('g'):  # 119

                key_g[0] = 1 + key_g[0]
                if (key_g[0] % 2) == 0:
                    key_g[1] = False
                if (key_g[0] % 2) != 0:
                    key_g[1] = True

                print('g', key, key_g[0], key_g[1])

            elif key == ord('m'):  # 109
                print('m', key)
                print('g - Muda ON/OFF a opção do ROI')
                print('m - Opções do Teclado')
                print('Esc - Encerra o Programa')

            elif key == 27:  # Esc
                print('Esc', key)
                break

cap0.release()
#cap1.release()
cv2.destroyAllWindows()
