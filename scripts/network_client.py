import socket


# module config
_host = '127.0.0.1'
_port = 65432

# moduel state
_client_socket = None
_network_read_event_listner = None


def set_network_read_event_listner(func):
    ''' add listner function to the network read event '''

    global _network_read_event_listner

    _network_read_event_listner = func


def network_read_event_trigger():

    # if network read event listenr is none then do nothing
    if _network_read_event_listner == None:
        return

    packet = None

    try:
        packet = _client_socket.recv(1).decode()
        _client_socket.send(f"GET: {packet}".encode())
        _network_read_event_listner(packet)

    # non blocking socket read
    except BlockingIOError:
        pass

    return packet


def _init_module():
    global _client_socket

    # setup TCP client socket
    _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _client_socket.connect((_host, _port))
    _client_socket.setblocking(0)


_init_module()
