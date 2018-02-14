import datetime
import logging
import threading
import time
import traceback

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import Updater, CommandHandler, RegexHandler, Filters

from pyloader import Config
from pyloader.downloading import DownloadThread
from pyloader.downloading import Regex
from pyloader.server import ArgList
from pyloader.server.user_groups import root

__all__ = ["TelegramServer"]


def error_callback(bot, update, error):
    logger = logging.getLogger("telegramserver.error")

    try:
        raise error
    except Unauthorized as e:
        logger.error(e.message)
    # remove update.message.chat_id from conversation list
    except BadRequest as e:
        logger.error(e.message)
    # handle malformed requests - read more below!
    except TimedOut as e:
        logger.error(e.message)
    # handle slow connection problems
    except NetworkError as e:
        logger.error(e.message)
    # handle other connection problems
    except ChatMigrated as e:
        logger.error(e.message)
    # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError as e:
        logger.error(e.message)


def regex_download(bot, update):
    logger = logging.getLogger(__name__)
    logger.debug("Found regex-pattern for YouTube link!")

    try:
        # TODO: avoid download video multiple times with "Thread map"
        thread = DownloadThread(args=(update,))
        thread.start()
        pass
    except Exception:
        error = traceback.format_exc()
        logger.critical(error)


def ping(bot, update):
    update.message.reply_text("ping") # TODO: ping with millis


@root
def reboot(bot, update):
    logger = logging.getLogger(__name__)

    user = update.message.from_user

    logger.info("User: {name} [{id}] initialized reboot.".format(name=user.username, id=user.id))

    timeout = "no_timeout"
    arglist = ArgList(update.message)
    if arglist[0] is not None:
        timeout = arglist[0]

    def reboot_after_timeout(t):
        time.sleep(t)
        reboot_now()

    def reboot_now():
        update.message.reply_text("Reboot now!")

        from pyloader.py_loader import reboot_service
        reboot_service()

    if timeout.isdigit():
        timeout = int(timeout)

        msg_time = update.message.date #datetime.datetime.now().time()
        reboot_time = msg_time + datetime.timedelta(seconds=timeout)

        log = "Rebooting at {time}".format(time=reboot_time)
        logger.info(log)

        update.message.reply_text(log)

        t = threading.Thread(target=reboot_after_timeout, args=(timeout,))
        t.start()

    else:
        reboot_now()


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
