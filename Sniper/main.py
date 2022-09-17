from    Interface              import dpg_context          as interface
from    Capture                import capture              as cap 
from    IA                     import follow               as ia

import  dearpygui.dearpygui    as dpg 
import  mediapipe              as mp
import  numpy                  as np
import  time 
import  cv2
import  os

interface.init_main( 'Novo Sniper Brasileiro' )

PATH    = os.path.dirname( __file__ )


CAMERAS_OK = dpg.add_bool_value( default_value = False, parent = interface.values_registry )
SERIAL_OK  = dpg.add_bool_value( default_value = False, parent = interface.values_registry ) 

img_spotter = cap.img_spotter 
img_shooter = cap.img_shooter 
Shooter     = cap.Shooter 
Spotter     = cap.Spotter


def init_capture():
    global img_spotter, img_shooter 
    global Spotter, Shooter 

    # Janela de aviso de carregamento das câmeras 
    with dpg.window( tag = 'win_loading', label = 'Aguarde...', width = 250, height = 100, pos = [dpg.get_viewport_width()/2-125, dpg.get_viewport_height()/2-50] ):
        dpg.add_text( tag = 'loading_msg', default_value = 'Carregando as imagens das câmeras', parent = 'win_loading' ) 

    try:
        Spotter, spotter_texture, w, h = cap.init_capture( CAP_ID = 0 , w = 640, h = 480 )
        img_spotter = dpg.add_raw_texture( parent = interface.textures_registry, height = h, width = w, default_value = spotter_texture, format = dpg.mvFormat_Float_rgb )
        dpg.configure_item( 'img_spotter', texture_tag = img_spotter )

        Shooter, shooter_texture, w, h = cap.init_capture( CAP_ID = PATH + '\\Interface\\videos\\ExemploITA.mp4', w = 280, h = 460 )
        img_shooter = dpg.add_raw_texture( parent = interface.textures_registry, height = h, width = w, default_value = shooter_texture, format = dpg.mvFormat_Float_rgb )
        dpg.configure_item( 'img_shooter', texture_tag = img_shooter )
        
        cap.conf_capture( Shooter, bright = 80, contrast = 100 ) 
        cap.conf_capture( Spotter, bright = 80, contrast = 100 ) 

        dpg.delete_item( 'win_loading')
        dpg.set_value( CAMERAS_OK, True )
    
    except:
        dpg.configure_item('loading_msg', 'Erro ao carregar as câmeras' )
        dpg.set_value( CAMERAS_OK, False )

dpg.set_frame_callback( 2, init_capture )


# # Mouse callbacks
def r_mouse_detection( sender, data, user ):
    mouse_x, mouse_y = dpg.get_mouse_pos()
    # axes_motor_x = mouse_x - center_x
    # axes_motor_y = mouse_y - center_y
    # aim_distance = np.sqrt(axes_motor_x ** 2 + axes_motor_y ** 2)
    # # print('Distance to Aim: ', aim_distance)
    # # print('X: ', axes_motor_x, 'Y: ', axes_motor_y)
    dpg.set_value( interface.CALLBACK, dpg.get_value(interface.CALLBACK) + 'R_CLICK\r X: {}\rY: {} ADD_CALLBACK\n'.format(mouse_x, mouse_y) )

def l_mouse_detection( sender, data, user ):
    mouse_x, mouse_y = dpg.get_mouse_pos()
    dpg.set_value( interface.CALLBACK, dpg.get_value(interface.CALLBACK) + 'L_CLICK\r X: {}\rY: {} ADD_CALLBACK\n'.format(mouse_x, mouse_y) )

dpg.configure_item( interface.r_mouse, callback = r_mouse_detection )
dpg.configure_item( interface.l_mouse, callback = l_mouse_detection )



# Main loop  
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

    dtime = time.time()
    if dpg.get_value( CAMERAS_OK ):
        spotter_status, spotter_texture = cap.get_capture_texture( Spotter )
        shooter_status, shooter_texture = cap.get_capture_texture( Shooter )

            # TODAS MANIPULAÇÕES DO SPOTTER AQUI
        if spotter_status: 
            imgRGB = cv2.cvtColor( spotter_texture, cv2.COLOR_BGR2RGB)
            centerx = int(spotter_texture.shape[0] * 0.5)
            centery = int(spotter_texture.shape[1] * 0.5)
            results = ia.pose.process(imgRGB)
            if results.pose_landmarks:
                ia.mpDraw.draw_landmarks(spotter_texture, results.pose_landmarks, ia.mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = spotter_texture.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(spotter_texture, (cx, cy), 3, (ia.myColors[6][1]), cv2.FILLED)

            spotter_texture = ia.aim_print(spotter_texture, centery, centerx, (ia.myColors[6][1]))
            spotter_texture = ia.find_skin(spotter_texture, ia.mySkin)
            spotter_texture = ia.faces_and_eyes( spotter_texture, (ia.myColors[1][1]), (ia.myColors[2][1]))

            spotter_texture = cap.att_capture_texture( spotter_texture  )
            dpg.set_value( img_spotter, spotter_texture )


        if shooter_status: 
            shooter_texture = cap.att_capture_texture( shooter_texture  )
            dpg.set_value( img_shooter, shooter_texture )


        dpg.configure_item( 'img_spotter', texture_tag = img_spotter )
        dpg.configure_item( 'img_shooter', texture_tag = img_shooter )
    else: 
        dpg.configure_item( 'img_spotter', texture_tag = interface.accuracy )
        dpg.configure_item( 'img_shooter', texture_tag = interface.ammo     )
    
    dpg.configure_item( 'fps_info', default_value = 'FPS: ' + str(round(1/(time.time()-dtime),2) if time.time()-dtime != 0 else 0) )

# Encerrando os contextos 
dpg.destroy_context()
cv2.destroyAllWindows()
Spotter.release()
Shooter.release()