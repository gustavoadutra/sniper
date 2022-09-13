# imports
import cv2
import mediapipe
import pyautogui
import time
import numpy as np

cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mediapipe.solutions.drawing_utils
wSrc, hSrc = pyautogui.size()  # 1360 x 768 = screen size
preX, preY = 0, 0
currentX, CurrentY = 0, 0


def handLandmark(colorImg):
    landmarkList = []
    landmarkPositions = mainHand.process(colorImg)
    landmarkCheck = landmarkPositions.multi_hand_landmarks
    if landmarkCheck:
        for hand in landmarkCheck:
            for index, landmark in enumerate(hand.landmark):
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS)
                h, w, c = img.shape  # height, width, channel
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)

                landmarkList.append([index, centerX, centerY])
    return landmarkList


def fingers(landmarks):
    fingerTips = []
    tipIds = [4, 8, 12, 16, 20]

    if landmarks[tipIds[0]][1] < landmarks[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    for ids in range(1, 5):
        if landmarks[tipIds[ids]][2] < landmarks[tipIds[ids] - 2][2]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips


if cap.isOpened():
    _, img = cap.read()
    hImg, wImg, _, = img.shape

    while True:
        _, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lmList = handLandmark(imgRGB)
        if len(lmList) != 0:
            finger = fingers(lmList)

            ##################################################################
            #  POSITION FINGER'S LIST
            ##################################################################

            if finger == [1, 1, 1, 1, 1]:
                print('all up')
            elif finger == ([0, 1, 0, 0, 0]):  # move mouse using 1 fingers

                x1, y1 = lmList[8][1:]
                x3 = np.interp(x1, (wImg * 0.5, wImg * 0.95), (1, wSrc - 2))
                y3 = np.interp(y1, (hImg * 0.1, hImg * 0.5), (1, hSrc - 2))
                currentX = int(preX + (x3 - preX) / 5)
                currentY = int(preY + (y3 - preY) / 5)
                pyautogui.moveTo(currentX, currentY)
                preX, preY = currentX, currentY
                print('move to {0} x {1}'.format(currentX, currentY))

            elif finger == [1, 1, 0, 0, 0]:  # left click
                pyautogui.leftClick()
                time.sleep(0.4)
                print('left click')
            elif finger == [0, 1, 0, 0, 1]:  # right click
                pyautogui.rightClick()
                time.sleep(0.4)
                print('right click')
            elif finger == [0, 0, 0, 0, 0]:
                print('all close!')
                # break

            else:
                print('none', finger)

            ############################################################

        cv2.imshow("webcam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
