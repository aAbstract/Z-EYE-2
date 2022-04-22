# note this driver create non-blocking TCP socket

import utils.log as log_man

import socket


# module config
_host = '127.0.0.1'
_port = 65432

# module state
_socket_server = None
_socket_client = None


def _init_module():
    global _socket_server
    global _socket_client

    log_man.add_log('networking.network_driver._init_module',
                    'INFO', 'initlizing networking driver')
    log_man.add_log('networking.network_driver._init_module',
                    'DEBUG', f"starting tcp server at {_host}:{_port}")

    # start TCP server
    _socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket_server.bind((_host, _port))
    _socket_server.listen()

    # accept TCP client
    _socket_client, client_addr = _socket_server.accept()
    _socket_client.setblocking(0)

    # client connected routine
    log_man.add_log('networking.network_driver._init_module',
                    'DEBUG', f"client {client_addr} connected")

    log_man.add_log('networking.network_driver._init_module',
                    'INFO', 'finished initlizing networking driver')


def write_raw(msg: str):
    msg_to_write = f"{msg};"
    msg_buffer = msg_to_write.encode()

    if _socket_client != None:
        _socket_client.send(msg_buffer)


def read_raw():
    out = ''

    init_char = -1
    try:
        init_char = _socket_client.recv(1).decode()
    
    except BlockingIOError:
            pass

    if init_char == -1:
        return out

    out += init_char
    
    while True:
        try:
            char = _socket_client.recv(1).decode()
            
            if char == ';':
                break

            out += char

        # non blocking socket read
        except BlockingIOError:
            pass

    return out


_init_module()
