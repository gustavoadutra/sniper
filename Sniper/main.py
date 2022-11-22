import threading

from Interface import dpg_context as interface
from _sniper_utils import *

import dearpygui.dearpygui as dpg
import time
import cv2

# Nome da viewport 
interface.init_main('Novo Sniper Brasileiro')

from spotter import *
from shooter import *
from serial_dy import *

# Defini os IDs das cameras 
dpg.set_value(SPOTTER_ID, 0)
dpg.set_value(SHOOTER_ID, 0)

# Porta conectado o OpenCR
dpg.set_value(DEVICE, 'COM18')

# As funções vem do spotter
dpg.set_frame_callback(2, init_spotter)
dpg.set_frame_callback(3, init_shooter)
dpg.set_frame_callback(4, init_serial )

# Callback para encerrar o código
dpg.add_key_press_handler(dpg.mvKey_Escape, callback=dpg.destroy_context, parent=interface.handlers_registry)
dpg.add_key_press_handler(dpg.mvKey_Q, callback=dpg.destroy_context, parent=interface.handlers_registry)


def thread_serial():
    global dpg
    if dpg.get_value(SERIAL_OK):
        try:
            run_serial()
            dpg.configure_item('SERIAL', default_value='SERIAL : ACTIVATED\n')
        except:
            interface.print_callback('Erro na serial ')
            dpg.set_value(SERIAL_OK, False)
            dpg.configure_item('SERIAL', default_value='SERIAL : INACTIVATED\n')

def thread_shooter():
    global dpg
    if dpg.get_value(SHOOTER_OK):
        run_shooter(holistic)
        dpg.configure_item('SHOOTER', default_value='SHOOTER : ACTIVATED\n')
    else:
        dpg.configure_item('img_shooter', texture_tag=interface.ammo)
        dpg.configure_item('SHOOTER', default_value='SHOOTER : INACTIVATED\n')


def thread_spotter():
    global dpg
    if dpg.get_value(SPOOTER_OK):
        run_spotter()
        dpg.configure_item('SPOTTER', default_value='SPOTTER : ACTIVATED\n')
    else:
        dpg.configure_item('img_spotter', texture_tag=interface.accuracy)
        dpg.configure_item('SPOTTER', default_value='SPOTTER : ACTIVATED\n')


# Main loop
with mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8) as holistic:

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

        dpg.configure_item('fps_info', default_value='FPS: ' + str(round(1 / (time.time() - dtime), 2) if time.time() - dtime != 0 else 0))


# Encerrando os contextos 
dpg.destroy_context()
cv2.destroyAllWindows()
Spotter.release()
Shooter.release()
