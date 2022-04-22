import cv2
from datetime import datetime

import PCA.PCA_math as PCA
import settings.settings as set_man
import utils.log as log_man
import camera.camera as cam_man
import utils.img as img_man
import settings.settings as set_man

# module config
_color_red = (0, 0, 255)
_color_white = (255, 255, 255)


def training_mode_setup():
    PCA.load_model()


def training_mode_loop():
    # load settings
    avg_mine_dia = set_man.get_settings('avg_mine_dia')
    cam = cam_man.get_cam()
    frame_size = set_man.get_settings('frame_size')


    # read frame from camera
    _, frame = cam.read()
    frame = cv2.resize(frame, dsize=(frame_size, frame_size), interpolation=cv2.INTER_CUBIC)
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # check if there is object in the middle of the frame
    is_mid = img_man.is_obj_in_middle(grey_frame)

    mid_obj_x = int(frame_size / 2)
    mid_obj_y = int(frame_size / 2)

    # highlight middle object
    if (is_mid):
        frame = cv2.circle(frame, (mid_obj_x, mid_obj_y), 2, _color_red, -1)
        frame = cv2.circle(frame, (mid_obj_x, mid_obj_y),
                           int(avg_mine_dia / 2), _color_red, 2)
    else:
        frame = cv2.circle(frame, (mid_obj_x, mid_obj_y), 2, _color_white, -1)
        frame = cv2.circle(frame, (mid_obj_x, mid_obj_y),
                           int(avg_mine_dia / 2), _color_white, 2)

    # show modified frame
    cv2.imshow('Robot Camera', frame)

    # read key hit
    key = cv2.waitKey(1) & 0xFF

    # process key hit
    if (key == ord('s')):
        # crop central image
        cor_image = grey_frame[int(mid_obj_x - (avg_mine_dia) / 2):int(mid_obj_x + ((avg_mine_dia) / 2)),
                               int(mid_obj_y - (avg_mine_dia) / 2):int(mid_obj_y + ((avg_mine_dia) / 2))]

        # save image to the dataset directory
        cur_img_count: int = set_man.get_settings('next_img_index')
        img_dir = f"./dataset/img{cur_img_count}.jpg"
        set_man.set_settings('next_img_index', cur_img_count + 1)
        cv2.imwrite(img_dir, cor_image)

        log_man.add_log('modes.training_mode_loop',
                        'DEBUG', f"added image {img_dir} to dataset")

    elif (key == ord('t')):
        # crop central image
        cor_image = grey_frame[int(mid_obj_x - (avg_mine_dia) / 2):int(mid_obj_x + ((avg_mine_dia) / 2)),
                               int(mid_obj_y - (avg_mine_dia) / 2):int(mid_obj_y + ((avg_mine_dia) / 2))]

        # test the model
        img_name = PCA.match_image(cor_image)
        print(img_name)
        input()

    elif (key == ord('r')):
        # train the model
        log_man.add_log('modes.training_mode_loop',
                        'INFO', f"fitting PCA model to the dataset")
        PCA.train_model()
        log_man.add_log('modes.training_mode_loop',
                        'INFO', f"done fitting PCA model to the dataset")

        set_man.save_settings()

        return -1

    elif (key == ord('q')):
        set_man.save_settings()
        return -1

    return 0
