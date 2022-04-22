# import listeners
import networking.serial_read_event_listener as serial_read_event_listener

# event listeners list
_event_listeners_list = [
    serial_read_event_listener.setup_serial_read_event_listener
]


def setup_event_listeners():
    ''' init system event listeners '''

    for event_setup_func in _event_listeners_list:
        event_setup_func()
