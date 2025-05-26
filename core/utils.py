import logging
import socket
import subprocess
from base64 import b64encode
from functools import wraps
from typing import Callable, Any, Optional, Tuple

import psutil
from nacl.public import PrivateKey


def terminal_wrapper(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except subprocess.CalledProcessError:
            logging.exception(f"[-] Fail processing function: {func.__name__}")
            return None
    return wrapper

def get_default_interface() -> Optional[Tuple[str, str]]:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]

    for iface, addresses in psutil.net_if_addrs().items():
        for addr in addresses:
            if addr.family == socket.AF_INET and addr.address == local_ip:
                return local_ip, iface

    raise Exception("[-] Fail get interface!")

def generate_wg_keys() -> Tuple[str, str]:
    private_key = PrivateKey.generate()
    public_key = private_key.public_key
    private_key_b64 = b64encode(private_key._private_key).decode()
    public_key_b64 = b64encode(public_key._public_key).decode()
    return private_key_b64, public_key_b64