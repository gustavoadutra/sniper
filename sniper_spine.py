import cv2

# ===============
#    VARIABLES
# ===============

# CAMERA ACTIVATION
webcam_shooter = cv2.VideoCapture(0)
webcam_shooter.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
webcam_shooter.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

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
# DEFINE LIST HERE
# ================


def keyboard_control(key_selected):
    key_selected[0] += 1
    if (key_selected[0] % 2) == 0:
        key_selected[1] = False
    else:
        key_selected[1] = True
    print(key_selected, key_selected[0], key_selected[1])


# ================
#      CODE
# ================


while True:

    success, frame_shooter = webcam_shooter.read()
    frame_shooter = cv2.flip(frame_shooter, 1)

    cv2.namedWindow('Shooter View')

    # ====================
    #  KEYBOARD STATEMENT
    # ====================

    if key_a[1] is True:  # Adjustment on Screen
        print('Adjustment on Screen')

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

    if key_p[1] is True:  # Print Sniper View
        key_p[1] = False

    if key_r[1] is True:  # Reset the ROI
        print('Tracker Reset')
        key_r[1] = False

    # ===================
    #    CODE SCREEN
    # ===================
    
    cv2.imshow('Shooter View', frame_shooter)

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
        keyboard_control(key_p)

    elif key == ord('r'):  # 114 Reset the ROI
        keyboard_control(key_r)

    elif key == ord('q'):  # 113 Exit Program
        print('Break')
        break

# DISABLE CAMERA
webcam_shooter.release()

# CLOSE WINDOWS
cv2.destroyAllWindows()
