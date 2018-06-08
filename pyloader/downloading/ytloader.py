# coding=utf-8
import logging
import re
import youtube_dl
from pathlib import Path
from pyloader import Config

__all__ = ["YTLoader"]


class YTLoader:

    logger = logging.getLogger(__name__)

    url = None
    title = None

    def __init__(self, url):

        self.url = url

        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            self.title = info_dict.get('title', None)

    def download(self, destination="downloads"):

        # Create destination when not existing
        path = Path(destination)
        if not path.exists():
            path.mkdir(parents=True)

        path = Config.dir_download + "/%(title)s.%(ext)s"

        class Log(object):
            logger = logging.getLogger("downloader")

            def info(self, msg):
                self.logger.info(msg)

            def debug(self, msg):
                self.logger.info(msg)

            def warning(self, msg):
                self.logger.info(msg)

            def error(self, msg):
                self.logger.error(msg)

        ydl_opts = {
            'outtmpl': path,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # TODO: LOG!
            #'logger': Log(),
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

        return Path(path)
