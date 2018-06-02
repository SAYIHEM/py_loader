from datetime import datetime
import logging
import threading
import time

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import Updater, CommandHandler, RegexHandler, Filters, CallbackQueryHandler

from pyloader import Config
from pyloader.downloading import Regex, ThreadLimiter, Job
from pyloader.server import ArgList
from pyloader.server.user_groups import root
from pyloader.tools import build_menu

__all__ = ["TelegramServer"]





# Threadlimiter instance
threadlimiter = ThreadLimiter(max_threads=Config.max_threads)



def test(bot, update):

    button_list = [
        InlineKeyboardButton("col1", callback_data="B1"),
        InlineKeyboardButton("col2", callback_data="B2"),
        InlineKeyboardButton("row 2", callback_data="B3")
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.send_message(Config.admin_chat_id, "Save track to...", reply_markup=reply_markup)


def call(bot, update):
    bool = bot.answer_callback_query(update.callback_query.id, "TEST", "")


class TelegramServer:

    logger = logging.getLogger(__name__)

    updater = None

    def __init__(self, token):
        self.updater = Updater(token)
        self.__set_handler()

        self.logger.debug("Initialized Updater with API-Token.")

    def start(self):
        self.logger.info("Started Telegram Bot.")
        self.updater.start_polling()

        self.updater.idle()

    # TODO: send audio
    def __set_handler(self):
        self.updater.dispatcher.add_handler(RegexHandler(Regex.yt_link, self.__regex_download))
        self.updater.dispatcher.add_handler(CommandHandler("ping", self.__ping))
        self.updater.dispatcher.add_handler(CommandHandler("reboot", self.__reboot))

        self.updater.dispatcher.add_error_handler(self.__error_callback)

        # self.updater.dispatcher.add_handler(CommandHandler("test", test))
        # self.updater.dispatcher.add_handler(CallbackQueryHandler(call))

        self.logger.debug("Set up handler.")

    @staticmethod
    def __regex_download(bot: telegram.bot, update: telegram.Update):
        logger = logging.getLogger(__name__)
        logger.debug("Found regex-pattern for YouTube link!")

        threadlimiter.put_job(Job(bot, update))

    @staticmethod
    def __ping(bot: telegram.bot, update: telegram.Update):
        millis = ((datetime.now() - update.message.date) / 10000).microseconds
        update.message.reply_text("ping {ping}ms".format(ping=millis))  # Answer with milliseconds

    @staticmethod
    @root
    def __reboot(bot: telegram.bot, update: telegram.Update):
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

            msg_time = update.message.date  # datetime.datetime.now().time()
            reboot_time = msg_time + datetime.timedelta(seconds=timeout)

            log = "Rebooting at {time}".format(time=reboot_time)
            logger.info(log)

            update.message.reply_text(log)

            t = threading.Thread(target=reboot_after_timeout, args=(timeout,))
            t.start()

        else:
            reboot_now()

    @staticmethod
    def __error_callback(bot: telegram.bot, update: telegram.Update, error):
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
