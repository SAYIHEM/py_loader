# coding=utf-8
from telegramserver import TelegramServer
import logging



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Start Telegram server
    server = TelegramServer('548165005:AAGUTShuLphcrMwGbhDcfVndQ009zjHuFHk')
    #server.add_handler(CommandHandler("d", download))
    server.start()