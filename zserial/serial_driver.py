# note: this driver supports linux only

import re
import serial
import subprocess

import utils.log as log_man

# module config
_baud_rate = 115200

# module state
_serial_port = None


def _init_module():
    global _serial_port

    log_man.add_log('zserial.serial_driver._init_module',
                    'INFO', 'initializing serial driver')

    # exec system call to list all available serial ports
    sub_process = subprocess.Popen(
        'ls /dev/ttyUSB*', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, _ = sub_process.communicate()
    output = stdout.decode()
    port_list = re.findall('(/dev/ttyACM[0-9]+|/dev/ttyUSB[0-9]+)', output)

    if len(port_list) != 0:

        # choose serial uplink
        if len(port_list) == 1:
            port_name = port_list[0]
        else:
            port_name = port_list[1]

        log_man.add_log('zserial.serial_driver._init_module',
                        'DEBUG', f"connecting to serial port {port_name}")

        _serial_port = serial.Serial(port_name, _baud_rate)

        log_man.add_log('zserial.serial_driver._init_module',
                        'DEBUG', f"connected to serial port {port_name}")

        log_man.add_log('zserial.serial_driver._init_module',
                        'INFO', 'finished initializing serial driver')
    else:
        exc_msg = 'no serial port detected'
        log_man.add_log('zserial.serial_driver._init_module', 'ERROR', exc_msg)


def write_raw(msg: str):
    msg_to_write = f"{msg};"
    msg_buffer = msg_to_write.encode()

    if _serial_port != None:
        _serial_port.write(msg_buffer)


def read_raw():
    out = ''

    if not _serial_port.inWaiting():
        return out

    while True:
        if (_serial_port.inWaiting()):
            char = _serial_port.read(1).decode()

            if char == ';':
                break

            if char != '\n' and char != 13:
                out += char

    return out


_init_module()
