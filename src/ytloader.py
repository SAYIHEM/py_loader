# coding=utf-8
from pytube import YouTube
import logging
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
        stream = self.yt.streams.first()

        stream.download(destination, filename=self.title)

