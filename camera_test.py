import cv2

# CAMERA ACTIVATION
webcam_shooter = cv2.VideoCapture(3)
webcam_shooter.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
webcam_shooter.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
'''
webcam_spotter = cv2.VideoCapture(0)  # CAM
webcam_spotter.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
webcam_spotter.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)'''



while True:
    success, frame_shooter = webcam_shooter.read()  # shooter

    if success:
        frame_shooter = cv2.flip(frame_shooter, 1)
        center_x_shooter = int(frame_shooter.shape[1] * 0.5)
        center_y_shooter = int(frame_shooter.shape[0] * 0.5)

        cv2.namedWindow('Shooter View')
        # cv2.namedWindow('Spotter View')

        cv2.imshow('Shooter View', frame_shooter)
        #cv2.imshow('Spotter View', frame_spotter)


    if cv2.waitKey(1) and 0xff == ord('q'):
        break

# DISABLE CAMERA
webcam_shooter.release()
# webcam_spotter.release()

# CLOSE WINDOWS
cv2.destroyAllWindows()
