# import system modes
import modes.mode_factory as mode_factory

# import event triggers
import event.triggers as triggers

# import event listenrs
import event.listeners as listeners

# setup code
# load system mode
setup_func_ptr, loop_func_ptr = mode_factory.get_sys_mode()
# trigger system mode setup function
setup_func_ptr()

# setup event listenrs
listeners.setup_event_listeners()

# loop code state
exit_code = 0

# loop code
while (True):

    # handle system mode
    exit_code = loop_func_ptr()

    # handle event triggers
    triggers.handle_triggers()

    if exit_code == -1:
        break
