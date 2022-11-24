from Interface import dpg_context as interface 
from dynamixel_sdk import *

import dearpygui.dearpygui as dpg 

# Control table address
ADDR_MX_PRESENT_POSITION = 36
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_TORQUE = 24

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
DXL_ID_X = 1
DXL_ID_Y = 2

TORQUE_ENABLE  = 1
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


# REGISTRADORES DPG 
DEVICE     = dpg.add_string_value( tag = 'DEVICE'   , default_value = 'COM3', parent = interface.values_registry )
BAUDRATE   = dpg.add_int_value   ( tag = 'BAUDRATE' , default_value = 57600 , parent = interface.values_registry )
SERIAL_OK = dpg.add_bool_value   ( tag = 'SERIAL_OK', default_value = False , parent = interface.values_registry )

GO_MOTOR_X = dpg.add_float_value( tag = 'GO_MOTOR_X', default_value = 0, parent = interface.values_registry )
GO_MOTOR_Y = dpg.add_float_value( tag = 'GO_MOTOR_Y', default_value = 0, parent = interface.values_registry )

KEY_H = dpg.add_bool_value( default_value = False, parent = interface.values_registry )
KEY_L = dpg.add_bool_value( default_value = False, parent = interface.values_registry )

KEY_X = dpg.add_bool_value( default_value = False, parent = interface.values_registry )
KEY_Y = dpg.add_bool_value( default_value = False, parent = interface.values_registry )


# FUNÇÕES DO DxlCom
portHandler = PortHandler( dpg.get_value( DEVICE ) ) 
packetHandler = PacketHandler(PROTOCOL_VERSION)


"""
Tecla L - Faz o controle do laser, precisa do portHandler do dynamixel;
:param press: Parâmetro True ou False de clique sobre a opção;
:return: None 
"""
def KEY_L_callback (sender, data, user): 
    dpg.set_value( KEY_L, not dpg.get_value( KEY_L ))
    interface.print_callback( 'Laser point: ' + str(dpg.get_value(KEY_L)) )

# Serial control 
def KEY_Y_callback( sender, data, user ): 
    if dpg.get_value( SERIAL_OK ):
        portHandler.closePort()
        dpg.set_value( SERIAL_OK, False)
    else: 
        init_serial() 

def KEY_H_callback (sender, data, user): 
    dpg.set_value( KEY_H, not dpg.get_value( KEY_H ))
    interface.print_callback( 'Motor: ' + ("Enable" if dpg.get_value(KEY_H) else "Disable" )  )


# Aplica os callbacks 
dpg.configure_item( 'key_Y', callback = KEY_Y_callback  )
dpg.configure_item( 'key_L', callback = KEY_L_callback  )
dpg.configure_item( 'key_H', callback = KEY_H_callback  )
dpg.configure_item( 'but_H', callback = KEY_H_callback  )


# PID X e Y
def set_motors_PID():
    global packetHandler, portHandler 
    # print("define X PID")
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 28, 7)      # P
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 27, 0)      # I
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 26, 200)    # D
    # print("define Y PID")
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 28, 7)      # P
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 27, 0)      # I
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 26, 200)    # D
    # Enable Dynamixel Torque
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, TORQUE_ENABLE)
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, TORQUE_ENABLE)
    # Go to initial position
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position_x)
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, dxl_goal_position_y)


# Open port
def open_port(): 
    global portHandler, packetHandler
    portHandler = PortHandler( dpg.get_value( DEVICE ) ) 
    packetHandler = PacketHandler(PROTOCOL_VERSION)
    if portHandler.openPort():
        interface.print_callback("Succeeded to open the port")
        if portHandler.setBaudRate( dpg.get_value(BAUDRATE) ):
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
    try:
        if open_port():
            set_motors_PID() 
            dpg.set_value( SERIAL_OK, True )           
        else: 
            dpg.set_value( SERIAL_OK, False )
            interface.print_callback( 'Serial not OK')
        
    except:
        dpg.set_value( SERIAL_OK, False )
        interface.print_callback( 'Serial not OK')

# Colocar o go_motor_x dentro do registry do dpg 
# Colocar o go_motor_y dentro do registry do dpg 

# Roda no loop principal do código 
def run_serial(): 

    # Liga o Laser
    if dpg.get_value( KEY_L ):
        portHandler.writePort('1'.encode())
        dpg.bind_item_theme( 'but_L', theme = interface.on_button )
    else:
        portHandler.writePort('0'.encode())
        dpg.bind_item_theme( 'but_L', theme = interface.def_button )

    # Motores habilitados 
    if dpg.get_value( KEY_H ):
        dpg.bind_item_theme( 'but_H', theme = interface.on_button )
    else: 
        dpg.bind_item_theme( 'but_H', theme = interface.def_button )


    # Move os motores para a posição desejada
    if dpg.get_value(KEY_H) and dpg.get_value( SERIAL_OK ) and dpg.get_value( 'AUX_E' ):
        try:             
            '''MOTOR X'''
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_PRESENT_POSITION)
            goal_x = dxl_present_position + dpg.get_value( GO_MOTOR_X )  # add info about where to go.
            # limits of robot
            if goal_x > DXL_MAXIMUM_POSITION_VALUE_X:   goal_x = DXL_MAXIMUM_POSITION_VALUE_X
            if goal_x < DXL_MINIMUM_POSITION_VALUE_X:   goal_x = DXL_MINIMUM_POSITION_VALUE_X
            dxl_goal_position = goal_x
            # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_PRESENT_POSITION)
            interface.print_callback( "[ID:%03d] GoalPos:%03d  \nPresPos:%03d" % (DXL_ID_X, dxl_goal_position, dxl_present_position) )
            if dxl_comm_result != COMM_SUCCESS: interface.print_callback(f"{packetHandler.getTxRxResult(dxl_comm_result)}, <<1")
            elif dxl_error != 0:                interface.print_callback(f"{packetHandler.getRxPacketError(dxl_error)}, <<2")
            done = abs(dxl_goal_position - dxl_present_position)
            interface.print_callback( f"{done} == {dxl_goal_position} - {dxl_present_position} < {DXL_MOVING_STATUS_THRESHOLD}")
            # Write goal position
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position)
        except:
            pass

        '''MOTOR Y'''
        try:
            # Read the actual position
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_PRESENT_POSITION)
            goal_y = dxl_present_position + dpg.get_value( GO_MOTOR_Y )  # add info about where to go.
            # limits of robot
            if goal_y > DXL_MAXIMUM_POSITION_VALUE_Y:   goal_y = DXL_MAXIMUM_POSITION_VALUE_Y
            if goal_y < DXL_MINIMUM_POSITION_VALUE_Y:   goal_y = DXL_MINIMUM_POSITION_VALUE_Y
            dxl_goal_position = goal_y
            # Write goal position
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, dxl_goal_position )
            # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_PRESENT_POSITION)
            interface.print_callback("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_Y, dxl_goal_position, dxl_present_position))
            if dxl_comm_result != COMM_SUCCESS: interface.print_callback("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:                interface.print_callback("%s" % packetHandler.getRxPacketError(dxl_error))
        except:
            pass 