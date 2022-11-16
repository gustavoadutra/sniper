from Interface import dpg_context as interface
from dynamixel_sdk import *

import dearpygui.dearpygui as dpg
import cv2

# REGISTRADORES DPG 
DEVICE = dpg.add_string_value(default_value='COM18', parent=interface.values_registry)
GO_MOTOR_X = dpg.add_float_value(default_value=0, parent=interface.values_registry)
GO_MOTOR_Y = dpg.add_float_value(default_value=0, parent=interface.values_registry)

SERIAL_OK = dpg.add_bool_value(default_value=False, parent=interface.values_registry)

KEY_A = dpg.add_bool_value(default_value=False, parent=interface.values_registry)
KEY_H = dpg.add_bool_value(default_value=False, parent=interface.values_registry)

KEY_X = dpg.add_bool_value(default_value=False, parent=interface.values_registry)
KEY_Y = dpg.add_bool_value(default_value=False, parent=interface.values_registry)

KEY_L = dpg.add_bool_value(default_value=False, parent=interface.values_registry)

# Control table address
ADDR_MX_PRESENT_POSITION = 36
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_TORQUE = 24

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
DXL_ID_X = 1
DXL_ID_Y = 2
BAUDRATE = 57600

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

portHandler = PortHandler(dpg.get_value(DEVICE))
packetHandler = PacketHandler(PROTOCOL_VERSION)


# Adjustment on Screen/Calibrate
def KEY_A_callback(sender, data, user):
    dpg.set_value(KEY_A, not dpg.get_value(KEY_A))
    interface.print_callback('Calibrate: ' + str(dpg.get_value(KEY_A)))


# Turn 'manual' Control Cameras
def KEY_H_callback(sender, data, user):
    dpg.set_value(KEY_H, not dpg.get_value(KEY_H))
    interface.print_callback('Key H: ' + str(dpg.get_value(KEY_H)))


# Turn on the laser point
def KEY_L_callback(sender, data, user):
    dpg.set_value(KEY_L, not dpg.get_value(KEY_L))
    interface.print_callback('Laser point: ' + str(dpg.get_value(KEY_L)))


# Aplica os callbacks 
dpg.configure_item('key_A', callback=KEY_A_callback)
dpg.configure_item('key_H', callback=KEY_H_callback)
dpg.configure_item('key_L', callback=KEY_L_callback)


# PID X e Y
def set_motors_PID():
    global packetHandler, portHandler

    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 28, 7)  # P
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 27, 0)  # I
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 26, 200)  # D
    # print("define PID")

    # packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 28, 7)      # P
    # packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 27, 0)      # I
    # packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 26, 200)    # D

    # Enable Dynamixel Torque
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, TORQUE_ENABLE)
    # packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, TORQUE_ENABLE)
    # print('define Torque')

    # Go to initial position
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position_x)
    # packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, dxl_goal_position_y)
    # print('Go to X init')


# Open port
def open_port():
    global portHandler

    if portHandler.openPort():
        interface.print_callback("Succeeded to open the port")
        if portHandler.setBaudRate(BAUDRATE):
            interface.print_callback("Succeeded to change the baudrate")
            return True
        else:
            interface.print_callback("Failed to change the baudrate")
            return False
    else:
        interface.print_callback("Failed to open the port")
        return False

    # Apenas inicia a comunicação Serial


def init_serial():
    if open_port():
        set_motors_PID()
        dpg.set_value(SERIAL_OK, True)
    else:
        dpg.set_value(SERIAL_OK, False)


# Colocar o go_motor_x dentro do registry do dpg 
# Colocar o go_motor_y dentro do registry do dpg 


# Roda no loop principal do código 
def run_serial():
    # Liga o Laser
    if dpg.get_value(KEY_L):
        portHandler.writePort('1'.encode())
    else:
        portHandler.writePort('0'.encode())

    if dpg.get_value(KEY_H) and dpg.get_value(KEY_X):
        while True:
            try:
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X,
                                                                                               ADDR_MX_PRESENT_POSITION)
                goal_x = dxl_present_position + dpg.get_value(GO_MOTOR_X)  # add info about where to go.
                break
            except:
                pass

                # limits of robot
        if goal_x > DXL_MAXIMUM_POSITION_VALUE_X:   goal_x = DXL_MAXIMUM_POSITION_VALUE_X
        if goal_x < DXL_MINIMUM_POSITION_VALUE_X:   goal_x = DXL_MINIMUM_POSITION_VALUE_X
        dxl_goal_position = goal_x

        # Write goal position
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION,
                                                                  dxl_goal_position)

        while True:
            # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X,
                                                                                           ADDR_MX_PRESENT_POSITION)
            interface.print_callback(
                "[ID:%03d] GoalPos:%03d  \nPresPos:%03d" % (DXL_ID_X, dxl_goal_position, dxl_present_position))

            if dxl_comm_result != COMM_SUCCESS:
                interface.print_callback(f"{packetHandler.getTxRxResult(dxl_comm_result)}, <<1")
            elif dxl_error != 0:
                interface.print_callback(f"{packetHandler.getRxPacketError(dxl_error)}, <<2")

            done = abs(dxl_goal_position - dxl_present_position)
            interface.print_callback(
                f"{done} == {dxl_goal_position} - {dxl_present_position} < {DXL_MOVING_STATUS_THRESHOLD}")

            if abs(done) < DXL_MOVING_STATUS_THRESHOLD:
                dpg.set_value(KEY_X, False)
                break

    if dpg.get_value(KEY_H) and dpg.get_value(KEY_Y):
        # Read the actual position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_Y,
                                                                                       ADDR_MX_PRESENT_POSITION)
        goal_y = dxl_present_position + dpg.get_value(GO_MOTOR_Y)  # add info about where to go.

        # limits of robot
        if goal_y > DXL_MAXIMUM_POSITION_VALUE_Y:   goal_y = DXL_MAXIMUM_POSITION_VALUE_Y
        if goal_y < DXL_MINIMUM_POSITION_VALUE_Y:   goal_y = DXL_MINIMUM_POSITION_VALUE_Y
        dxl_goal_position = goal_y

        # Write goal position
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION,
                                                                  dxl_goal_position)

        while True:
            # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_Y,
                                                                                           ADDR_MX_PRESENT_POSITION)
            interface.print_callback(
                "[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_Y, dxl_goal_position, dxl_present_position))

            if dxl_comm_result != COMM_SUCCESS:
                interface.print_callback("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                interface.print_callback("%s" % packetHandler.getRxPacketError(dxl_error))

            if not abs(dxl_goal_position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                dpg.set_value(KEY_Y, False)
                break
