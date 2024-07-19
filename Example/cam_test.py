import sys
sys.path.append('..')
from HikrobotCamera.hik_camera import HikCamera
import cv2

hk = HikCamera()
hk.start_stream()
while True:
    frame = hk.get_frame_reader()
    if frame is not None:
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break