import cv2
webcam_zer = cv2.VideoCapture(0)  # CAM

key_a = [0, False]  # Adjustment on Screen/Calibrate
key_b = [0, False]  # Turn ON Green Laser Pointer
key_e = [0, False]  # Activate MediaPipe
key_g = [0, False]  # Turn ON/OFF the ROI images
key_h = [0, False]  # Turn 'manual' Control Cameras
key_m = [0, False]  # Keyboard Mapping
key_o = [0, False]  # Motors follow Mouse
key_p = [0, False]  # Print Sniper View
key_q = [0, False]  # Exit Program
key_r = [0, False]  # Reset the ROI
key_x = [0, False]  # motor x turn ON
key_y = [0, False]  # motor y turn ON

while True:

    _, frame_zer = webcam_zer.read()  # OBSERVER

    if not (webcam_zer.read())[0]:
        break

    cv2.imshow('Prototype View', frame_zer)

    ##########################
    ###  KEYBOARD CONTROL  ###
    ##########################

    key = cv2.waitKey(1) & 0xFF

    if key == ord('a'):  # 119 Adjustment on Screen
        key_a[0] = 1 + key_a[0]
        if (key_a[0] % 2) == 0:
            key_a[1] = False
        if (key_a[0] % 2) != 0:
            key_a[1] = True
        print('a', key, key_a[0], key_a[1])

    elif key == ord('b'):  # 98 Turn ON Green Laser Pointer
        key_b[0] = 1 + key_b[0]
        if (key_b[0] % 2) == 0:
            key_b[1] = False
        if (key_b[0] % 2) != 0:
            key_b[1] = True
        print('b', key, key_b[0], key_b[1])

    elif key == ord('e'):  # 120 Activate MediaPipe
        key_e[0] = 1 + key_e[0]
        if (key_e[0] % 2) == 0:
            key_e[1] = False
        if (key_e[0] % 2) != 0:
            key_e[1] = True
        print('e', key, key_e[0], key_e[1])

    elif key == ord('g'):  # 119 Turn ON/OFF the ROI images
        key_g[0] = 1 + key_g[0]
        if (key_g[0] % 2) == 0:
            key_g[1] = False
        if (key_g[0] % 2) != 0:
            key_g[1] = True
        print('g', key, key_g[0], key_g[1])

    elif key == ord('h'):  # 104 Turn Open chanel to control motors
        key_h[0] = 1 + key_h[0]
        if (key_h[0] % 2) == 0:
            key_h[1] = False
        if (key_h[0] % 2) != 0:
            key_h[1] = True
        print('h', key, key_h[0], key_h[1])

    elif key == ord('m'):  # 109 Keyboard Mapping
        key_m[0] = 1 + key_m[0]
        if (key_m[0] % 2) == 0:
            key_m[1] = False
        if (key_m[0] % 2) != 0:
            key_m[1] = True
        print('m', key, key_m[0], key_m[1])

    elif key == ord('o'):  # 111 motors follow mouse
        key_o[0] = 1 + key_o[0]
        if (key_o[0] % 2) == 0:
            key_o[1] = False
        if (key_o[0] % 2) != 0:
            key_o[1] = True
        print('o', key, key_o[0], key_o[1])

    elif key == ord('p'):  # 112 Print Sniper View
        key_p[0] = 1 + key_p[0]
        if (key_p[0] % 2) == 0:
            key_p[1] = False
        if (key_p[0] % 2) != 0:
            key_p[1] = True
        print('p', key, key_p[0], key_p[1])

    elif key == ord('r'):  # 114 Reset the ROI
        key_r[0] = 1 + key_r[0]
        if (key_r[0] % 2) == 0:
            key_r[1] = False
        if (key_r[0] % 2) != 0:
            key_r[1] = True
        print('r', key, key_r[0], key_r[1])

    elif key == ord('x'):  # 120 Turn Open chanel to x motor
        key_x[0] = 1 + key_x[0]
        if (key_x[0] % 2) == 0:
            key_x[1] = False
        if (key_x[0] % 2) != 0:
            key_x[1] = True
        print('x', key, key_x[0], key_x[1])

    elif key == ord('y'):  # 121 Turn Open chanel to y motor
        key_y[0] = 1 + key_y[0]
        if (key_y[0] % 2) == 0:
            key_y[1] = False
        if (key_y[0] % 2) != 0:
            key_y[1] = True
        print('y', key, key_y[0], key_y[1])

    elif key == ord('q'):  # 113 Exit Program
        print('q', key, 'break')
        break
