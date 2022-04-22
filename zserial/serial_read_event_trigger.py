# import utils.log as log_man
import event.event as event_man
import zserial.serial_api as ser_man


def check_event():

    serial_packet = ser_man.read_data()

    if serial_packet == '':
        return

    # log_man.add_log('zserial.serial_read_event_trigger', 'DEBUG', f"read from serial port: {serial_packet}")

    if serial_packet == '1':
        event_man.post_event('serial_read', 'L')
