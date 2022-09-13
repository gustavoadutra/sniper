import cv2
import numpy as np
import mediapipe as mp

bright = 80
contrast = 100

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

webcam = cv2.VideoCapture(0)  # 640x480
webcam.set(3, 640)  # Width
webcam.set(4, 480)  # Height
webcam.set(10, bright)  # Bright
webcam.set(11, contrast)  # Contrast

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyes_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

myColors = [['DARK GRAY', (55, 55, 55)],
            ['BLUE', (255, 0, 0)],
            ['GREEN', (0, 255, 0)],
            ['RED', (0, 0, 255)],
            ['BLACK', (0, 0, 0)],
            ['WHITE', (255, 255, 255)],
            ['DARK GREEN', (100, 130, 20)]]  # BGR

mySkin = [[myColors[4][0], 0, int((-0.5 * bright) + 105), int(bright * 1.1),
           16, int((-1.5 * bright) + 330), 255, myColors[4][1]]]  # BGR


def faces_and_eyes(frames, bgr_face, bgr_eyes):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frames, (x, y), (x + w, y + h), bgr_face, 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frames[y:y + h, x:x + w]
        eyes = eyes_detector.detectMultiScale(roi_gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), bgr_eyes, 2)


def aim_print(frames, center_y, center_x, color):
    cv2.circle(frames, (center_y, center_x), 3, color, 0)
    cv2.line(frames, (center_y, center_x + 30), (center_y, center_x + 5), color, 1)
    cv2.line(frames, (center_y, center_x + 45), (center_y, center_x + 30), color, 2)
    cv2.line(frames, (center_y + 30, center_x), (center_y + 5, center_x), color, 1)
    cv2.line(frames, (center_y + 45, center_x), (center_y + 30, center_x), color, 2)
    cv2.line(frames, (center_y - 30, center_x), (center_y - 5, center_x), color, 1)
    cv2.line(frames, (center_y - 45, center_x), (center_y - 30, center_x), color, 2)
    return


def find_skin(frames, my_skin):
    img_hsv = cv2.cvtColor(frames, cv2.COLOR_BGR2HSV)
    count = 0
    for skin in my_skin:
        lower = np.array(skin[1:4])
        upper = np.array(skin[4:7])
        mask = cv2.inRange(img_hsv, lower, upper)
        mask_blur = cv2.GaussianBlur(mask, (3, 3), 0)
        x, y = get_contours(mask_blur)
        cv2.circle(imgResult, (x, y + 30), 2, my_skin[count][7], cv2.FILLED)  # target central
        count += 1


def get_contours(frames):
    contours, hierarchy = cv2.findContours(frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def mouse_detection(event, mouse_x, mouse_y, flag, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('L DOWN', flag, param)
        print(mouse_x, mouse_y)
        math_behind(mouse_x, mouse_y, centery, centerx)
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.imwrite("save{0}.jpg".format(str(mouse_x + mouse_y)), frame)  #        FAZER ITERAçÃO


def math_behind(mouse_x, mouse_y, center_x, center_y):
    axes_motor_x = mouse_x - center_x
    axes_motor_y = mouse_y - center_y
    aim_distance = np.sqrt(axes_motor_x ** 2 + axes_motor_y ** 2)
    print('Distance to Aim: ', aim_distance)
    print('X: ', axes_motor_x, 'Y: ', axes_motor_y)


if webcam.isOpened():
    _, frame = webcam.read()
    centerx = int(frame.shape[0] * 0.5)
    centery = int(frame.shape[1] * 0.5)
    cv2.namedWindow('follow')
    cv2.setMouseCallback('follow', mouse_detection)

    while True:
        _, frame = webcam.read()
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = frame.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 3, (myColors[6][1]), cv2.FILLED)

        # aim_print(frame, centery, centerx, (myColors[6][1]))
        imgResult = frame.copy()
        # find_skin(frame, mySkin)
        # faces_and_eyes(imgResult, (myColors[1][1]), (myColors[2][1]))

        cv2.imshow('follow', imgResult)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



webcam.release()
cv2.destroyAllWindows()
