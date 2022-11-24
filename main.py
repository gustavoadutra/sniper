import  dearpygui.dearpygui    as     dpg

from Interface import dpg_context as interface

interface.init_main( 'IRAE - Sniper' )

from    spotter                import * 
from    shooter                import * 
from    serial_dy              import * 

import threading 
import  time


# Defini os IDs das cameras 
dpg.set_value( SPOTTER_ID, 1 )
dpg.set_value( SHOOTER_ID, 0 )

# Porta conectado o OpenCR 
dpg.set_value( DEVICE, 'COM18' )

# As funções vem do spotter 
dpg.set_frame_callback( 2, init_spotter )
dpg.set_frame_callback( 3, init_shooter )
dpg.set_frame_callback( 4, init_serial  )


# Callback para encerrar o código 
dpg.add_key_press_handler( dpg.mvKey_Escape, callback = dpg.destroy_context, parent = interface.handlers_registry )


def thread_serial():
    global dpg
    if dpg.get_value( SERIAL_OK ):  run_serial() 
    else:                           dpg.set_value( SERIAL_OK, False )
def thread_shooter():
    global dpg
    if dpg.get_value( SHOOTER_OK ): run_shooter( holistic )
    else:                           dpg.configure_item( 'img_shooter', texture_tag = interface.ammo     )
def thread_spotter():
    global dpg
    if dpg.get_value( SPOOTER_OK ): run_spotter()
    else:                           dpg.configure_item( 'img_spotter', texture_tag = interface.accuracy )


# Main loop
with mp_holistic.Holistic(min_detection_confidence = 0.8, min_tracking_confidence = 0.8) as holistic:
    th_serial  = threading.Thread(target = thread_serial() )
    th_serial.start() 
    th_shooter = threading.Thread(target = thread_shooter())
    th_shooter.start()
    th_spotter = threading.Thread(target = thread_spotter())
    th_spotter.start()
    
    while dpg.is_dearpygui_running():
        # Medir o FPS do código
        dtime = time.time()

        dpg.render_dearpygui_frame()
        
        # Call the threadings    
        if not th_spotter.is_alive():
            th_spotter = threading.Thread(target = thread_spotter())            
            th_spotter.start() 
        if not th_shooter.is_alive():
            th_shooter = threading.Thread(target = thread_shooter())            
            th_shooter.start() 
        if not th_serial.is_alive():
            th_serial = threading.Thread( target = thread_serial() )
            th_serial.start() 
        interface.render_main()

        # Medir o FPS do código 
        dpg.configure_item( 'fps_info', default_value = 'FPS: ' + str(round(1/(time.time()-dtime),2) if time.time()-dtime != 0 else 0) )

# Encerrando os contextos 
dpg.destroy_context()
Spotter.release()
Shooter.release()