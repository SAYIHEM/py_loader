import logging
import traceback
from queue import Queue
import atexit

from pyloader.downloading import DownloadThread

__all__ = ['ThreadLimiter']


class ThreadLimiter:

    logger = logging.getLogger(__name__)

    threads = []

    __job_queue = None

    def __init__(self, max_threads):
        self.__job_queue = Queue()

        # Start threads for job-queue
        try:
            for i in range(max_threads):
                self.threads.append(DownloadThread(args=(self.__job_queue,)))
                self.threads[i].setDaemon(True)
                self.threads[i].start()
                pass
        except Exception:
            error = traceback.format_exc()
            self.logger.critical(error)

        # Register atExit function
        atexit.register(self.__at_exit)

    def put_job(self, job):
        self.__job_queue.put(job)

    def __at_exit(self):
        for t in self.threads:
            t.join()
