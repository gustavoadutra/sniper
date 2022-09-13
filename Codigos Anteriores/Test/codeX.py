from __future__ import print_function
import cv2
from dynamixel_sdk import *
from pynput.keyboard import Controller

###################
###  VARIABLES  ###
###################

# res_types = [(480, 640), (720, 1280), (1080, 1920)]
webcam_zer = cv2.VideoCapture(2)  # CAM

key_a = [0, False]  # Adjustment on Screen/Calibrate
# key_b = [0, False]  # Turn ON Green Laser Pointer
# key_e = [0, False]  # Activate MediaPipe
# key_g = [0, False]  # Turn ON/OFF the ROI images
key_h = [0, False, True]  # Turn 'manual' Control Cameras
# key_m = [0, False]  # Keyboard Mapping
# key_p = [0, False]  # Print Sniper View
# key_q = [0, False]  # Exit Program
# key_r = [0, False]  # Reset the ROI
key_x = [0, False]  # motor x turn ON
# key_y = [0, False]  # motor y turn ON

mouseX = 0
mouseY = 0

go_motor_x = None
# go_motor_y = None

#########################
###  MX106 VARIABLES  ###
#########################

# Control table address
ADDR_MX_TORQUE_ENABLE = 24
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
DXL_ID_X = 1
# DXL_ID_Y = 2
BAUDRATE = 57600
DEVICE = 'COM3'

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# X axis
DXL_MINIMUM_POSITION_VALUE_X = 880
DXL_MAXIMUM_POSITION_VALUE_X = 3880
dxl_goal_position_x = 2280  # Goal position


DXL_MOVING_STATUS_THRESHOLD = 30  # approximation limit (min = 3)
MAP = 1.016
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


# PID
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 28, 10)  # P
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 27, 0)  # I
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 26, 6)  # D

# Enable Dynamixel Torque
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
# packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
# Go to initial position
packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position_x)
# packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, dxl_goal_position_y)


##########################
###  DEFINE LIST HERE  ###
##########################


def mouse_detection(event, mouse_x, mouse_y, tag, param):  # Mouse Parameters
    global mouseX, mouseY, go_motor_x

    if event == cv2.EVENT_RBUTTONDOWN:
        print('center x: ', center_x_zer, ' shape x: ', frame_zer.shape[1])
        print('center y: ', center_y_zer, ' shape y: ', frame_zer.shape[0])
        print('mouse x: ', mouseX)
        # print('mouse y: ', mouseY)

    if event == cv2.EVENT_LBUTTONDOWN:  # Update mouse location
        print('center x: ', center_x_zer, ' coordinate x: ', mouseX)
        print('center y: ', center_y_zer, ' coordinate y: ', mouseY)
        print('go_motor')

    if event == cv2.EVENT_LBUTTONDOWN and (key_h[1] is True) and (key_h[2] is True):  # Center Cameras
        go_motor_x = int((center_x_zer - mouseX) * MAP)
        key_x[1] = True  # X axis camera, motor Id:1

    mouseX, mouseY = mouse_x, mouse_y

####################
###  CODE START  ###
####################


while True:

    _, frame_zer = webcam_zer.read()  # OBSERVER
    # frame_zer = cv2.flip(frame_zer, 1)

    if not (webcam_zer.read())[0]:
        continue

    center_x_zer = int(frame_zer.shape[1] * 0.5)
    center_y_zer = int(frame_zer.shape[0] * 0.5)



    cv2.namedWindow('Prototype View')
    cv2.setMouseCallback('Prototype View', mouse_detection)

    ############################
    ###  KEYBOARD STATEMENT  ###
    ############################

    if key_a[1] is True:  # Adjustment on Screen
        cv2.line(frame_zer, (center_x_zer, 0), (center_x_zer, frame_zer.shape[0]), (255, 0, 255), 1)
        cv2.line(frame_zer, (0, center_y_zer), (frame_zer.shape[1], center_y_zer), (0, 255, 255), 1)

    if (key_h[1] and key_x[1]) is True:  # open x
        # Read the actual position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X,
                                                                                       ADDR_MX_PRESENT_POSITION)

        goal_x = dxl_present_position + go_motor_x  # add info about where to go.

        # limits of robot
        if goal_x > DXL_MAXIMUM_POSITION_VALUE_X:
            goal_x = DXL_MAXIMUM_POSITION_VALUE_X
        if goal_x < DXL_MINIMUM_POSITION_VALUE_X:
            goal_x = DXL_MINIMUM_POSITION_VALUE_X
        dxl_goal_position = goal_x

        # Write goal position
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION,
                                                                  dxl_goal_position)
        Controller().press('h')

        while True:
            # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X,
                                                                                           ADDR_MX_PRESENT_POSITION)
            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_X, dxl_goal_position, dxl_present_position))

            if dxl_comm_result != COMM_SUCCESS:
                print(COMM_SUCCESS)
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))

            if not abs(dxl_goal_position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                key_x[1] = False
                break


    #####################
    ###  CODE SCREEN  ###
    #####################

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

    elif key == ord('h'):  # 104 Turn Open chanel to control motors
        key_h[0] = 1 + key_h[0]
        if (key_h[0] % 2) == 0:
            key_h[1] = False
        if (key_h[0] % 2) != 0:
            key_h[1] = True
        print('h', key, key_h[0], key_h[1])

    if key == ord('q'):  # 113 Exit Program
        print('q', key, 'break')
        break

# Disable camera
webcam_zer.release()
# Close Windows
cv2.destroyAllWindows()
# Disable Dynamixel Torque
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
# packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
# Close port
portHandler.closePort()
