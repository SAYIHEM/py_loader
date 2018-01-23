import datetime
import logging
import threading
import time
import traceback

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import Updater, CommandHandler, RegexHandler

from pyloader.config import PyLoaderConfig
from pyloader.downloading import DownloadThread
from pyloader.downloading import Regex

__all__ = ["TelegramServer"]


def error_callback(bot, update, error):

    logger = logging.getLogger("telegramserver.error")

    try:
        raise error
    except Unauthorized:
        error = traceback.format_exc()
        logger.error(error)
    # remove update.message.chat_id from conversation list
    except BadRequest:
        error = traceback.format_exc()
        logger.error(error)
    # handle malformed requests - read more below!
    except TimedOut:
        error = traceback.format_exc()
        logger.error(error)
    # handle slow connection problems
    except NetworkError:
        error = traceback.format_exc()
        logger.error(error)
    # handle other connection problems
    except ChatMigrated as e:
        error = traceback.format_exc()
        logger.error(error)
    # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        error = traceback.format_exc()
        logger.error(error)


def regex_download(bot, update):
    logger = logging.getLogger()
    logger.debug("Found regex-pattern for YouTube link!")

    try:
        # TODO: avoid download video multiple times with "Thread map"
        thread = DownloadThread(args=(update, PyLoaderConfig.dir_temp, PyLoaderConfig.dir_download,))
        thread.start()
    except Exception as e:
        error = traceback.format_exc()
        logger.error(error)


def ping(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="ping")

def reboot(bot, update):
    logger = logging.getLogger(__name__)

    chat_id = update.message.chat_id
    user = update.message.from_user

    logger.info("User: {name} [{id}] initialized reboot.".format(name=user.username, id=user.id))

    timeout = update.message.text.split(" ")[1] # TODO: Fix out of bounds when no time -> function to make list of args
    if timeout.isdigit():
        timeout = int(timeout)

        msg_time = update.message.date #datetime.datetime.now().time()
        reboot_time = msg_time + datetime.timedelta(seconds=timeout)

        log = "Rebooting at {time}".format(time=reboot_time)
        logger.info(log)

        bot.send_message(chat_id=chat_id, text=log)

        def reboot_after_timeout(t):
            print(t)
            from pyloader.py_loader import reboot_service
            time.sleep(t)

            bot.send_message(chat_id=chat_id, text="Reboot now!")
            reboot_service()

        t = threading.Thread(target=reboot_after_timeout, args=(timeout,))
        t.start()


class TelegramServer:

    logger = logging.getLogger(__name__)

    updater = None

    def __init__(self, token):
        self.updater = Updater(token)
        self._set_handler()

        # Add error handler to root logger
        #logging.getLogger().addHandler(self.OnErrorHandler(self.updater))

        self.logger.debug("Initialized Updater with API-Token.")

    # TODO: send audio
    def _set_handler(self):
        self.updater.dispatcher.add_handler(RegexHandler(Regex.yt_link, regex_download))
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
            self.logger.error("Handler was no Telegram.CommandHandler!\n" + handler)

        self.updater.stop()

        self.updater.dispatcher.add_handler(handler)
