# coding=utf-8
from pytube import YouTube
import logging

class YTLoader:

    logger = logging.getLogger(__name__)

    yt = ""
    title = ""

    def __init__(self, url):

        # TODO: check url
        self.yt = YouTube(url)

        # Remove UTF-8 characters from title
        self.title = self.yt.title.encode('ascii', 'ignore')

    def download(self, destination="temp"):

        # Todo: create destination when not existing

        # TODO: select video
        stream = self.yt.streams.first()

        stream.download(destination, filename=self.title)

