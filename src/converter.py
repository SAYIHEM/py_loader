# coding=utf-8
import moviepy.editor as mp
from pathlib import Path
from src.exceptions.FileNotFoundException import FileNotFoundException
import logging
import os


class Converter:

    logger = logging.getLogger(__name__)

    file = ""

    def __init__(self, file):

        # Check File exists
        path = Path(file)
        if not path.is_file():
            self.logger.error("Invalid path: " + file)
            raise FileNotFoundException()

        self.file = file

    def to_mp3(self, out="temp/audio.mp3"):

        # Create destination when not existing
        path = Path(os.path.dirname(out))
        if not path.exists():
            path.mkdir(parents=True)


        clip = mp.VideoFileClip(self.file)
        clip.audio.write_audiofile(out, fps=44100,
                                   nbytes=2,
                                   buffersize=2000,
                                   codec=None,
                                   bitrate='320k',
                                   ffmpeg_params=None,
                                   write_logfile=False,
                                   verbose=True,
                                   progress_bar=True)