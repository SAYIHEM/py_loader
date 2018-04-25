import logging
import traceback
from queue import Queue
from threading import Thread
import atexit

from pyloader.downloading import DownloadThread

__all__ = ['ThreadLimiter']


class ThreadLimiter:

    logger = logging.getLogger(__name__)

    threads = []

    __wait_queue = None
    __process_queue = None

    def __init__(self, max_threads):
        self.__wait_queue = Queue()
        self.__process_queue = Queue(maxsize=max_threads)

        Thread(target=(lambda: self.__queue_jobs())).start()

        # Start threads for processing-queue
        try:
            for i in range(self.__process_queue.maxsize):
                self.threads.append(DownloadThread(args=(self.__process_queue,)))
                self.threads[i].setDaemon(True)
                self.threads[i].start()
                pass
        except Exception:
            error = traceback.format_exc()
            self.logger.critical(error)

    def put_job(self, job):
        self.__wait_queue.put(job)

    def __queue_jobs(self):
        while True:
            # Get jobs from waiting-queue
            job = self.__wait_queue.get()
            self.__wait_queue.task_done()

            # Queue jobs to the processing queue
            self.__process_queue.put(job)

            self.logger.info('Queued Job: {id} [{count}]'
                             .format(id=str(job.id),
                                     count=str(self.__wait_queue.qsize() + 1)))

    @atexit.register
    def at_exit(self):
        for t in self.threads:
            t.join()
