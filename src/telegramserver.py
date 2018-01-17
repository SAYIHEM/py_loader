from telegram.ext import Updater, CommandHandler, RegexHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from src.exceptions.IllegalArgumentException import IllegalArgumentException
from download_thread import DownloadThread
import logging
import regex

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Globals
dir_temp = "temp"
dir_download = "/home/tomg/projects/py_loader/downloads"

def download(bot, update):
    logger = logging.getLogger()

    try:
        #TODO: avoid download video multiple times with "Thread map"
        thread = DownloadThread(args=(update, dir_temp, dir_download,))
        thread.start()
    except Exception as e:
        chat_id = update.message.chat_id
        error = "There was an error: " + str(e)
        bot.send_message(chat_id=chat_id, text=error)


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

    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="yield")

class TelegramServer:

    logger = logging.getLogger(__name__)

    updater = ""

    def __init__(self, token):

        self.updater = Updater(token)
        self._set_handler()

        self.logger.debug("Initialized Updater with API-Token.")

    def _set_handler(self):
        self.updater.dispatcher.add_handler(CommandHandler("d", download))

        self.updater.dispatcher.add_handler(RegexHandler(regex.yt_link, regex_download))
        self.updater.dispatcher.add_error_handler(error_callback)

        self.logger.debug("Set up handler.")

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

        self.logger.info("Started Telegram Bot.")




    def add_handler(self, handler):
        if not isinstance(handler, CommandHandler):
            self.logger.error("Handler was no Telegram.CommandHandler!")
            raise IllegalArgumentException()

        self.updater.stop()

        self.updater.dispatcher.add_handler(handler)

        self.updater.start_polling()
        self.updater.idle()