from __future__ import print_function
from dynamixel_sdk import *
from pynput.keyboard import Controller
import cv2  # opencv-contrib-python
import datetime
import os
import mediapipe as mp
import numpy as np
import serial

###################
###  VARIABLES  ###
###################

# res_types = [(480, 640), (720, 1280), (1080, 1920)]
webcam_shooter = cv2.VideoCapture(0)  # CAM
webcam_shooter.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
webcam_shooter.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
# webcam_spotter = cv2.VideoCapture(2)  # CAM
# webcam_spotter.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
# webcam_spotter.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
# openCR = serial.Serial(port="COM4", baudrate=57600)

key_a = [0, False]  # Adjustment on Screen/Calibrate
key_b = [0, False]  # Turn ON Green Laser Pointer
key_e = [0, False]  # Activate MediaPipe
key_g = [0, False]  # Turn ON/OFF the ROI images
key_h = [0, False]  # Turn 'manual' Control Cameras
key_p = [0, False]  # Print Sniper View
key_q = [0, False]  # Exit Program
key_r = [0, False]  # Reset the ROI
key_x = [0, False]  # motor x turn ON
key_y = [0, False]  # motor y turn ON

mouseX = 0
mouseY = 0
distance_shooter_center_x = 0
distance_shooter_center_y = 0
r_ROI_X = 30  # Range ROI
r_ROI_Y = 60  # Range ROI
go_motor_x = None
go_motor_y = None

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

BGR = [(55, 55, 55),  # DARK GRAY
       (255, 0, 0),  # BLUE
       (0, 255, 0),  # GREEN
       (0, 0, 255),  # RED
       (0, 0, 0),  # BLACK
       (255, 255, 255),  # WHITE
       (100, 130, 20),  # DARK GREEN
       (255, 0, 255),  # YELLOW
       (0, 255, 255)]  # PURPLE

#########################
###  MX106 VARIABLES  ###
#########################

# Control table address
ADDR_MX_TORQUE = 24
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36
# Protocol version
PROTOCOL_VERSION = 1.0
# Default setting
DXL_ID_X = 1
DXL_ID_Y = 2
BAUDRATE = 57600
DEVICE = 'COM4'
ENABLE = 1
DISABLE = 0

# X axis
DXL_MINIMUM_POSITION_VALUE_X = 1160
DXL_MAXIMUM_POSITION_VALUE_X = 3430
dxl_goal_position_x = 2280  # Goal position
# Y axis
DXL_MINIMUM_POSITION_VALUE_Y = 1570
DXL_MAXIMUM_POSITION_VALUE_Y = 2630
dxl_goal_position_y = 2050  # Goal position

DXL_MOVING_STATUS_THRESHOLD = 20  # (min > 3)
MAP = 1.017
portHandler = PortHandler(DEVICE)
# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

#  PID Parameters
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 28, 6)   # P
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 27, 0)   # I
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 26, 10)  # D
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 28, 6)   # P
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 27, 0)   # I
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 26, 10)  # D
# Enable Dynamixel Torque
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, ENABLE)
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, ENABLE)
# Go to initial position
packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position_x)
packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, dxl_goal_position_y)


##########################
###  DEFINE LIST HERE  ###
##########################


def mouse_detection(event, mouse_x, mouse_y, flag, param):  # Mouse Parameters
    global mouseX, mouseY, r_ROI_X, r_ROI_Y, go_motor_x, go_motor_y, bbox

    if event == cv2.EVENT_RBUTTONDOWN:
        print('R BUTTON DOWN', param)
        # print('center x: ', center_x_spotter, ' shape x: ', frame_spotter.shape[1])
        # print('center y: ', center_y_spotter, ' shape y: ', frame_spotter.shape[0])
        # print('mouse x: ', mouseX)
        # print('mouse y: ', mouseY)

    if event == cv2.EVENT_LBUTTONDOWN and (key_g[1] is True):  # Press LEFT Mouse Button - Create ROI Square
        print('L BUTTON DOWN - ROI SELECTION')
        # bbox = (ret_xi, ret_yi, (r_ROI_X * 2), (r_ROI_Y * 2))  # (Xi,Yi,Width,Height)
        # tracker.init(frame_spotter, bbox)
        # print('Tracker initializing{}'.format(bbox))
        Controller().press('g')

    if event == cv2.EVENT_LBUTTONDOWN and (key_h[1] is True):  # Center Cameras
        go_motor_x = int((mouseX - center_x_shooter) * MAP)  # With 2 Cams CHANGE TO center_x_spotter
        go_motor_y = int((mouseY - center_y_shooter) * MAP)  # With 2 Cams CHANGE TO center_y_spotter
        key_x[1] = True  # X axis camera, motor Id:1
        key_y[1] = True  # Y axis camera, motor Id:2

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


def holistic_aim(frame_shooter_def):  # MediaPipe in the Sniper View
    global distance_shooter_center_x, distance_shooter_center_y

    image_shooter = cv2.cvtColor(frame_shooter_def, cv2.COLOR_BGR2RGB)
    image_shooter.flags.writeable = False
    results = holistic.process(image_shooter)
    image_shooter.flags.writeable = True
    image_shooter = cv2.cvtColor(image_shooter, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(image_shooter, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # mp_holistic.POSE_CONNECTIONS <= lines/connections
    # landmark_drawing_spec <= pointers

    if results.pose_landmarks is not None:  # no math if no target

        # coordinates = (left eye + right eye / 2) * screen center
        x_shooter = int(
            (results.pose_landmarks.landmark[2].x + results.pose_landmarks.landmark[5].x) * center_x_shooter)
        y_shooter = int(
            (results.pose_landmarks.landmark[2].y + results.pose_landmarks.landmark[5].y) * center_y_shooter)

        distance_shooter_center_x = center_x_shooter - x_shooter
        distance_shooter_center_y = center_y_shooter - y_shooter

        cv2.line(image_shooter, (x_shooter, y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 4)
        cv2.putText(image_shooter, f'x:{x_shooter} y:{y_shooter}', (x_shooter, y_shooter - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # hypotenuse

        cv2.line(image_shooter, (x_shooter, center_y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 2)
        cv2.putText(image_shooter, f'{distance_shooter_center_x}', (x_shooter, center_y_shooter + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # x

        cv2.line(image_shooter, (center_x_shooter, y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 4)
        cv2.putText(image_shooter, f'{distance_shooter_center_y}', (center_x_shooter + 20, y_shooter + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # y

        aim_sq = 50
        if distance_shooter_center_x in range(-aim_sq, aim_sq) and distance_shooter_center_y in range(-aim_sq, aim_sq):
            print('target on')

    return image_shooter


####################
###  CODE START  ###
####################

#  tracker = cv2.legacy.TrackerTLD_create()  # Create tracker TLD
with mp_holistic.Holistic(min_detection_confidence=0.6, min_tracking_confidence=0.6) as holistic:
    while True:

        _, frame_shooter = webcam_shooter.read()  # shooter
        #  _, frame_spotter = webcam_spotter.read()  # spotter
        frame_shooter = cv2.flip(frame_shooter, 1)
        # frame_spotter = cv2.flip(frame_spotter, 1)
        center_x_shooter = int(frame_shooter.shape[1] * 0.5)
        center_y_shooter = int(frame_shooter.shape[0] * 0.5)
        # center_x_spotter = int(frame_spotter.shape[1] * 0.5)
        # center_y_spotter = int(frame_spotter.shape[0] * 0.5)

        if not (webcam_shooter.read())[0]:  # or not (webcam_spotter.read())[0]:
            break

        cv2.namedWindow('Shooter View')
        cv2.setMouseCallback('Shooter View', mouse_detection)
        # cv2.namedWindow('Spotter View')
        # cv2.setMouseCallback('Spotter View', mouse_detection)

        # get updated location of objects in subsequent frames
        # _, bbox = tracker.update(frame_spotter)
        # Draw tracked objects
        # p1 = (int(bbox[0]), int(bbox[1]))
        # p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        # cv2.rectangle(frame_spotter, p1, p2, (255, 0, 0), 2, 1)

        ############################
        ###  KEYBOARD STATEMENT  ###
        ############################

        if key_a[1] is True:  # Adjustment on Screen
            cv2.line(frame_shooter, (center_x_shooter, 0), (center_x_shooter, frame_shooter.shape[0]), (BGR[7]), 1)
            cv2.line(frame_shooter, (0, center_y_shooter), (frame_shooter.shape[1], center_y_shooter), (BGR[8]), 1)
            # cv2.line(frame_spotter, (center_x_spotter, 0), (center_x_spotter, frame_spotter.shape[0]), (BGR[7]), 1)
            # cv2.line(frame_spotter, (0, center_y_spotter), (frame_spotter.shape[1], center_y_spotter), (BGR[8]), 1)

        if key_b[1] is True:  # Turn ON the Selection of a ROI
            # openCR.write(b'a')
            print('Enable Green Laser Pointer')

        if key_e[1] is True:  # Activate MediaPipe
            frame_shooter = holistic_aim(frame_shooter)
            # Read the actual position
            go_motor_x = int(-distance_shooter_center_x)
            go_motor_y = int(distance_shooter_center_y)
            key_x[1] = True  # X axis camera, motor Id:1
            key_y[1] = True  # Y axis camera, motor Id:2

        if key_g[1] is True:  # Turn ON the Selection of a ROI
            print('g pressed')
            # Create a DRAW rectangle of a ROI
            # ret_xi = mouseX - r_ROI_X
            # ret_yi = mouseY - r_ROI_Y
            # ret_xo = mouseX + r_ROI_X
            # ret_yo = mouseY + r_ROI_X
            # cv2.rectangle(frame_spotter, (int(ret_xi), int(ret_yi)), (int(ret_xo), int(ret_yo)), (BGR[1]), 2)

        if (key_h[1] and key_x[1]) is True:  # open x
            # Read the actual position
            dxl_present_position_x, dxl_comm_result_x, dxl_error_x = packetHandler.read2ByteTxRx(portHandler,
                                                                                    DXL_ID_X, ADDR_MX_PRESENT_POSITION)

            goal_x = dxl_present_position_x + go_motor_x  # add info about where to go.

            # limits of robot
            if goal_x > DXL_MAXIMUM_POSITION_VALUE_X:
                goal_x = DXL_MAXIMUM_POSITION_VALUE_X
            if goal_x < DXL_MINIMUM_POSITION_VALUE_X:
                goal_x = DXL_MINIMUM_POSITION_VALUE_X
            dxl_goal_position_x = goal_x

            # Write goal position
            packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position_x)

            while 1:
                # Read present position
                dxl_present_position_x, dxl_comm_result_x, dxl_error_x = packetHandler.read2ByteTxRx(portHandler,
                                                                                                     DXL_ID_X,
                                                                                                     ADDR_MX_PRESENT_POSITION)
                # print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_X, dxl_goal_position_x, dxl_present_position_x))

                if dxl_comm_result_x != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_x))
                elif dxl_error_x != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error_x))

                if not abs(dxl_goal_position_x - dxl_present_position_x) > DXL_MOVING_STATUS_THRESHOLD:
                    key_x[1] = False
                    break

        if (key_h[1] and key_y[1]) is True:  # open y
            # Read the actual position
            dxl_present_position_y, dxl_comm_result_y, dxl_error_y = packetHandler.read2ByteTxRx(portHandler, DXL_ID_Y,
                                                                                    ADDR_MX_PRESENT_POSITION)

            goal_y = dxl_present_position_y + go_motor_y  # add info about where to go.

            # limits of robot
            if goal_y > DXL_MAXIMUM_POSITION_VALUE_Y:
                goal_y = DXL_MAXIMUM_POSITION_VALUE_Y
            if goal_y < DXL_MINIMUM_POSITION_VALUE_Y:
                goal_y = DXL_MINIMUM_POSITION_VALUE_Y
            dxl_goal_position_y = goal_y

            # Write goal position
            packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, dxl_goal_position_y)

            while 1:
                # Read present position
                dxl_present_position_y, dxl_comm_result_y, dxl_error_y = packetHandler.read2ByteTxRx(portHandler,
                                                                                                     DXL_ID_Y,
                                                                                                     ADDR_MX_PRESENT_POSITION)
                # print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_Y, dxl_goal_position_y, dxl_present_position_y))

                if dxl_comm_result_y != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_y))
                elif dxl_error_y != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error_y))

                if not abs(dxl_goal_position_y - dxl_present_position_y) > DXL_MOVING_STATUS_THRESHOLD:
                    key_y[1] = False
                    break

        if key_p[1] is True:  # Print Sniper View
            now = datetime.datetime.now()
            cv2.imwrite((os.path.join('guest', 'target{}{}{}{}.jpg'.format(now.day, now.hour, now.minute, now.second))),
                        frame_shooter[0:frame_shooter.shape[1], 0:frame_shooter.shape[0]])
            print('saved')
            Controller().press('p')

        if key_r[1] is True:  # Reset the ROI
            # tracker = cv2.legacy.TrackerTLD_create()
            print('Tracker Reseted')
            Controller().press('r')

        #####################
        ###  CODE SCREEN  ###
        #####################

        cv2.imshow('Shooter View', frame_shooter)
        # cv2.imshow('Spotter View', frame_spotter)

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
                # openCR.write(b'c')
                print('Disable Green Laser Pointer')
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

        if key == ord('q'):  # 113 Exit Program
            print('q', key, 'break')
            break

# Disable camera
webcam_shooter.release()
# Close Windows
cv2.destroyAllWindows()
# Disable Dynamixel Torque
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, DISABLE)
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, DISABLE)
# Close port
portHandler.closePort()
