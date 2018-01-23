from pyloader.py_loader import PyLoader
import logging
from logging import StreamHandler
import sys
import coloredlogs
import atexit


def main():

    global telegram_server
    global logger
    logger = logging.getLogger(__name__)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.addHandler(console_handler)
    coloredlogs.install()

    py_loader = PyLoader()
    py_loader.run()
    telegram_server = py_loader.telegram_server


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
