# coding=utf-8
from pytube import YouTube
import logging
import re
import os
from pathlib import Path

class YTLoader:

    logger = logging.getLogger(__name__)

    yt = ""
    title = ""

    def __init__(self, url):

        self.yt = YouTube(url)

        # Remove UTF-8 characters from title
        self.title = self.yt.title.encode('ascii', 'ignore')

    def download(self, destination="temp"):

        # Create destination when not existing
        path = Path(destination)
        if not path.exists():
            path.mkdir(parents=True)

        # TODO: select video
        audio_streams = self.yt.streams.filter(only_audio=True).all()
        stream = self.__best_stream(audio_streams)
        stream.download(destination, filename=self.title)

        self.logger.debug("List of audio streams: " + str(audio_streams))
        self.logger.debug("Selecting: " + str(stream))

        file = self.__toPath(self.title)
        extension = "." + str(stream.mime_type.split("/")[1])

        s = Path(destination, file + extension)
        return Path(destination, file + extension)

    def __best_stream(self, steam_list):
        stream = steam_list[0]
        for s in steam_list:
            rate_stream = int(re.sub("[^0-9]", "", stream.abr))
            rate_s = int(re.sub("[^0-9]", "", s.abr))
            if rate_stream < rate_s:
                stream = s

        return stream

    def __path(self, s):
        return s.encode('ascii', errors='ignore')

    def __toPath(self, s, max_length=255):
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
        pattern = '|'.join(ntfs_chrs + chrs)
        regex = re.compile(pattern, re.UNICODE)
        filename = regex.sub('', s)
        return unicode(filename[:max_length].rsplit(' ', 0)[0])