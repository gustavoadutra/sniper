import cv2
from sniper_utils import *


# ===============
#    VARIABLES
# ===============

# CAMERA ACTIVATION
webcam_shooter = cv2.VideoCapture(3)
webcam_shooter.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
webcam_shooter.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

webcam_spotter = cv2.VideoCapture(0)  # CAM
webcam_spotter.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
webcam_spotter.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

# SELECTOR KEYBOARD
key_a = [0, False]  # Adjustment on Screen/Calibrate
key_l = [0, False]  # Turn ON Green Laser Pointer
key_m = [0, False]  # Activate MediaPipe
key_o = [0, False]  # Turn ON/OFF the ROI images
key_c = [0, False]  # Turn 'manual' Control Cameras
key_p = [0, False]  # Print Sniper View
key_q = [0, False]  # Exit Program
key_r = [0, False]  # Reset the ROI
key_x = [0, False]  # motor x turn ON
key_y = [0, False]  # motor y turn ON

# COLORS
BGR = [(55, 55, 55),  # DARK GRAY
       (255, 0, 0),  # BLUE
       (0, 255, 0),  # GREEN
       (0, 0, 255),  # RED
       (0, 0, 0),  # BLACK
       (255, 255, 255),  # WHITE
       (100, 130, 20),  # DARK GREEN
       (255, 0, 255),  # YELLOW
       (0, 255, 255)]  # PURPLE


# ================
#      CODE
# ================


while True:

    _, frame_shooter = webcam_shooter.read()  # shooter
    frame_shooter = cv2.flip(frame_shooter, 1)
    center_x_shooter = int(frame_shooter.shape[1] * 0.5)
    center_y_shooter = int(frame_shooter.shape[0] * 0.5)

    _, frame_spotter = webcam_spotter.read()  # spotter
    frame_spotter = cv2.flip(frame_spotter, 1)
    center_x_spotter = int(frame_spotter.shape[1] * 0.5)
    center_y_spotter = int(frame_spotter.shape[0] * 0.5)

    cv2.namedWindow('Shooter View')
    cv2.namedWindow('Spotter View')
    # ====================
    #  KEYBOARD STATEMENT
    # ====================

    if key_a[1] is True:  # Adjustment on Screen
        cv2.line(frame_shooter, (center_x_shooter, 0), (center_x_shooter, frame_shooter.shape[0]), (BGR[7]), 1)
        cv2.line(frame_shooter, (0, center_y_shooter), (frame_shooter.shape[1], center_y_shooter), (BGR[8]), 1)
        cv2.line(frame_spotter, (center_x_spotter, 0), (center_x_spotter, frame_spotter.shape[0]), (BGR[7]), 1)
        cv2.line(frame_spotter, (0, center_y_spotter), (frame_spotter.shape[1], center_y_spotter), (BGR[8]), 1)

    if key_l[1] is True:  # Laser
        print('Enable Green Laser Pointer')

    if key_m[1] is True:  # Activate MediaPipe
        print('Activate Mediapipe')

    if key_o[1] is True:  # Turn ON the Selection of a ROI
        print('Turn on ROI')

    if (key_c[1] and key_x[1]) is True:  # Open X
        print('Open X')

    if (key_c[1] and key_y[1]) is True:  # Open Y
        print('Open Y')

    if key_r[1] is True:  # Reset the ROI
        print('Tracker Reset')
        key_r[1] = False

    # ===================
    #    CODE SCREEN
    # ===================

    cv2.imshow('Shooter View', frame_shooter)
    cv2.imshow('Spotter View', frame_spotter)

    # ========================
    #    KEYBOARD CONTROL
    # ========================

    key = cv2.waitKey(1) & 0xFF

    if key == ord('a'):  # 119 Adjustment on Screen
        keyboard_control(key_a)

    elif key == ord('l'):  # 98 Turn ON Green Laser Pointer
        keyboard_control(key_l)

    elif key == ord('m'):  # 120 Activate MediaPipe
        keyboard_control(key_m)

    elif key == ord('o'):  # 119 Turn ON/OFF the ROI images
        keyboard_control(key_o)

    elif key == ord('c'):  # 104 Turn Open chanel to control motors
        keyboard_control(key_c)

    elif key == ord('p'):  # 112 Print Sniper View
        sniper_print(frame_shooter)

    elif key == ord('r'):  # 114 Reset the ROI
        keyboard_control(key_r)

    elif key == ord('q'):  # 113 Exit Program
        print('Break')
        break

# DISABLE CAMERA
webcam_shooter.release()
webcam_spotter.release()

# CLOSE WINDOWS
cv2.destroyAllWindows()
