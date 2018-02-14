# coding=utf-8
import logging
import os

from pyloader import Config
from pyloader.server.telegramserver import TelegramServer

__all__ = ["PyLoader", "reboot_service"]


class PyLoader:
    telegram_server = None
    logger = logging.getLogger(__name__)



    def __init__(self):
        self.telegram_server = TelegramServer(Config.bot_token)

    def run(self):
        # Start Telegram server
        self.telegram_server.start()


def reboot_service():
    logger = logging.getLogger(__name__)

    # Restart system service
    os.system("sudo systemctl restart pyloader.service >> "+Config.dir_err+" 2>> "+Config.dir_log+" &")


