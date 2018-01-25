import logging
import traceback
from pathlib import Path
from threading import Thread

from pyloader.downloading import Converter, YTLoader

__all__ = ["DownloadThread"]


class DownloadThread(Thread):

    logger = logging.getLogger(__name__)

    update = None

    dir_temp = None
    dir_download = None

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(DownloadThread, self).__init__(group=group, target=target, name=name)

        self.args = args
        self.kwargs = kwargs

        # TODO: Pass parameters better
        self.update = self.args[0]
        self.dir_temp = self.args[1]
        self.dir_download = self.args[2]

    def run(self):
        self.logger.info("New Thread for downloading and converting.")

        # Get url from message
        url = self.update.message.text

        # Download
        loader = None
        audio = None
        try:
            loader = YTLoader(url)
            audio = loader.download(self.dir_temp)
        except Exception as e:
            error = traceback.format_exc()
            self.logger.critical(error)
            return

        self.logger.debug("Converting: " + str(audio))

        file_out = Path(self.dir_download, loader.title + ".mp3")

        # Convert
        try:
            converter = Converter(audio)
            converter.to_mp3(file_out)
        except Exception as e:
            error = traceback.format_exc()
            self.logger.critical(error)

        # Delete video file
        try:
            audio.unlink()
        except Exception as e:
            self.logger.critical("Cannot delete File: " + str(e))

        # Reply message
        self.update.message.reply_text('Downloaded: \n{}'.format(loader.title))
        self.logger.info("Done converting: " + loader.title)
