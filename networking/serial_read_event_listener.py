import utils.log as log_man
import event.event as event_man
import networking.network_api as net_man


def _serial_read_evnet_handler(network_signal: str):
    net_man.write_raw(network_signal)


def setup_serial_read_event_listener():
    log_man.add_log('networking.serial_read_evnet_handler',
                    'INFO', 'adding serial_read_evnet_handler event listner')

    event_man.subscribe('serial_read', _serial_read_evnet_handler)

    log_man.add_log('networking.serial_read_evnet_handler',
                    'INFO', 'finished adding serial_read_evnet_handler event listner')
