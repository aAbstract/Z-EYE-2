import network_client as net_man


def network_read_handler(data: str):
    print(f"read from socket: {data}")


# setup network client
net_man.set_network_read_event_listner(network_read_handler)

while True:
    net_man.network_read_event_trigger()
