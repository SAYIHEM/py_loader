from pyloader import Config

__all__ = ["root"]


def root(func):
    def func_wrapper(bot, update):
        id_client = update.message.from_user.id

        if id_client == Config.id_admin:
            return func(bot, update)
        else:
            update.message.reply_text("Permission denied!")

    return func_wrapper