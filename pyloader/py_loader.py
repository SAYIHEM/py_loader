# coding=utf-8
import os
from sh import sudo
import logging
from pyloader.config import PyLoaderConfig

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
    os.system("sudo systemctl restart pyloader.service >> "+PyLoaderConfig.dir_err+" 2>> "+PyLoaderConfig.dir_log+" &")


