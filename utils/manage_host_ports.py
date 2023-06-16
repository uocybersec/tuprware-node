import psutil
from random import randint

MIN_PORT = 1024
MAX_PORT = 65535

def is_port_in_use(port: int) -> bool:
    for conn in psutil.net_connections(): # check connections on ports over TCP and UDP for both IPv4 and IPv6
        if conn.laddr.port == port:
            return True
    return False

def get_host_port() -> int: # returns a random available host port
    while True:
        port = randint(MIN_PORT, MAX_PORT)
        if not is_port_in_use(port):
            return port
    