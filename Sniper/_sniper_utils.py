from Interface import dpg_context as interface 
from Interface import variables 
from Capture import capture as cap 

import  dearpygui.dearpygui as dpg  
import datetime
import cv2
import os

PATH = os.path.dirname( __file__) 

# Callback do Botão Direito 
def r_mouse_detection( sender, data, user ):
    mouse_x, mouse_y = dpg.get_mouse_pos()

# Callback do Botão Esquerdo 
def l_mouse_detection( sender, data, user ):
    mouse_x, mouse_y = dpg.get_mouse_pos()


# Tecla A
def camera_calibrate(sender, data, user ):
    frame_shooter, frame_spotter = user 
    """
    Faz duas linhas na tela, para a calibragem das câmeras e laser;
    :param frame_shooter: Frame da câmera Shooter;
    :param frame_spotter: Frame da câmera Spotter;
    :return: Frames com as linhas feitos;

    """

    center_x_spotter = frame_spotter.shape[0] / 2
    center_y_spotter = frame_spotter.shape[1] / 2
    cv2.line( frame_spotter, (center_x_spotter, 0), (center_x_spotter, frame_spotter.shape[0]), ( variables.BGR[7]), 1 )
    cv2.line( frame_spotter, (0, center_y_spotter), (frame_spotter.shape[1], center_y_spotter), ( variables.BGR[8]), 1 )

    return frame_shooter, frame_spotter


"""
Tecla P - Tira uma foto;
:param frame: Frame que irá se tornar imagem;
:return: None 
"""
def sniper_print( sender, data, frame ) ->  None:
    interface.print_callback( 'Taking picture.')
    if not os.path.exists('TargetPics'):
        os.mkdir('TargetPics')
    now = datetime.datetime.now()
    cv2.imwrite( PATH + '/TargetPics/target{}{}{}{}{}{}.jpg'.format(now.year, now.month, now.day, now.hour, now.minute, now.second), frame )


"""
Tecla L - Faz o controle do laser, precisa do portHandler do dynamixel;
:param press: Parâmetro True ou False de clique sobre a opção;
:return: None 
"""
def laser( sender, data, portHandler) -> None :
    if dpg.get_value( KEY_P ):
        portHandler.writePort('1'.encode())
    else:
        portHandler.writePort('0'.encode())