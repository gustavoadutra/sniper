'''

funciona na camera do spotter. liga a ROI na tecla "g".
ao clicar com mouse botão esquerdo liga TLD.
ao clicar no "r" reseta ou desliga a TLD
pode ainda rolar o botão do mouse aumentando ou diminuindo
o retângulo da ROI.

'''

from __future__ import print_function
from pynput.keyboard import Controller
import cv2  # opencv-contrib-python

###################
###  VARIABLES  ###
###################

webcam_spotter = cv2.VideoCapture(0)  # CAM

key_g = [0, False]  # Turn ON/OFF the ROI images
key_q = [0, False]  # Exit Program
key_r = [0, False]  # Reset the ROI

mouseX = 0
mouseY = 0
distance_shooter_center_x = 0
distance_shooter_center_y = 0
r_ROI_X = 30  # Range ROI
r_ROI_Y = 60  # Range ROI

BGR = [(55, 55, 55),  # DARK GRAY
       (255, 0, 0),  # BLUE
       (0, 255, 0),  # GREEN
       (0, 0, 255),  # RED
       (0, 0, 0),  # BLACK
       (255, 255, 255),  # WHITE
       (100, 130, 20),  # DARK GREEN
       (255, 0, 255),  # YELLOW
       (0, 255, 255)]  # PURPLE


##########################
###  DEFINE LIST HERE  ###
##########################


def mouse_detection(event, mouse_x, mouse_y, flag, param):  # Mouse Parameters
    global mouseX, mouseY, r_ROI_X, r_ROI_Y, bbox

    if event == cv2.EVENT_LBUTTONDOWN and (key_g[1] is True):  # Press LEFT Mouse Button - Create ROI Square
        print('L BUTTON DOWN - ROI SELECTION')
        bbox = (ret_xi, ret_yi, (r_ROI_X * 2), (r_ROI_Y * 2))  # (Xi,Yi,Width,Height)
        print( bbox )
        tracker.init(frame_spotter, bbox)
        Controller().press('g')

    if event == cv2.EVENT_MOUSEWHEEL:  # MouseWheel Grow the Square ROI
        if flag > 0:
            r_ROI_X = r_ROI_X + 3
            r_ROI_Y = r_ROI_Y + 3
        if flag < 0:
            r_ROI_X = r_ROI_X - 3
            r_ROI_Y = r_ROI_Y - 3
        print('new range: ROI X =', r_ROI_X, 'ROI Y =', r_ROI_Y)

    mouseX, mouseY = mouse_x, mouse_y
    r_ROI_X, r_ROI_Y = r_ROI_X, r_ROI_Y


####################
###  CODE START  ###
####################

tracker = cv2.legacy.TrackerTLD_create()  # Create tracker TLD
while True:

    _, frame_spotter = webcam_spotter.read()  # spotter
    frame_spotter = cv2.flip(frame_spotter, 1)
    center_x_spotter = int(frame_spotter.shape[1] * 0.5)
    center_y_spotter = int(frame_spotter.shape[0] * 0.5)

    if not (webcam_spotter.read())[0]:
        break

    cv2.namedWindow('Spotter View')
    cv2.setMouseCallback('Spotter View', mouse_detection)

    _, bbox = tracker.update(frame_spotter)
    # Draw tracked objects
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame_spotter, p1, p2, (255, 0, 0), 2, 1)

    ############################
    ###  KEYBOARD STATEMENT  ###
    ############################

    if key_g[1] is True:  # Turn ON the Selection of a ROI
        # Create a DRAW rectangle of a ROI
        ret_xi = mouseX - r_ROI_X
        ret_yi = mouseY - r_ROI_Y
        ret_xo = mouseX + r_ROI_X
        ret_yo = mouseY + r_ROI_X
        cv2.rectangle(frame_spotter, (int(ret_xi), int(ret_yi)), (int(ret_xo), int(ret_yo)), (BGR[1]), 2)

    if key_r[1] is True:  # Reset the ROI
        tracker = cv2.legacy.TrackerTLD_create()
        print('Tracker Reseted')
        Controller().press('r')

    #####################
    ###  CODE SCREEN  ###
    #####################

    cv2.imshow('Spotter View', frame_spotter)

    ##########################
    ###  KEYBOARD CONTROL  ###
    ##########################

    key = cv2.waitKey(1) & 0xFF

    if key == ord('g'):  # 119 Turn ON/OFF the ROI images
        key_g[0] = 1 + key_g[0]
        if (key_g[0] % 2) == 0:
            key_g[1] = False
        if (key_g[0] % 2) != 0:
            key_g[1] = True
        print('g', key, key_g[0], key_g[1])

    elif key == ord('r'):  # 114 Reset the ROI
        key_r[0] = 1 + key_r[0]
        if (key_r[0] % 2) == 0:
            key_r[1] = False
        if (key_r[0] % 2) != 0:
            key_r[1] = True
        print('r', key, key_r[0], key_r[1])

    if key == ord('q'):  # 113 Exit Program
        print('q', key, 'break')
        break

# Disable camera
webcam_spotter.release()
# Close Windows
cv2.destroyAllWindows()

