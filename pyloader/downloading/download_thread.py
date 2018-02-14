import logging
import traceback
from threading import Thread

from pyloader import Config
from pyloader.downloading import Converter, YTLoader

__all__ = ["DownloadThread"]


class DownloadThread(Thread):

    logger = logging.getLogger(__name__)

    update = None

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(DownloadThread, self).__init__(group=group, target=target, name=name)

        self.args = args
        self.kwargs = kwargs

        # TODO: Pass parameters better
        self.update = self.args[0]

    def run(self):
        self.logger.info("New Thread for downloading and converting.")

        # Get url from message
        url = self.update.message.text

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
