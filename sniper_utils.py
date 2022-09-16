import cv2
import datetime
import os
from dynamixel_sdk import *


# VARIABLES MOTORS MX106

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
DEVICE = 'COM3'
ENABLE = 1
DISABLE = 0

# X axis
DXL_MINIMUM_POSITION_VALUE_X = 1160
DXL_MAXIMUM_POSITION_VALUE_X = 3430
dxl_goal_position_x = 2280  # Goal position
# Y axis
DXL_MINIMUM_POSITION_VALUE_Y = 2191
DXL_MAXIMUM_POSITION_VALUE_Y = 2943
dxl_goal_position_y = 2612  # Goal position

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
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 28, 10)   # P
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 27, 0)   # I
packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 26, 6)  # D
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 28, 10)   # P
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 27, 0)   # I
packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 26, 6)  # D


def keyboard_control(key_selected):
    key_selected[0] += 1
    if (key_selected[0] % 2) == 0:
        key_selected[1] = False
    else:
        key_selected[1] = True
    print(key_selected, key_selected[0], key_selected[1])


def sniper_print(frame):
    print('Take picture.')
    if not os.path.exists('TargetPics'):
        os.mkdir('TargetPics')
    now = datetime.datetime.now()
    cv2.imwrite(os.getcwd()+f'/TargetPics/target{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}.jpg',
                frame)


def laser(key):
    if key:
        portHandler.writePort('1'.encode())
    else:
        portHandler.writePort('0'.encode())


def go_motor(go_motor_x, go_motor_y):
    # Actual position

    if verify_goal(go_motor_x, DXL_MAXIMUM_POSITION_VALUE_X, DXL_MINIMUM_POSITION_VALUE_Y) and verify_goal(
            go_motor_y, DXL_MAXIMUM_POSITION_VALUE_Y, DXL_MINIMUM_POSITION_VALUE_Y):
        print('Position verified')
        packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, go_motor_x)
        packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, go_motor_y)
        while True:
            if verify_position(go_motor_x, 'x') and verify_position(go_motor_y, 'y'):
                break


def verify_goal(goal_pos, goal_max, goal_min):
    # Verify if goal is possible
    # To not break components of the robot
    if goal_min > goal_pos > goal_max:
        print('Wrong position')
        return False
    return True


def verify_position(dxl_goal_position, var):
    # Read present position X or Y
    # Checks if the robot has reached its destination
    if var == 'x':
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X,
                                                                                       ADDR_MX_PRESENT_POSITION)
    else:
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_Y,
                                                                                       ADDR_MX_PRESENT_POSITION)

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    if abs(dxl_goal_position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
        return True


def initiate_motors():
    # Enable Dynamixel Torque
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, ENABLE)
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, ENABLE)
    print("Indo para posição inicial.")

    go_motor(dxl_goal_position_x, dxl_goal_position_y)


def finish_motors():
    print("Finishing motors")
    go_motor(dxl_goal_position_x, DXL_MINIMUM_POSITION_VALUE_Y)
    time.sleep(0.8)
    # Disable Dynamixel Torque
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, DISABLE)
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, DISABLE)
    # Close port
    portHandler.closePort()


