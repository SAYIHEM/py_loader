import time

__all__ = ['Job']


class Job:

    bot = None
    update = None
    id = None

    def __init__(self, bot, update):
        self.bot = bot
        self.update = update
        self.id = time.time()
