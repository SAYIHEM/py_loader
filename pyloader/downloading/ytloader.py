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

        # TODO: Check url
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

    def _best_stream(self, steam_list):
        stream = steam_list[0]
        for s in steam_list:
            rate_stream = int(re.sub("[^0-9]", "", stream.abr))
            rate_s = int(re.sub("[^0-9]", "", s.abr))
            if rate_stream < rate_s:
                stream = s

        return stream

    def _to_path(self, s, max_length=255):
        """Sanitize a string making it safe to use as a filename.

        This function was based off the limitations outlined here:
        https://en.wikipedia.org/wiki/Filename.

        :param str s:
            A string to make safe for use as a file name.
        :param int max_length:
            The maximum filename character length.
        :rtype: str
        :returns:
            A sanitized string.
        """
        # Characters in range 0-31 (0x00-0x1F) are not allowed in ntfs filenames.
        ntfs_chrs = [chr(i) for i in range(0, 31)]
        chrs = [
            '\"', '\#', '\$', '\%', '\'', '\*', '\,', '\.', '\/', '\:',
            '\;', '\<', '\>', '\?', '\\', '\^', '\|', '\~', '\\\\',
        ]

        # TODO: Do not remove 'äöü'
        pattern = '|'.join(ntfs_chrs + chrs)
        regex = re.compile(pattern, re.UNICODE)
        filename = regex.sub('', s)
        return str(filename[:max_length].rsplit(' ', 0)[0])