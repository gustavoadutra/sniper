import  dearpygui.dearpygui as dpg
import  mediapipe as mp
import os 

# VARIÁVEIS GLOBAIS 
distance_shooter_center_x = 0
distance_shooter_center_y = 0

packetHandler   = 0.0
portHandler     = 0.0 

go_motor_x = None
go_motor_y = None

r_ROI_X = 30
r_ROI_Y = 60

mouseX = 0
mouseY = 0


# OBJETOS 
mp_face_detection   = mp.solutions.face_detection
mp_drawing          = mp.solutions.drawing_utils
mp_drawing_styles   = mp.solutions.drawing_styles
mp_holistic         = mp.solutions.holistic
# openCR              = serial.Serial(port="COM4", baudrate=57600)

