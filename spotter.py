from Interface import dpg_context as interface, variables as var 
from Capture   import capture     as cap 

import dearpygui.dearpygui as dpg 
import cv2

# Create tracker TLD
tracker = cv2.legacy.TrackerTLD_create()  

r_ROI_X = 50
r_ROI_Y = 50

mouseX, mouseY = 0, 0 
spotter_texture = [] 
bbox_spotter    = []
ret_xi          = 0 
ret_yi          = 0 
ret_xo          = 0  
ret_yo          = 0 

# Valores de texturas 
img_spotter = cap.img_spotter 
Spotter     = cap.Spotter

# Registradores de controle 
SPOOTER_OK  = dpg.add_bool_value( tag = 'SPOOTER_OK', default_value = False, parent = interface.values_registry )
SPOTTER_ID  = dpg.add_int_value ( default_value = 0    , parent = interface.values_registry )
KEY_G       = dpg.add_bool_value( default_value = False, parent = interface.values_registry )
L_BUTTON    = dpg.add_bool_value( default_value = False, parent = interface.values_registry )
BBOX_TRACK  = dpg.add_bool_value( default_value = False, parent = interface.values_registry )

# Turn ON the Selection of a ROI
def KEY_G_callback (sender, data, user): 
    dpg.set_value( KEY_G, not dpg.get_value( KEY_G ))
    interface.print_callback( str(dpg.get_value(KEY_G)) )

# Reset the ROI
def KEY_R_callback( sender, data, user ):
    global tracker
    try:
        tracker = cv2.legacy.TrackerTLD_create()
        dpg.set_value( BBOX_TRACK, False )
        dpg.set_value( KEY_G, False )
        interface.print_callback( 'Tracker Reseted')
    except:
        print( 'Erro ao reiniciar a Legacy Tracker')

# Create ROI Square
def mouse_l_button( sender, data, user ): 
    dpg.set_value( L_BUTTON, True )

# SPOTTER MOUSE DETECTION 
# MouseWheel Grow the Square ROI
def mouse_wheel( sendar, data, user ):  # Mouse Parameters [ rotação ]
    global r_ROI_X, r_ROI_Y, bbox_spotter
    if data > 0:
        r_ROI_X = r_ROI_X + 3
        r_ROI_Y = r_ROI_Y + 3
    if data < 0:
        r_ROI_X = r_ROI_X - 3
        r_ROI_Y = r_ROI_Y - 3
    r_ROI_X, r_ROI_Y = r_ROI_X, r_ROI_Y
    interface.print_callback( 'New range: ROI X =' + str(r_ROI_X) + 'ROI Y =' + str(r_ROI_Y))

# Aplicação dos handlers 
dpg.add_mouse_click_handler( dpg.mvMouseButton_Left, callback = mouse_l_button, parent = interface.handlers_registry  )
dpg.add_mouse_wheel_handler( callback = mouse_wheel, parent = interface.handlers_registry  ) 
dpg.configure_item( 'but_K', callback = mouse_l_button  )
dpg.configure_item( 'but_G', callback = KEY_G_callback  )
dpg.configure_item( 'key_G', callback = KEY_G_callback  )
dpg.configure_item( 'but_R', callback = KEY_R_callback  )
dpg.configure_item( 'key_R', callback = KEY_R_callback  )


'''
Funciona na camera do spotter. Liga a ROI na tecla "G".
Ao clicar com mouse botão esquerdo liga TLD.
Ao clicar no "R" reseta ou desliga a TLD
Pode ainda rolar o scroll do mouse aumentando ou diminuindo O retângulo da ROI.
'''
def run_spotter( ):
    global ret_xi, ret_yi, ret_xo, ret_yo
    global tracker, bbox_spotter

    spotter_status, spotter_texture = cap.get_capture_texture( Spotter )
    if spotter_status: 

        # Turn ON the Selection of a ROI
        # Create a DRAW rectangle of a ROI 
        if dpg.get_value( KEY_G ):
            dpg.bind_item_theme( 'but_G', interface.on_button )
            try:
                mouseX, mouseY = dpg.get_mouse_pos()
                ret_xi = mouseX - r_ROI_X - 25   
                ret_xo = mouseX + r_ROI_X - 25    
                ret_yi = mouseY - r_ROI_Y  
                ret_yo = mouseY + r_ROI_Y 
                cv2.rectangle( spotter_texture, (int(ret_xi), int(ret_yi)), (int(ret_xo), int(ret_yo)), (var.BGR[1]), 2) 
            except:
                interface.print_callback( 'Erro na função ROI Square \nTente novamente') 
        else:
            dpg.bind_item_theme( 'but_G', interface.def_button )


        # Create ROI Square
        if dpg.get_value( L_BUTTON ):
            if dpg.get_value( KEY_G ):
                try: 
                    bbox_spotter = (ret_xi, ret_yi, (r_ROI_X * 2), (r_ROI_Y * 2))
                    tracker.init( spotter_texture, bbox_spotter )    
                    interface.print_callback('L_BUTTON - ROI SELECTION ACTIVATE') 
                    dpg.configure_item( 'SPOTTER', default_value = 'SPOTTER: ACTIVATED' )       
                    dpg.set_value( BBOX_TRACK, True )       
                    dpg.set_value( KEY_G, False ) 

                except:
                    interface.print_callback('ROI SELECTION FAIL')        
            dpg.set_value( L_BUTTON, False ) 


        # Draw tracked objects
        if dpg.get_value( BBOX_TRACK ): 
            dpg.bind_item_theme( 'but_K', theme = interface.on_button )
            try:
                _, bbox_spotter = tracker.update( spotter_texture )
                p1 = (int(bbox_spotter[0]), int(bbox_spotter[1]) )
                p2 = (int(bbox_spotter[0] + bbox_spotter[2]), int(bbox_spotter[1] + bbox_spotter[3]))
                cv2.rectangle(spotter_texture, p1, p2, (255, 0, 0), 2, 1)
            except:
                dpg.set_value( BBOX_TRACK, False )
        else:
            dpg.bind_item_theme( 'but_K', theme = interface.def_button )  


        if dpg.get_value( 'KEY_A' ): 
            center_x_shooter = spotter_texture.shape[0] // 2
            center_y_shooter = spotter_texture.shape[1] // 2
            cv2.line( spotter_texture, (center_x_shooter, 0), (center_x_shooter, spotter_texture.shape[0]), ( var.BGR[7]), 2 )
            cv2.line( spotter_texture, (0, center_y_shooter), (spotter_texture.shape[1], center_y_shooter), ( var.BGR[7]), 2 )

        # Atualiza a imagem para ficar de acordo com o padrão dpg 
        spotter_texture = cap.att_capture_texture( spotter_texture  )
        dpg.set_value( img_spotter, spotter_texture )
        dpg.configure_item( 'img_spotter', texture_tag = img_spotter )


# Inicia a camera de visualização 
def init_spotter( ):
    global Spotter, img_spotter 
    try:
        interface.print_callback( 'Iniciando Spotter Cam ')
        Spotter, spotter_texture, w, h = cap.init_capture( CAP_ID = dpg.get_value(SPOTTER_ID) , w = 640, h = 480 )
        img_spotter = dpg.add_raw_texture( parent = interface.textures_registry, height = h, width = w, default_value = spotter_texture, format = dpg.mvFormat_Float_rgb )
        dpg.configure_item( 'img_spotter', texture_tag = img_spotter )
        interface.print_callback( 'Spotter cam : ' + str(Spotter) )
        if Spotter == False:
            dpg.set_value( SPOOTER_OK, False )
            interface.print_callback( 'Falha na inicialização do Spotter' )
        else:
            dpg.set_value( SPOOTER_OK, True )
            interface.print_callback( 'Spotter inicializado com sucesso' )
    except: 
        dpg.set_value( SPOOTER_OK, False )
        interface.print_callback( 'Falha na inicialização do Spotter' )
