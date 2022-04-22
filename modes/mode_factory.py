# import system modes
import modes.training_mode as tm
import modes.action_mode as am
import modes.update_model_mode as umm
import modes.no_camera_mode as no_cm


import utils.log as log_man


_modes_map = {
    1: (tm.training_mode_setup, tm.training_mode_loop),
    2: (am.action_mode_setup, am.action_mode_loop),
    3: (umm.update_model_mode_setup, umm.update_model_mode_loop),
    4: (no_cm.no_camera_mode_setup, no_cm.no_camera_mode_loop),
}


def get_sys_mode():
    print('1 -> training mode')
    print('2 -> action mode')
    print('3 -> update model mode')
    print('4 -> no camera mode')
    ans: int = int(input('mode: '))
    if ans not in _modes_map.keys():
        raise Exception('error invalid option')

    log_man.add_log('modes.mode_factory.get_sys_mode',
                    'DEBUG', f"mode {ans} choosen")
    return _modes_map[ans]
