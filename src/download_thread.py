from threading import Thread
from ytloader import YTLoader
from converter import Converter
from pathlib import Path
import os
from os.path import basename
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DownloadThread(Thread):

    logger = logging.getLogger(__name__)

    update = ""

    dir_temp = ""
    dir_download = ""

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(DownloadThread, self).__init__(group=group, target=target, name=name, verbose=verbose)

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

        loader = YTLoader(url)
        loader.download(self.dir_temp)

        # Get downloaded video
        video = ""
        for file in Path(self.dir_temp).iterdir():
            path = str(file.absolute())
            filename = basename(path)
            title = os.path.splitext(filename)[0]

            if title == loader.title:
                video = filename

        self.logger.debug("Converting: " + video)

        file_in = self.dir_temp + "/" + video
        file_out = self.dir_download + "/" + loader.title + ".mp3"

        # Convert
        converter = Converter(file_in)
        converter.to_mp3(file_out)

        # Reply message
        self.update.message.reply_text('Downloaded: {}'.format(loader.title))
        self.logger.info("Done converting: " + loader.title)
