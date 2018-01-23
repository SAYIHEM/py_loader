# coding=utf-8
import moviepy.editor as mp
from pathlib import Path
from exceptions.FileNotFoundException import FileNotFoundException
import logging
import os

__all__ = ["Converter"]


class Converter:

    logger = logging.getLogger(__name__)

    file = None

    def __init__(self, file):

        # Check File exists
        if not isinstance(file, Path):
            file = Path(file)
        if not file.is_file():
            self.logger.error("Invalid path: " + str(file))
            raise FileNotFoundException()

        self.file = file

    def to_mp3(self, out="temp/audio.mp3"):

        # Create destination when not existing
        path = Path(os.path.dirname(str(out)))
        if not path.exists():
            path.mkdir(parents=True)

        # TODO: put output to logger
        clip = mp.AudioFileClip(str(self.file))
        clip.write_audiofile(str(out), fps=44100,
                                   nbytes=2,
                                   buffersize=2000,
                                   codec=None,
                                   bitrate='320k',
                                   ffmpeg_params=None,
                                   write_logfile=False,
                                   verbose=True,
                                   progress_bar=True)