from datetime import datetime
import re
import cv2
import numpy as np

import PCA.PCA_math as PCA
import settings.settings as set_man
import camera.camera as cam_man
import event.event as event_man


# module config
_color_red = (0, 0, 255)
_last_time: datetime = None


def action_mode_setup():
    PCA.load_model()


def action_mode_loop():
    global _last_time

    # load settings
    cam = cam_man.get_cam()
    frame_size = set_man.get_settings('frame_size')
    avg_mine_dia = set_man.get_settings('avg_mine_dia')
    match_list = set_man.get_settings('match_list')

    # read frame from camera
    _, frame = cam.read()
    frame = cv2.resize(frame, dsize=(frame_size, frame_size), interpolation=cv2.INTER_CUBIC)
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # create sliding window view
    view = np.lib.stride_tricks.sliding_window_view(grey_frame, (avg_mine_dia, avg_mine_dia))
    view_shape = view.shape

    # skip n when scanning the frame
    slide_wind_res = int(avg_mine_dia * 0.3)
    
    # circle draw offset
    cir_offset = 0.7

    # found match flag
    is_match = False
    for x in range(0, view_shape[0], slide_wind_res):
        for y in range(0, view_shape[1], slide_wind_res):
            detected_img = PCA.match_image(view[x, y])
            
            reg_ex = f"./dataset/(?:{'|'.join(match_list)})[0-9]+.jpg"
            if re.match(reg_ex, detected_img):
                
                # post serial_read_event_listner
                event_man.post_event('serial_read', 'U')

                # draw circle around the matched object
                cir_y = int(y + avg_mine_dia * cir_offset)
                cir_x = int(x + avg_mine_dia * cir_offset)
                frame = cv2.circle(frame, (cir_y, cir_x), int(avg_mine_dia / 2), _color_red, 2)
                
                is_match = True
                break
        
        if is_match:
            break

    cv2.imshow('Robot Camera', frame)

    # read key hit
    key = cv2.waitKey(1) & 0xFF

    # process key hits
    if (key == ord('q')):
        return -1
