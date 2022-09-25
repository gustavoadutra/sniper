import cv2
import datetime
import os


#Tecla A
def camera_calibrate(frame_shooter, frame_spotter):
    """
    Faz duas linhas na tela, para a calibragem das câmeras e laser;
    :param frame_shooter: Frame da câmera Shooter;
    :param frame_spotter: Frame da câmera Spotter;
    :return: Frames com as linhas feitos;
    """
    center_x_shooter = frame_shooter.shape[0] / 2
    center_y_shooter = frame_shooter.shape[1] / 2
    center_x_spotter = frame_spotter.shape[0] / 2
    center_y_spotter = frame_spotter.shape[1] / 2

    cv2.line(frame_shooter, (center_x_shooter, 0), (center_x_shooter, frame_shooter.shape[0]), (BGR[7]), 1)
    cv2.line(frame_shooter, (0, center_y_shooter), (frame_shooter.shape[1], center_y_shooter), (BGR[8]), 1)
    cv2.line(frame_spotter, (center_x_spotter, 0), (center_x_spotter, frame_spotter.shape[0]), (BGR[7]), 1)
    cv2.line(frame_spotter, (0, center_y_spotter), (frame_spotter.shape[1], center_y_spotter), (BGR[8]), 1)

    return frame_shooter, frame_spotter

# Tecla P
def sniper_print(frame):
    """
    Tira uma foto;
    :param frame: Frame que irá se tornar imagem;
    :return:
    """
    print('Take picture.')
    if not os.path.exists('TargetPics'):
        os.mkdir('TargetPics')
    now = datetime.datetime.now()
    cv2.imwrite(os.getcwd()+f'/TargetPics/target{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}.jpg',
                frame)

# Tecla L
def laser(press, portHandler):
    """
    Faz o controle do laser, precisa do portHandler do dynamixel;
    :param press: Parâmetro True ou False de clique sobre a opção;
    :return:
    """
    if press:
        portHandler.writePort('1'.encode())
    else:
        portHandler.writePort('0'.encode())






