import logging
from logging import Handler
from pyloader import Config

__all__ = ["NotifyOnException"]


class NotifyOnException(Handler):

    updater = None
    chat_id = None

    def emit(self, record):
        self.updater.bot.send_message(Config.id_admin, "There was an error:\n" + record.msg)

    def __init__(self, updater, chat_id, level=logging.CRITICAL):
        super().__init__(level)
        self.updater = updater
        self.chat_id = chat_id