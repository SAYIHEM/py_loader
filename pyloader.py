import atexit
import logging
import sys
from logging import StreamHandler

import coloredlogs

from pyloader import PyLoader
from pyloader.handler import NotifyOnException
from pyloader import Config

telegram_server = None
logger = None

def main():



    logger = logging.getLogger()

    logging.basicConfig(level=logging.CRITICAL,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    #console_handler.setFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.addHandler(console_handler)
    coloredlogs.install()

    py_loader = PyLoader()
    telegram_server = py_loader.telegram_server

    logger.addHandler(NotifyOnException(updater=py_loader.telegram_server.updater,
                                        chat_id=Config.admin_chat_id))
    py_loader.run()


if __name__ == "__main__":
    main()


@atexit.register
def at_exit():

    if telegram_server is not None:
        telegram_server.updater.stop()
    else:
        logger.debug("'server' was None!")

    if telegram_server.updater.running:
        logger.error("Could not stop telegram server!")
    else:
        logger.info("Telegram server offline.")
