import time
import dynamixel
import cv2

mouseX = 0
mouseY = 0
key_h = [0, False]


def keyboard_control(key_selected):
    key_selected[0] += 1
    if (key_selected[0] % 2) == 0:
        key_selected[1] = False
    else:
        key_selected[1] = True
    print(key_selected, key_selected[0], key_selected[1])


def mouse_detection(event, mouse_x, mouse_y, flag, param):  # Mouse Parameters
    global mouseX, mouseY

    if event == cv2.EVENT_LBUTTONDOWN and key_h[1]:  # Center Cameras
        print(mouseX, mouseY)
        vig.go_motor(mouseX, mouseY)
        mouseX, mouseY = 0, 0

    mouseX, mouseY = mouse_x, mouse_y


def camera_usage(cam):
    cap = cv2.VideoCapture(cam)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignorando frame da camera vazio.")
            # If loading a video, use 'break' instead of 'continue'.
            print("Abrindo novamente a camera.")
            cap = cv2.VideoCapture(cam)
            continue

        cv2.imshow('Camera', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(5) & 0xFF == ord('h'):
            keyboard_control(key_h)

        cv2.setMouseCallback('Camera', mouse_detection)


vig = dynamixel.VigilantMotors()
camera_usage(3)

