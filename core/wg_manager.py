from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from django.conf import settings

from core.constants import WG_CONF
from core.utils import generate_wg_keys, terminal_wrapper
from wireguard.models import WgClient


logger = logging.getLogger("wg-manager")

class Wireguard:
    _private_key: str = None
    _pub_key: str = None
    _path: Path = Path(settings.WG_DIR)
    _name: str = None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._name = "wg-quick@wg1.service"
        self._init()

    def _init(self) -> None:
        private_key_path = self._path / "privatekey"
        public_key_path = self._path / "publickey"
        if private_key_path.exists() and public_key_path:
            with open(private_key_path, "r", encoding="utf-8") as file:
                self._private_key = file.read().strip()
            with open(public_key_path, "r", encoding="utf-8") as file:
                self._pub_key = file.read().strip()
        else:
            self._save_keys()

    def write_config(self) -> None:
        clients_conf = WgClient.get_client_peers()
        conf_data = WG_CONF.format(self._private_key,
                                   settings.WG_PORT,
                                   settings.SERVER_INTERFACE,
                                   settings.SERVER_INTERFACE, clients_conf)
        with open(self._path / "wg1.conf", "w", encoding="utf-8") as file:
            file.write(conf_data)
        logger.info("[+] Saved wireguard config")
        self.reload()

    def _save_keys(self) -> None:
        self._private_key, self._pub_key = generate_wg_keys()
        with open(self._path / "privatekey", "w", encoding="utf-8") as file:
            file.write(self._private_key)
        with open(self._path / "publickey", "w", encoding="utf-8") as file:
            file.write(self._pub_key)
        logger.info("[+] Saved server keys")

    @terminal_wrapper
    def restart(self) -> None:
        subprocess.run(["sudo", "/bin/systemctl", "restart", self._name], check=True)
        logger.info(f"[+] Service {self._name} was restarted")

    @terminal_wrapper
    def start(self) -> None:
        subprocess.run(["sudo", "/bin/systemctl", "start", self._name], check=True)
        logger.info(f"[+] Service {self._name} was started")

    @terminal_wrapper
    def stop(self) -> None:
        subprocess.run(["sudo", "/bin/systemctl", "stop", self._name], check=True)
        logger.info(f"[+] Service {self._name} was stopped")

    @terminal_wrapper
    def reload(self) -> None:
        subprocess.run(["sudo", "/bin/systemctl", "reload", self._name], check=True)
        logger.info(f"[+] Service {self._name} was reloaded")

    @property
    def public_key(self) -> str:
        return self._pub_key
