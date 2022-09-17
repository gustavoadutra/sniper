from dynamixel_sdk import * 
import serial 

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
DXL_MINIMUM_POSITION_VALUE_X = 880
DXL_MAXIMUM_POSITION_VALUE_X = 3880
dxl_goal_position_x = 2280  # Goal position

# Y axis
DXL_MINIMUM_POSITION_VALUE_Y = 1570
DXL_MAXIMUM_POSITION_VALUE_Y = 2630
dxl_goal_position_y = 2050  # Goal position

DXL_MOVING_STATUS_THRESHOLD = 20  # (min > 3)
MAP = 1.017

# Initialize PacketHandler instance
portHandler   = None   
packetHandler = None       


# Open port
def open_port( device : str = 'COM3', protocol_version : float = 1.0):
    global portHandler, packetHandler 

    portHandler = PortHandler( DEVICE )
    packetHandler = PacketHandler( PROTOCOL_VERSION )
    
    status = portHandler.openPort()
    if status:
        print("Succeeded to open the port")
        return True
    else:
        print("Failed to open the port")
        return False     


# Set port baudrate
def set_baudrate( bauds : int = 9600 ):
    global BAUDRATE, portHandler 

    status = portHandler.setBaudRate( bauds )
    if status:
        print("Succeeded to change the baudrate")
        BAUDRATE = bauds 
        return True 
    else:
        print("Failed to change the baudrate")
        return False


#  PID Parameters
def set_PID_parameters():
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 28, 6)   # P
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 27, 0)   # I
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, 26, 10)  # D

    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 28, 6)   # P
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 27, 0)   # I
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, 26, 10)  # D



# Enable Dynamixel Torque
def enable_torque():
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, ENABLE)
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, ENABLE)

# Go to initial position
def initial_position():
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION, dxl_goal_position_x)
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION, dxl_goal_position_y)

# Disable Dynamixel Torque
def disable_torque():
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, DISABLE)
    packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, DISABLE)