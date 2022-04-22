import numpy as np


import settings.settings as set_man


def is_obj_in_middle(frame):
    bth = 30  # black threshold
    tr = .1  # tolerance ratio
    frame_size = set_man.get_settings('frame_size')
    center = int(frame_size / 2)
    mid_avg = np.sum(frame[center - 1:center + 2, center - 1:center + 2]) / 9
    if (mid_avg < bth + bth * tr):
        return True
    else:
        return False
