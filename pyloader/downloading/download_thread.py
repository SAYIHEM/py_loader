import logging
import re
import time
import traceback
from threading import Thread

from pyloader import Config
from pyloader.downloading import Regex, YTLoader

__all__ = ["DownloadThread"]


class DownloadThread(Thread):

    logger = logging.getLogger(__name__)

    queue = None

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super().__init__(group=group, target=target, name=name)

        self.args = args
        self.kwargs = kwargs

        # TODO: Pass parameters better
        self.queue = self.args[0]

    def run(self):
        while True:
            if not self.queue.empty():
                job = self.queue.get()

                self.logger.info('Processing Job: {id} [{count}]'
                                 .format(id=str(job.id),
                                         count=str(self.queue.qsize() + 1)))

                self.__process_download(job)

            # Lower CPU usage
            time.sleep(0.5)

    def __process_download(self, job):

        # Get url from message
        url = job.update.message.text

        # Filter link to find video url
        url = re.findall(Regex.yt_link, url)
        url = ''.join(url[0])  # Concatenate regex groups

        # TODO: implement Save to dircetory
        # genre_dirs = ["Hardstyle", "Rawstyle", "Hardcore", "Frenchcore"]  # TODO: config file with directory shortcuts -> function to add new
        # button_list = [InlineKeyboardButton(s, callback_data=s) for s in genre_dirs]
        # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        # self.bot.send_message(self.update.message.chat_id, "Save track to one of the directories...", reply_markup=reply_markup)

        # Download
        try:
            loader = YTLoader(url)
            loader.download(Config.dir_download)
        except Exception as e:
            error = traceback.format_exc()
            self.logger.critical(error)
            return

        # Finish queue task
        self.queue.task_done()

        # Reply message
        job.update.message.reply_text('Downloaded: \n{}'.format(loader.title))
        self.logger.info("Done converting: " + loader.title)

