import networking.network_driver as net_driver


def write_raw(data: str):
    net_driver.write_raw(data)


def read_raw():
    return net_driver.read_raw()
