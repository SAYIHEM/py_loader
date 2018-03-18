import logging
import traceback
from threading import Thread

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pyloader import Config
from pyloader.downloading import Converter, YTLoader
from pyloader.tools import build_menu

__all__ = ["DownloadThread"]


class DownloadThread(Thread):

    logger = logging.getLogger(__name__)

    bot = None
    update = None

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(DownloadThread, self).__init__(group=group, target=target, name=name)

        self.args = args
        self.kwargs = kwargs

        # TODO: Pass parameters better
        self.bot = self.args[0]
        self.update = self.args[1]

    def run(self):
        self.logger.info("New Thread for downloading and converting.")

        # Get url from message
        url = self.update.message.text

        genre_dirs = ["Hardstyle", "Rawstyle", "Hardcore", "Frenchcore"]  # TODO: config file with directory shortcuts -> function to add new
        button_list = [InlineKeyboardButton(s, callback_data=s) for s in genre_dirs]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        self.bot.send_message(self.update.message.chat_id, "Save track to one of the directories...", reply_markup=reply_markup)

        # Download
        try:
            loader = YTLoader(url)
            loader.download(Config.dir_download)
        except Exception as e:
            error = traceback.format_exc()
            self.logger.critical(error)
            return

        # Reply message
        self.update.message.reply_text('Downloaded: \n{}'.format(loader.title))
        self.logger.info("Done converting: " + loader.title)
