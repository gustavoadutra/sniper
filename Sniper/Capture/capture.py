import numpy as np
import cv2 


img_spotter = [] 
img_shooter = [] 
Shooter = None 
Spotter = None


# Inicia a câmera ou carrega um vídeo do CAP_ID
def init_capture( CAP_ID : str, w : int = 480, h : int = 640 ):
    try:
        cap = cv2.VideoCapture( CAP_ID,  cv2.CAP_DSHOW )
        cap.set( cv2.CAP_PROP_FRAME_WIDTH , w )
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, h )
        

        _, frame = cap.read()
        
        # Image size or you can get this from image shape
        frame_width     = cap.get( cv2.CAP_PROP_FRAME_WIDTH  )
        frame_height    = cap.get( cv2.CAP_PROP_FRAME_HEIGHT )
        print( frame_width, frame_height )

        # First webcam run to create the texture registry  
        data = np.flip( frame, 2 )
        data = data.ravel()
        data = np.asfarray(data, dtype = 'f' )
        frame_texture = np.true_divide(data, 255.0)

        return cap, frame_texture, frame_width, frame_height
    
    except: 
        return False, [], -1, -1


# Configura os parametros da Câmera 
def conf_capture( cap, bright : int = 80, contrast : int = 100 ):    
    cap.set( 10, bright  )  # Bright
    cap.set( 11, contrast)  # Contrast


# Realiza a captura de imagem da Camera CAP 
def get_capture_texture( cap ):
    try:
        success, frame = cap.read()
        if success: 
            return True, frame
        else:
            return False, [] 
    except:
        return False, []


# Atualiza a textura para o padrão dpg
def att_capture_texture( texture ):
    data = np.flip( texture, 2 )
    data = data.ravel()
    data = np.asfarray(data, dtype = 'f' )
    texture_data = np.true_divide(data, 255.0)
    return texture_data 