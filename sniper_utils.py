import cv2
import datetime
import os


def keyboard_control(key_selected):
    '''
    Alter the conditions of the keys when they are pressed
    :param key_selected: key pressed by the user
    :return:
    '''
    key_selected[0] += 1
    if (key_selected[0] % 2) == 0:
        key_selected[1] = False
    else:
        key_selected[1] = True
    print(key_selected, key_selected[0], key_selected[1])


def sniper_print(frame):
    '''
    Take a picture
    :param frame: image generated by opencv
    :return:
    '''
    print('Take picture.')
    if not os.path.exists('TargetPics'):
        os.mkdir('TargetPics')
    now = datetime.datetime.now()
    cv2.imwrite(os.getcwd()+f'/TargetPics/target{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}.jpg',
                frame)


def draw_clines():
    pass