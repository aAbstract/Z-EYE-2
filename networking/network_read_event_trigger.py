import networking.network_api as net_man


def check_event():

    data = net_man.read_raw()

    if data == '':
        return

    print(f"READ: {data}")
    net_man.write_raw(f"GET: {data}")
