from telegram.ext import Updater, CommandHandler, RegexHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

from pyloader.downloading import regex
from pyloader.downloading.download_thread import DownloadThread

from logging import Handler
import logging

import time
import datetime

# Globals

dir_temp = "/home/pi/py_loader/temp"
dir_download = "/home/pi/music/downloads"
my_chat_id = 341971901  # ID of private bot chat

__all__ = ["TelegramServer"]


def error_callback(bot, update, error):

    logger = logging.getLogger("telegramserver.error")

    def log_error(err):
        logger.error(str(err))

    try:
        raise error
    except Unauthorized:
        error = "There was an error: " + str(error)
        log_error(error)
    # remove update.message.chat_id from conversation list
    except BadRequest:
        error = "There was an error: " + str(error)
        log_error(error)
    # handle malformed requests - read more below!
    except TimedOut:
        error = "There was an error: " + str(error)
        log_error(error)
    # handle slow connection problems
    except NetworkError:
        error = "There was an error: " + str(error)
        log_error(error)
    # handle other connection problems
    except ChatMigrated as e:
        error = "There was an error: " + str(error)
        log_error(error)
    # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        error = "There was an error: " + str(error)
        log_error(error)


def regex_download(bot, update):
    logger = logging.getLogger()
    logger.debug("Found RegEx for YouTube link!")

    try:
        # TODO: avoid download video multiple times with "Thread map"
        thread = DownloadThread(args=(update, dir_temp, dir_download,))
        thread.start()
    except Exception as e:
        chat_id = update.message.chat_id
        error = "There was an error: " + str(e)
        bot.send_message(chat_id=chat_id, text=error)


def ping(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="ping")


def reboot(bot, update):
    logger = logging.getLogger(__name__)

    chat_id = update.message.chat_id
    user = update.message.from_user

    logger.info("User: {name} [{id}] initialized reboot.".format(name=user.username, id=user.id))

    timeout = update.message.text.split(" ")[1] # TODO: Fix out of bounds when no time
    if timeout.isdigit():
        timeout = int(timeout)

        msg_time = update.message.date #datetime.datetime.now().time()
        reboot_time = msg_time + datetime.timedelta(seconds=timeout)

        log = "Rebooting at {time}".format(time=reboot_time)
        logger.info(log)

        bot.send_message(chat_id=chat_id, text=log)
        time.sleep(timeout)

    bot.send_message(chat_id=chat_id, text="Reboot now!")

    from pyloader.py_loader import reboot_service
    reboot_service()

    pass


class TelegramServer:

    class OnErrorHandler(Handler): # TODO: make as singleton to send from everywhere

        updater = None

        def emit(self, record):
            self.updater.bot.send_message(chat_id=my_chat_id, text="ping")

        def __init__(self, updater, level=logging.ERROR):
            super().__init__(level)
            self.updater = updater

    logger = logging.getLogger(__name__)

    updater = None

    def __init__(self, token):

        self.updater = Updater(token)
        self._set_handler()

        self.logger.addHandler(self.OnErrorHandler(self.updater))

        self.logger.debug("Initialized Updater with API-Token.")

    # TODO: send audio
    def _set_handler(self):
        self.updater.dispatcher.add_handler(RegexHandler(regex.yt_link, regex_download))
        self.updater.dispatcher.add_error_handler(error_callback)
        self.updater.dispatcher.add_handler(CommandHandler("ping", ping))
        self.updater.dispatcher.add_handler(CommandHandler("reboot", reboot))

        self.logger.debug("Set up handler.")

    def start(self):
        self.logger.info("Started Telegram Bot.")
        self.updater.start_polling()

        self.updater.idle()


    # TODO: Fix function
    def add_handler(self, handler):
        if not isinstance(handler, CommandHandler):
            self.logger.error("Handler was no Telegram.CommandHandler!")
            raise IllegalArgumentException()

        self.updater.stop()

        self.updater.dispatcher.add_handler(handler)
