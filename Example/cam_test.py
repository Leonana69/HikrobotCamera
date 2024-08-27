import sys
sys.path.append('..')
from HikrobotCamera.hik_camera import HikCamera
import cv2
import time

hk = HikCamera()
hk.start_stream()
t1 = time.time()
frame_count = 0
while True:
    t2 = time.time()
    if t2 - t1 > 1:
        print('FPS:', frame_count / (t2 - t1))
        frame_count = 0
        t1 = time.time()
    frame = hk.get_frame_reader()
    if frame is not None:
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1