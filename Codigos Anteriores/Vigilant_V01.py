from __future__ import print_function
import cv2
from dynamixel_sdk import *

###################
###  VARIABLES  ###
###################

webcam_spotter = cv2.VideoCapture(1)  # CAM

key_a = [0, False]  # Adjustment on Screen/Calibrate
key_h = [0, False]  # Turn 'manual' Control Cameras
key_q = [0, False]  # Exit Program
key_x = [0, False]  # motor x turn ON
key_y = [0, False]  # motor y turn ON

mouseX = 0
mouseY = 0

go_motor_x = None
go_motor_y = None

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
DEVICE = 'COM18'

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# X axis
DXL_MINIMUM_POSITION_VALUE_X = 1260
DXL_MAXIMUM_POSITION_VALUE_X = 3260
dxl_goal_position_x = 2260  # Goal position
# Y axis
DXL_MINIMUM_POSITION_VALUE_Y = 1236
DXL_MAXIMUM_POSITION_VALUE_Y = 3284
dxl_goal_position_y = 2050  # Goal position

DXL_MOVING_STATUS_THRESHOLD = 30  # (min > 3)
MAP = 1.017

portHandler = PortHandler(DEVICE)
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

# PID X e Y
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 28, 7)  # P
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 27, 0)  # I
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 26, 200)  # D
print("define PID")
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 28, 7)  # P
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 27, 0)  # I
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 26, 200)  # D

# Enable Dynamixel Torque
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, TORQUE_ENABLE)
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, TORQUE_ENABLE)
print('define Torque')
# Go to initial position
packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position_x)
packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, dxl_goal_position_y)
print('Go to X init')

##########################
###  DEFINE LIST HERE  ###
##########################


def mouse_detection(event, mouse_x, mouse_y, tag, param):  # Mouse Parameters
    global mouseX, mouseY, go_motor_x, go_motor_y

    if event == cv2.EVENT_RBUTTONDOWN:
        print('center x: ', center_x_zer, ' shape x: ', frame_spotter.shape[1])
        print('center y: ', center_y_zer, ' shape y: ', frame_spotter.shape[0])
        print('mouse x: ', mouseX)
        print('mouse y: ', mouseY)

    if event == cv2.EVENT_LBUTTONDOWN and (key_h[1] is True):  # Center Cameras
        go_motor_x = int((mouseX - center_x_zer) * MAP)
        key_x[1] = True  # X axis camera, motor Id:1
        # go_motor_y = int((mouseY - center_y_zer) * MAP)
        # key_y[1] = True  # Y axis camera, motor Id:2

    mouseX, mouseY = mouse_x, mouse_y

####################
###  CODE START  ###
####################


while True:
    _, frame_spotter = webcam_spotter.read()  # OBSERVER
    # frame_spotter = cv2.flip(frame_spotter, 1)

    center_x_zer = int(frame_spotter.shape[1] * 0.5)
    center_y_zer = int(frame_spotter.shape[0] * 0.5)

    if not (webcam_spotter.read())[0]:
        break

    cv2.namedWindow('Spotter View')
    cv2.setMouseCallback('Spotter View', mouse_detection)

    ############################
    ###  KEYBOARD STATEMENT  ###
    ############################

    if key_a[1] is True:  # Adjustment on Screen
        cv2.line(frame_spotter, (center_x_zer, 0), (center_x_zer, frame_spotter.shape[0]), (255, 0, 255), 1)
        cv2.line(frame_spotter, (0, center_y_zer), (frame_spotter.shape[1], center_y_zer), (0, 255, 255), 1)

    if (key_h[1] and key_x[1]) is True:  # open x
        # Read the actual position
        while True:
            try: 
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_PRESENT_POSITION)
                # print( dxl_present_position, type(dxl_present_position), dxl_present_position[0], type(dxl_present_position[0]) )
                goal_x = dxl_present_position + go_motor_x  # add info about where to go.
                if goal_x != 0:
                    break
            except:
                pass 

        # limits of robot
        if goal_x > DXL_MAXIMUM_POSITION_VALUE_X:
            goal_x = DXL_MAXIMUM_POSITION_VALUE_X
        if goal_x < DXL_MINIMUM_POSITION_VALUE_X:
            goal_x = DXL_MINIMUM_POSITION_VALUE_X
        dxl_goal_position = goal_x

        # Write goal position
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position)

        # while 1:

        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X,
                                                                                        ADDR_MX_PRESENT_POSITION)
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_X, dxl_goal_position, dxl_present_position))

        if dxl_comm_result != COMM_SUCCESS:
            print(f"{packetHandler.getTxRxResult(dxl_comm_result)}, <<1")
        elif dxl_error != 0:
            print(f"{packetHandler.getRxPacketError(dxl_error)}, <<2")

            # done = abs(dxl_goal_position - dxl_present_position)
            # print(f"{done} == {dxl_goal_position} - {dxl_present_position} < {DXL_MOVING_STATUS_THRESHOLD}")

            # if abs(done) < DXL_MOVING_STATUS_THRESHOLD:
            #     print("done")
            #     key_x[1] = False
            #     break

    # if (key_h[1] and key_y[1]) is True:  # open y
    #     # Read the actual position
    #     dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_Y,
    #                                                                                    ADDR_MX_PRESENT_POSITION)

    #     goal_y = dxl_present_position + go_motor_y  # add info about where to go.

    #     # limits of robot
    #     if goal_y > DXL_MAXIMUM_POSITION_VALUE_Y:
    #         goal_y = DXL_MAXIMUM_POSITION_VALUE_Y
    #     if goal_y < DXL_MINIMUM_POSITION_VALUE_Y:
    #         goal_y = DXL_MINIMUM_POSITION_VALUE_Y
    #     dxl_goal_position = goal_y

    #     # Write goal position
    #     dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION,
    #                                                               dxl_goal_position)

    #     while 1:
    #         # Read present position
    #         dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_Y,
    #                                                                                        ADDR_MX_PRESENT_POSITION)
    #         print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_Y, dxl_goal_position, dxl_present_position))

    #         if dxl_comm_result != COMM_SUCCESS:
    #             print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    #         elif dxl_error != 0:
    #             print("%s" % packetHandler.getRxPacketError(dxl_error))

    #         if not abs(dxl_goal_position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
    #             # if key_o[1] is False:
    #             key_y[1] = False
    #             break


    #####################
    ###  CODE SCREEN  ###
    #####################

    cv2.imshow('Spotter View', frame_spotter)

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
webcam_spotter.release()
# Close Windows
cv2.destroyAllWindows()
# Disable Dynamixel Torque
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, TORQUE_DISABLE)
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, TORQUE_DISABLE)
# Close port
portHandler.closePort()