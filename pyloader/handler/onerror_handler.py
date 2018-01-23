import logging
from logging import Handler

__all__ = ["OnErrorHandler"]


class OnErrorHandler(Handler):  # TODO: make as singleton to send from everywhere

    updater = None
    chat_id = None

    def emit(self, record):

        err = "There was an error:\n" + record.msg
        self.updater.bot.send_message(chat_id=self.chat_id, text=err)

    def __init__(self, updater, chat_id, level=logging.ERROR):
        super().__init__(level)
        self.updater = updater
        self.chat_id = chat_id