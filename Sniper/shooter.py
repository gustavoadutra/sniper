from Interface  import dpg_context  as interface
from Capture    import capture      as cap 

import dearpygui.dearpygui as dpg 
import mediapipe as mp
import datetime
import cv2 
import os 

PATH = os.path.dirname( __file__ )


BGR = [(55, 55, 55),        # DARK GRAY
       (255, 0, 0),         # BLUE
       (0, 255, 0),         # GREEN
       (0, 0, 255),         # RED
       (0, 0, 0),           # BLACK
       (255, 255, 255),     # WHITE
       (100, 130, 20),      # DARK GREEN
       (255, 0, 255),       # YELLOW
       (0, 255, 255)]       # PURPLE

distance_shooter_center_x = 0
distance_shooter_center_y = 0

# Media pipe macrodefinições 
mp_drawing          = mp.solutions.drawing_utils
mp_drawing_styles   = mp.solutions.drawing_styles
mp_holistic         = mp.solutions.holistic

# Valores de texturas 
img_shooter = cap.img_shooter 
Shooter     = cap.Shooter 


# Registradores de controle 
SHOOTER_OK  = dpg.add_bool_value( default_value = False, parent = interface.values_registry )
SHOOTER_ID  = dpg.add_int_value ( default_value = 0    , parent = interface.values_registry ) 

KEY_E       = dpg.add_bool_value( default_value = False, parent = interface.values_registry )
KEY_P       = dpg.add_bool_value( default_value = False, parent = interface.values_registry )

# Turn ON the Selection of a ROI
def KEY_E_callback (sender, data, user): 
    dpg.set_value( KEY_E, not dpg.get_value( KEY_E ))
    interface.print_callback( str(dpg.get_value(KEY_E)) )
# Take a picture of target 
def KEY_P_callback (sender, data, user): 
    dpg.set_value( KEY_P, not dpg.get_value( KEY_P ))
    interface.print_callback( str(dpg.get_value(KEY_P)) )

# Aplica os callbacks 
dpg.configure_item( 'key_E', callback = KEY_E_callback  )
dpg.configure_item( 'key_P', callback = KEY_P_callback  )



'''
Na câmera do Shooter quando o operador clicar na tecla "E" a
google mediapipe passa a funcionar. 
Ao apertar "E" novamente ela para de funcionar.
A IA irá medir a distância entre o centro dos olhos com o
centro da camera entregando valores de x e y.
'''
def run_shooter( holistic ):
    global distance_shooter_center_x, distance_shooter_center_y
    global mp_drawing, mp_drawing_styles, mp_holistic    

    shooter_status, shooter_texture = cap.get_capture_texture( Shooter )
    
    # # Inicia o media pipe
    if shooter_status:

        # Shooter tracker   
        if dpg.get_value( KEY_E ): 
            center_x_shooter = int(shooter_texture.shape[1] * 0.5)
            center_y_shooter = int(shooter_texture.shape[0] * 0.5)
            
            shooter_texture = cv2.cvtColor(shooter_texture, cv2.COLOR_BGR2RGB)
            shooter_texture.flags.writeable = False
            results = holistic.process(shooter_texture)
            shooter_texture.flags.writeable = True
            shooter_texture = cv2.cvtColor(shooter_texture, cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(shooter_texture, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            if results.pose_landmarks is not None:  
                # coordinates = (left eye + right eye / 2) * screen center
                x_shooter = int((results.pose_landmarks.landmark[2].x + results.pose_landmarks.landmark[5].x) * center_x_shooter)
                y_shooter = int((results.pose_landmarks.landmark[2].y + results.pose_landmarks.landmark[5].y) * center_y_shooter)
                
                distance_shooter_center_x = center_x_shooter - x_shooter
                distance_shooter_center_y = center_y_shooter - y_shooter

                cv2.line(shooter_texture, (x_shooter, y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 4)
                cv2.putText(shooter_texture, f'x:{x_shooter} y:{y_shooter}', (x_shooter, y_shooter - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # hypotenuse
                cv2.line(shooter_texture, (x_shooter, center_y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 2)
                cv2.putText(shooter_texture, f'{distance_shooter_center_x}', (x_shooter, center_y_shooter + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # x
                cv2.line(shooter_texture, (center_x_shooter, y_shooter), (center_x_shooter, center_y_shooter), (BGR[6]), 4)
                cv2.putText(shooter_texture, f'{distance_shooter_center_y}', (center_x_shooter + 20, y_shooter + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (BGR[8]), 2)  # y
                
                aim_sq = 50
                if distance_shooter_center_x in range(-aim_sq, aim_sq) and distance_shooter_center_y in range(-aim_sq, aim_sq):
                    interface.print_callback( 'Target on' )

        if dpg.get_value( KEY_P ):
            interface.print_callback( 'Taking picture.')
            if not os.path.exists('TargetPics'):
                os.mkdir('TargetPics')
            now = datetime.datetime.now()
            cv2.imwrite( PATH + '/TargetPics/target{}{}{}{}{}{}.jpg'.format(now.year, now.month, now.day, now.hour, now.minute, now.second), shooter_texture )
            dpg.set_value( KEY_P, False )

        
        #  Active adjustment on Screen 
        if dpg.get_value( 'KEY_A' ):
            center_x_shooter = dpg.get_item_width('win_cam_shooter')//2 # int(shooter_texture.shape[0] / 2 )
            center_y_shooter = dpg.get_item_width('win_cam_shooter')//2 # int(shooter_texture.shape[1] / 2 )

            cv2.line( shooter_texture, (center_x_shooter, 0), (center_x_shooter, shooter_texture.shape[0]), ( BGR[7]), 2 )
            cv2.line( shooter_texture, (0, center_y_shooter), (shooter_texture.shape[1], center_y_shooter), ( BGR[7]), 2 )


        # Atualiza a imagem para ficar de acordo com o padrão dpg 
        shooter_texture = cap.att_capture_texture( shooter_texture  )
        dpg.set_value( img_shooter, shooter_texture )
        dpg.configure_item( 'img_shooter', texture_tag = img_shooter )



# Inicia a camera de tiro 
def init_shooter( ):
    global  Shooter, img_shooter 
    try:
        interface.print_callback( 'Iniciando Shooter Cam ')
        Shooter, shooter_texture, w, h = cap.init_capture( CAP_ID = dpg.get_value(SHOOTER_ID), w = 640, h = 480 )
        img_shooter = dpg.add_raw_texture( parent = interface.textures_registry, height = h, width = w, default_value = shooter_texture, format = dpg.mvFormat_Float_rgb )
        
        dpg.configure_item( 'img_shooter', texture_tag = img_shooter )
        interface.print_callback( 'Shooter cam : ' + str(Shooter) )
        
        if Shooter == False: 
            dpg.set_value( SHOOTER_OK, False )
            interface.print_callback( 'Falha na inicialização do Shooter' )
        else: 
            dpg.set_value( SHOOTER_OK, True )
            interface.print_callback( 'Shooter inicializado com sucesso' )
    except: 
        dpg.set_value( SHOOTER_OK, False )
        interface.print_callback( 'Falha na inicialização do Shooter' )
    