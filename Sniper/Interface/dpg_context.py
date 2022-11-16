import dearpygui.dearpygui as dpg
import os

# INICIA O CONTEXTO DO DEARPYGUI 
dpg.create_context()

# REGISTRADORES DE VARIAVEIS GLOBAIS DO DPG (INTERFACE)
with dpg.value_registry() as values_registry:
    NUM_DEBUG_LINES = dpg.add_int_value(default_value=15)
    BUT_TOTAL = dpg.add_int_value(default_value=10)
    CALLBACK = dpg.add_string_value(default_value='')

# REGISTRO DE TEXTURAS UTILZIADOS PARA AS IMAGENS
with dpg.texture_registry(show=True) as textures_registry:
    # PEGA O CAMINHO ABSOLUTO DO PATH DE IMAGENS
    PATH = os.path.dirname(__file__)

    # IMAGENS DOS BOTÕES 
    # FAZER OS REGISTROS DE CADA IMAGEM COM OS MESMOS COMANDOS ABAIXO 
    accuracy_w, accuracy_h, accuracy_c, accuracy_data, = dpg.load_image(PATH + '\\images\\accuracy-100.png')
    ammo_w, ammo_h, ammo_c, ammo_data, = dpg.load_image(PATH + '\\images\\ammo-100.png')
    facial_recognition_w, facial_recognition_h, facial_recognition_c, facial_recognition_data, = dpg.load_image(
        PATH + '\\images\\facial-recognition-100.png')
    laser_w, laser_h, laser_c, laser_data, = dpg.load_image(PATH + '\\images\\laser-96.png')
    person_track_w, person_track_h, person_track_c, person_track_data, = dpg.load_image(
        PATH + '\\images\\person-track-80.png')
    take_picture_w, take_picture_h, take_picture_c, take_picture_data, = dpg.load_image(
        PATH + '\\images\\picture-100.png')
    reset_button_w, reset_button_h, reset_button_c, reset_button_data, = dpg.load_image(PATH + '\\images\\reset-58.png')
    services_w, services_h, services_c, services_data, = dpg.load_image(PATH + '\\images\\services-100.png')
    sniper_point_w, sniper_point_h, sniper_point_c, sniper_point_data, = dpg.load_image(
        PATH + '\\images\\sniper-64.png')
    sniper_gun_w, sniper_gun_h, sniper_gun_c, sniper_gun_data, = dpg.load_image(PATH + '\\images\\sniper-100.png')
    tracking_w, tracking_h, tracking_c, tracking_data, = dpg.load_image(PATH + '\\images\\tracking-100.png')
    no_image_w, no_image_h, no_image_c, no_image_data = dpg.load_image(PATH + '\\images\\no_image.png')

    # CRIAR AS TEXTURAS DE CADA IMAGEM
    accuracy = dpg.add_static_texture(width=accuracy_w, height=accuracy_h, default_value=accuracy_data)
    ammo = dpg.add_static_texture(width=ammo_w, height=ammo_h, default_value=ammo_data)
    facial_recognition = dpg.add_static_texture(width=facial_recognition_w, height=facial_recognition_h,
                                                default_value=facial_recognition_data)
    laser = dpg.add_static_texture(width=laser_w, height=laser_h, default_value=laser_data)
    person_track = dpg.add_static_texture(width=person_track_w, height=person_track_h, default_value=person_track_data)
    take_picture = dpg.add_static_texture(width=take_picture_w, height=take_picture_h, default_value=take_picture_data)
    reset_button = dpg.add_static_texture(width=reset_button_w, height=reset_button_h, default_value=reset_button_data)
    services = dpg.add_static_texture(width=services_w, height=services_h, default_value=services_data)
    sniper_point = dpg.add_static_texture(width=sniper_point_w, height=sniper_point_h, default_value=sniper_point_data)
    sniper_gun = dpg.add_static_texture(width=sniper_gun_w, height=sniper_gun_h, default_value=sniper_gun_data)
    tracking = dpg.add_static_texture(width=tracking_w, height=tracking_h, default_value=tracking_data)
    no_image = dpg.add_static_texture(width=no_image_w, height=no_image_h, default_value=no_image_data)

# CALLBACKS DOS INPUTS DE TECLADO // JOYSTICK // MOUSE
with dpg.handler_registry() as handlers_registry:
    key_G = dpg.add_key_release_handler(tag='key_G', key=dpg.mvKey_G, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))
    key_K = dpg.add_key_release_handler(tag='key_K', key=dpg.mvKey_K, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))
    key_R = dpg.add_key_release_handler(tag='key_R', key=dpg.mvKey_R, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))

    key_E = dpg.add_key_release_handler(tag='key_E', key=dpg.mvKey_E, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))

    key_A = dpg.add_key_release_handler(tag='key_A', key=dpg.mvKey_A, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))
    key_H = dpg.add_key_release_handler(tag='key_H', key=dpg.mvKey_H, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))
    key_P = dpg.add_key_release_handler(tag='key_P', key=dpg.mvKey_P, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))

    key_L = dpg.add_key_release_handler(tag='key_L', key=dpg.mvKey_L, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))

    key_X = dpg.add_key_release_handler(tag='key_X', key=dpg.mvKey_X, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))
    key_Y = dpg.add_key_release_handler(tag='key_Y', key=dpg.mvKey_Y, callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                                             dpg.get_value(
                                                                                                                 CALLBACK) + s + ' key pressed\n'))

    r_mouse = dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right,
                                          callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                 dpg.get_value(CALLBACK) + str(
                                                                                     d) + ' R click pressed\n'))
    l_mouse = dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left,
                                          callback=lambda s, d, u: dpg.set_value(CALLBACK,
                                                                                 dpg.get_value(CALLBACK) + str(
                                                                                     d) + ' L click pressed\n'))


# CALLBACK DE REDIMENSIONAMENTO DA TELA PRINCIPAL 
def resize_main(sender, data, user):
    # PROPORÇÃO DO TAMANHO DA TELA  
    prop_x, prop_y = data[2] / 1473, data[3] / 841

    # REDIMENSIONAMENTO DE JANELAS
    dpg.configure_item(item='win_cam_spotter', pos=[10 * prop_x, 10 * prop_y], width=900 * prop_x, height=565 * prop_y)
    dpg.configure_item(item='win_cam_shooter', pos=[915 * prop_x, 110 * prop_y], width=550 * prop_x,
                       height=325 * prop_y)
    dpg.configure_item(item='win_info_above', pos=[10 * prop_x, 580 * prop_y], width=1455 * prop_x, height=250 * prop_y)

    # REDIMENSIONAMENTO DOS FILHOS 
    dpg.configure_item('running_infos', width=dpg.get_item_width('win_info_above') * 1 / 3 - 20)
    dpg.configure_item('key_infos', width=dpg.get_item_width('win_info_above') * 1 / 3 - 20)
    dpg.configure_item('callbacks_infos', width=dpg.get_item_width('win_info_above') * 1 / 3 - 20)

    # REDIMENSIONAMENTO DOS ELEMENTOS  
    dpg.configure_item(item='img_spotter', width=dpg.get_item_width('win_cam_spotter'),
                       height=dpg.get_item_height('win_cam_spotter'))
    dpg.configure_item(item='img_shooter', width=dpg.get_item_width('win_cam_shooter'),
                       height=dpg.get_item_height('win_cam_shooter'))

    # REDIMENSIONAMENTO DOS BOTÕES 
    dpg.configure_item('but_G', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_K', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_R', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_E', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_A', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_H', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_P', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_Q', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_X', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)
    dpg.configure_item('but_Y', width=dpg.get_item_width('win_info_above') / dpg.get_value(BUT_TOTAL) - 17)


# CRIAÇÃO DA TELA PRINCIOAL
# TODOS ELEMENTOS DESENHADOS NA TELA FORAM FEITOS AQUI 
# PARA ADICIONAR UM BOTÃO OU ALGUMA FUNCIONALIDADE A MAIS, DEVE SER FEITA AQUI 
def init_main(window_name):
    with dpg.window(tag='main_window', no_close=True, no_collapse=True, no_move=True, no_scrollbar=True,
                    no_title_bar=True):
        # Janela de apresentação da camera sputter 
        with dpg.window(tag='win_cam_spotter', no_close=True, no_resize=True, no_collapse=True, no_move=True,
                        no_scrollbar=True, no_title_bar=True):
            dpg.add_image(tag='img_spotter', texture_tag=accuracy, width=dpg.get_item_width('win_cam_spotter'),
                          height=dpg.get_item_height('win_cam_spotter'))
            # Janela de de apresentação da camera shooter
        with dpg.window(tag='win_cam_shooter', no_close=True, no_resize=True, no_collapse=True, no_move=True,
                        no_scrollbar=True, no_title_bar=True):
            dpg.add_image(tag='img_shooter', texture_tag=ammo, width=dpg.get_item_width('win_cam_shooter'),
                          height=dpg.get_item_height('win_cam_shooter'))
            # Janela de inputs para o programa
        with dpg.window(tag='win_info_above', no_close=True, no_resize=True, no_collapse=True, no_move=True,
                        no_scrollbar=True, no_title_bar=True):
            # Botões de execução
            with dpg.child_window(tag='inputs', width=-1, height=90, border=False, no_scrollbar=True):
                with dpg.group(horizontal=True, pos=[5, 0]):
                    dpg.add_image_button(tag='but_G', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=facial_recognition)
                    dpg.add_image_button(tag='but_K', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=accuracy)
                    dpg.add_image_button(tag='but_R', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=reset_button)
                    dpg.add_image_button(tag='but_E', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=person_track)
                    dpg.add_image_button(tag='but_A', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=ammo)
                    dpg.add_image_button(tag='but_H', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=take_picture)
                    dpg.add_image_button(tag='but_P', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=sniper_gun)
                    dpg.add_image_button(tag='but_Q', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=sniper_point)
                    dpg.add_image_button(tag='but_X', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=tracking)
                    dpg.add_image_button(tag='but_Y', height=75,
                                         width=dpg.get_item_width(dpg.last_container()) / dpg.get_value(BUT_TOTAL) - 6,
                                         callback=lambda s, d, u: dpg.set_value(CALLBACK, dpg.get_value(
                                             CALLBACK) + s + ' button pressed\n'), texture_tag=services)

                    # ADICIONA DICAS QUANDO O MOUSE É POSTO EM CIMA DE ALGUM BOTÃO 
                    with dpg.tooltip(parent='but_G'):
                        dpg.add_text(
                            'ROI Square:\nCria um retangulo para \nfazer o enquadramento do rosto \npara perseguição\n\nshortkey: G')
                    with dpg.tooltip(parent='but_K'):
                        dpg.add_text('Perseguição:\nFaz a perseguição da pessoa\nClick+ROI open\n\nshortkey: K')
                    with dpg.tooltip(parent='but_R'):
                        dpg.add_text('ROI reset:\nReseta a função ROI Square\n\nshortkey: R')

                    with dpg.tooltip(parent='but_E'):
                        dpg.add_text('Tracking:\nInicia a perseguição\n\nshortkey: E')
                    with dpg.tooltip(parent='but_A'):
                        dpg.add_text('function_B\nshortkey: B')
                    with dpg.tooltip(parent='but_H'):
                        dpg.add_text('function_H\nshortkey: H')
                    with dpg.tooltip(parent='but_P'):
                        dpg.add_text('function_P\nshortkey: P')
                    with dpg.tooltip(parent='but_Q'):
                        dpg.add_text('function_Q\nshortkey: Q')
                    with dpg.tooltip(parent='but_X'):
                        dpg.add_text('function_X\nshortkey: X')
                    with dpg.tooltip(parent='but_Y'):
                        dpg.add_text('function_Y\nshortkey: Y')

            # Janelas de exebição de informações de execução
            with dpg.child_window(tag='outputs', width=-1, height=-1, border=False):
                with dpg.group(horizontal=True, pos=[5, 5]):
                    with dpg.child_window(tag='running_infos', width=dpg.get_item_width('win_info_above') * 1 / 3,
                                          height=-1, border=False):
                        dpg.add_text('Informações de execução')
                        with dpg.child_window(width=-1, height=-1):
                            dpg.add_text(tag='fps_info', default_value='FPS: 0.0')
                            dpg.add_text(tag='device_info', default_value='Device: Desconectado')
                            dpg.add_text(tag='baudrate_info', default_value='Baudrate: Desconectado')

                    with dpg.child_window(tag='key_infos', width=dpg.get_item_width('win_info_above') * 1 / 3,
                                          height=-1, border=False):
                        dpg.add_text('Operações ativas:')
                        with dpg.child_window(width=-1, height=-1):
                            SPOTTER = dpg.add_text(tag='SPOTTER', default_value='SPOTTER: INACTIVATED\n')
                            SHOOTER = dpg.add_text(tag='SHOOTER', default_value='SHOOTER: INACTIVATED\n')
                            SERIAL = dpg.add_text(tag='SERIAL', default_value='SERIAL : INACTIVATED\n')

                    with dpg.child_window(tag='callbacks_infos', width=dpg.get_item_width('win_info_above') * 1 / 3,
                                          height=-1, border=False):
                        dpg.add_text('Callbacks:')
                        with dpg.child_window(width=-1, height=-1):
                            dpg.add_text(tag='callbacks', source=CALLBACK, tracked=True, track_offset=1)

                            # CONFIGURAÇÕES DE VIEWPORT
    # O SISTEMA OPERACIONAL IRÁ ENXERGAR ESSA VIEWPORT NA ÁRVORE DE PROCESSOS 
    dpg.create_viewport(title=window_name, width=600, min_width=1000, height=200, min_height=800)

    # INCIA O DEARPYGUI 
    dpg.setup_dearpygui()

    # DEFINE E HABILITA A JANELA PRINCIPAL 
    dpg.set_primary_window("main_window", True)
    dpg.set_viewport_resize_callback(resize_main)
    dpg.maximize_viewport()
    dpg.show_viewport()


# FUNÇÃO PARA RENDERIZAÇÃO DA JANELA PRINCIPAL 
def render_main():
    pass


# PRINTA UMA MENSAGEM DE LOG 
def print_callback(msg: str) -> bool:
    if type(msg) == str:
        dpg.set_value(CALLBACK, dpg.get_value(CALLBACK) + msg + '\n')
    else:
        try:
            dpg.set_value(CALLBACK, dpg.get_value(CALLBACK) + str(msg) + '\n')
        except:
            return False

    lines = dpg.get_value(CALLBACK).split('\n')
    if len(lines) > dpg.get_value(NUM_DEBUG_LINES):
        msg = ''
        for line in lines[dpg.get_value(NUM_DEBUG_LINES):]:
            msg += line + '\n'
        dpg.set_value(CALLBACK, msg)
    return True
