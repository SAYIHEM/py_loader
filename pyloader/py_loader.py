# coding=utf-8

from sh import sudo
import logging

from pyloader.server.telegramserver import TelegramServer

__all__ = ["PyLoader"]

class PyLoader():
    telegram_server = None
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.telegram_server = TelegramServer('548165005:AAGUTShuLphcrMwGbhDcfVndQ009zjHuFHk')

    def run(self):
        # Start Telegram server
        self.telegram_server.start()

    def reboot_service(self, timeout=0):
        # Restart system service
        #os.system("sudo systemctl restart pyloader.service") # TODO: remove hardcoded service name
        err = str(sudo("systemtcl", "restart", "pyloader.service"))
        if err:
            self.logger.error(err)


