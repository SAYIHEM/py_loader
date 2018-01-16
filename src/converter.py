# coding=utf-8
import moviepy.editor as mp
from pathlib import Path
from FileNotFoundException import FileNotFoundException
import logging


class Converter:

    logger = logging.getLogger()

    file = ""

    def __init__(self, file):

        # Check File exists
        path = Path(file)
        if not path.is_file():
            self.logger.error("Invalid path: " + file)
            raise FileNotFoundException()

        self.file = file

    def to_mp3(self, out="temp/audio.mp3"):

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