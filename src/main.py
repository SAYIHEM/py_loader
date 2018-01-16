# coding=utf-8
from ytloader import YTLoader
from converter import Converter
from telegramserver import TelegramServer
from telegram.ext import CommandHandler
from threading import Thread
import logging

class ServerThread(Thread):

    server = ""

    def __init__(self, telegram_server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        server.start()


def start_server(server):
    server.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Start Telegram server
    server = TelegramServer('548165005:AAGUTShuLphcrMwGbhDcfVndQ009zjHuFHk')
    #server.add_handler(CommandHandler("d", download))
    server.start()

    #thread = ServerThread(server)
    #thread.start()
    #thread.add_handler(CommandHandler("d", download))
