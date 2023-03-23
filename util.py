import socket
import random

PORT = '5000'
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        IP = '192.168.0.4'
        # # doesn't even have to be reachable
        # s.connect(('10.254.254.254', 1))
        # IP = s.getsockname()[0]
    except Exception:
        IP = '192.168.0.4'
        #IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_nonce(length=8):
		"""Generate pseudorandom number."""
		return int(''.join([str(random.randint(0, 9)) for i in range(length)]))
