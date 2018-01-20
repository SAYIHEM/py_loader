# coding=utf-8
from telegramserver import TelegramServer
import logging
import coloredlogs
import atexit


server = None
logger = logging.getLogger("main")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    coloredlogs.install()

    # Start Telegram server
    server = TelegramServer('548165005:AAGUTShuLphcrMwGbhDcfVndQ009zjHuFHk')
    #server.add_handler(CommandHandler("d", download))
    server.start()

@atexit.register
def at_exit():

    if server is not None:
        server.updater.stop()
    else:
        logger.debug("'server' was None!")

    if server.updater.running:
        logger.error("Could not stop telegram server!")
    else:
        logger.info("Telegram server offline.")
