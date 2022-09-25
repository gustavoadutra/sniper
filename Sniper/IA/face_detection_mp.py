import mediapipe as mp
from ..variables import *
import cv2

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


holistic = mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8)


def holistic_aim(frame, center_x, center_y):
    """
    Utiliza o mediapipe, faz o tratamento da imagem e desenha nela;
    * Vai mandar para onde os motores devem ir em uma implementação futura *
    :param frame: Imagem recebida pela câmera do Shooter
    :param center_x: Centro de imagem do eixo x;
    :param center_y: Centro de imagem do eixo y;
    :return: Imagem tratada.
    """

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame.flags.writeable = False
    results = holistic.process(frame)

    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    if results.pose_landmarks is not None:  # no math if no target

        # coordinates = (left eye + right eye / 2) * screen center
        x_shooter = int(
            (results.pose_landmarks.landmark[2].x + results.pose_landmarks.landmark[5].x) * center_x)
        y_shooter = int(
            (results.pose_landmarks.landmark[2].y + results.pose_landmarks.landmark[5].y) * center_y)

        distance_center_x = center_x - x_shooter
        distance_center_y = center_y - y_shooter

        cv2.line(frame, (x_shooter, y_shooter), (center_x, center_y), (BGR[3]), 4)
        cv2.putText(frame, f'x:{x_shooter} y:{y_shooter}', (x_shooter, y_shooter - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # hypotenuse

        cv2.line(frame, (x_shooter, center_y), (center_x, center_y), (BGR[2]), 4)
        cv2.putText(frame, f'{distance_center_x}', (x_shooter, center_y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # x

        cv2.line(frame, (center_x, y_shooter), (center_x, center_y), (BGR[6]), 4)
        cv2.putText(frame, f'{distance_center_y}', (center_x + 20, y_shooter + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # y

    return frame
