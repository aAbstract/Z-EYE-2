import cv2
import utils.log as log_man


# module status
_cam = None


def _init_module():
    global _cam
    log_man.add_log('camera.camera._init_module', 'INFO', 'connecting to usb camera')
    _cam = cv2.VideoCapture(2)
    log_man.add_log('camera.camera._init_module', 'INFO', 'connected to usb camera')


def get_cam():
    return _cam


_init_module()
