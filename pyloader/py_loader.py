# coding=utf-8
import os
from sh import sudo
import logging

from pyloader.server.telegramserver import TelegramServer

__all__ = ["PyLoader", "reboot_service"]


class PyLoader:
    telegram_server = None
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.telegram_server = TelegramServer('548165005:AAGUTShuLphcrMwGbhDcfVndQ009zjHuFHk')

    def run(self):
        # Start Telegram server
        self.telegram_server.start()


def reboot_service(timeout=0):
    logger = logging.getLogger(__name__)

    # Restart system service
    os.system("sudo systemctl restart pyloader.service >> /home/pi/logs/py_loader.err 2>> /home/pi/logs/py_loader.log &")
    # TODO: remove hardcoded paths

    #err = str(sudo("/bin/systemctl", "restart", "pyloader.service", ">>", "/home/pi/logs/e.err", "2>>", "/home/pi/logs/l.err"))
    #if err:
    #    logger.error(err)


