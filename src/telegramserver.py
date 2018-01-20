from telegram.ext import Updater, CommandHandler, RegexHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from IllegalArgumentException import IllegalArgumentException
from download_thread import DownloadThread
import logging
import regex

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Globals
dir_temp = "/home/pi/py_loader/temp"
dir_download = "/home/pi/music/downloads"


def error_callback(bot, update, error):

    try:
        raise error
    except Unauthorized:
        error = "There was an error: " + str(error)
    # remove update.message.chat_id from conversation list
    except BadRequest:
        error = "There was an error: " + str(error)
    # handle malformed requests - read more below!
    except TimedOut:
        error = "There was an error: " + str(error)
    # handle slow connection problems
    except NetworkError:
        error = "There was an error: " + str(error)
    # handle other connection problems
    except ChatMigrated as e:
        error = "There was an error: " + str(error)
    # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        error = "There was an error: " + str(error)


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

# TODO: Add 'Show commands button'
class TelegramServer:

    logger = logging.getLogger(__name__)

    updater = None

    def __init__(self, token):

        self.updater = Updater(token)
        self._set_handler()

        self.logger.debug("Initialized Updater with API-Token.")

    # TODO: New handler for: ping, send audio
    def _set_handler(self):
        self.updater.dispatcher.add_handler(RegexHandler(regex.yt_link, regex_download))
        self.updater.dispatcher.add_error_handler(error_callback)
        self.updater.dispatcher.add_handler(CommandHandler("ping", ping))

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