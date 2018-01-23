# coding=utf-8
from pytube import YouTube
import logging
import re
from pathlib import Path

__all__ = ["YTLoader"]


class YTLoader:

    logger = logging.getLogger(__name__)

    yt = None
    title = None

    def __init__(self, url):

        self.yt = YouTube(url)

        # Remove UTF-8 characters from title
        self.title = self._toPath(self.yt.title)

    def download(self, destination="temp"):

        # Create destination when not existing
        path = Path(destination)
        if not path.exists():
            path.mkdir(parents=True)

        # Select audio stream
        audio_streams = self.yt.streams.filter(only_audio=True).all()
        stream = self._best_stream(audio_streams)
        stream.download(destination, filename=self.title)

        self.logger.debug("List of audio streams: " + str(audio_streams))
        self.logger.debug("Selecting: " + str(stream))

        file = self._toPath(self.title) # TODO remove double '_toPath'
        extension = "." + str(stream.mime_type.split("/")[1])

        return Path(destination, file + extension)

    def _best_stream(self, steam_list):
        stream = steam_list[0]
        for s in steam_list:
            rate_stream = int(re.sub("[^0-9]", "", stream.abr))
            rate_s = int(re.sub("[^0-9]", "", s.abr))
            if rate_stream < rate_s:
                stream = s

        return stream

    def _path(self, s):
        return s.encode('ascii', errors='ignore')

    def _toPath(self, s, max_length=255):
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