'''
Na câmera do Shooter quando o operador clicar na tecla "e" a
google mediapipe passa a funcionar. Ao apertar "e" novamente
ela para de funcionar.

A IA irá medir a distância entre o centro dos olhos com o
centro da camera entregando valores de x e y.

'''

from __future__ import print_function
import cv2  # opencv-contrib-python
import mediapipe as mp

###################
###  VARIABLES  ###
###################

# res_types = [(480, 640), (720, 1280), (1080, 1920)]
webcam_shooter = cv2.VideoCapture(0)  # CAM

key_e = [0, False]  # Activate MediaPipe
key_q = [0, False]  # Exit Program

distance_shooter_center_x = 0
distance_shooter_center_y = 0

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

BGR = [(55, 55, 55),  # DARK GRAY
       (255, 0, 0),  # BLUE
       (0, 255, 0),  # GREEN
       (0, 0, 255),  # RED
       (0, 0, 0),  # BLACK
       (255, 255, 255),  # WHITE
       (100, 130, 20),  # DARK GREEN
       (255, 0, 255),  # YELLOW
       (0, 255, 255)]  # PURPLE


##########################
###  DEFINE LIST HERE  ###
##########################

def holistic_aim(frame_shooter_def):  # MediaPipe in the Sniper View
    global distance_shooter_center_x, distance_shooter_center_y

    image_shooter = cv2.cvtColor(frame_shooter_def, cv2.COLOR_BGR2RGB)
    image_shooter.flags.writeable = False
    results = holistic.process(image_shooter)
    image_shooter.flags.writeable = True
    image_shooter = cv2.cvtColor(image_shooter, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(image_shooter, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # mp_holistic.POSE_CONNECTIONS <= lines/connections
    # landmark_drawing_spec <= pointers

    if results.pose_landmarks is not None:  # no math if no target

        # coordinates = (left eye + right eye / 2) * screen center
        x_shooter = int(
            (results.pose_landmarks.landmark[2].x + results.pose_landmarks.landmark[5].x) * center_x_shooter)
        y_shooter = int(
            (results.pose_landmarks.landmark[2].y + results.pose_landmarks.landmark[5].y) * center_y_shooter)

        distance_shooter_center_x = center_x_shooter - x_shooter
        distance_shooter_center_y = center_y_shooter - y_shooter

        cv2.line(image_shooter, (x_shooter, y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 4)
        cv2.putText(image_shooter, f'x:{x_shooter} y:{y_shooter}', (x_shooter, y_shooter - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # hypotenuse

        cv2.line(image_shooter, (x_shooter, center_y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 2)
        cv2.putText(image_shooter, f'{distance_shooter_center_x}', (x_shooter, center_y_shooter + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # x

        cv2.line(image_shooter, (center_x_shooter, y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 4)
        cv2.putText(image_shooter, f'{distance_shooter_center_y}', (center_x_shooter + 20, y_shooter + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # y

        aim_sq = 50
        if distance_shooter_center_x in range(-aim_sq, aim_sq) and distance_shooter_center_y in range(-aim_sq, aim_sq):
            print('target on')

    return image_shooter

####################
###  CODE START  ###
####################


with mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8) as holistic:
    while True:

        _, frame_shooter = webcam_shooter.read()  # shooter
        frame_shooter = cv2.flip(frame_shooter, 1)
        center_x_shooter = int(frame_shooter.shape[1] * 0.5)
        center_y_shooter = int(frame_shooter.shape[0] * 0.5)

        if not (webcam_shooter.read())[0]:
            break

        cv2.namedWindow('Shooter View')

        ############################
        ###  KEYBOARD STATEMENT  ###
        ############################

        if key_e[1] is True:  # Activate MediaPipe
            frame_shooter = holistic_aim(frame_shooter)

        #####################
        ###  CODE SCREEN  ###
        #####################

        cv2.imshow('Shooter View', frame_shooter)

        ##########################
        ###  KEYBOARD CONTROL  ###
        ##########################

        key = cv2.waitKey(1) & 0xFF

        if key == ord('e'):  # 120 Activate MediaPipe
            key_e[0] = 1 + key_e[0]
            if (key_e[0] % 2) == 0:
                key_e[1] = False
            if (key_e[0] % 2) != 0:
                key_e[1] = True
            print('e', key, key_e[0], key_e[1])

        if key == ord('q'):  # 113 Exit Program
            print('q', key, 'break')
            break

# Disable camera & Close Window
webcam_shooter.release()
cv2.destroyAllWindows()
