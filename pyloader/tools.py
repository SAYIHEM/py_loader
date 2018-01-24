from telegram import Message

__all__ = []


def to_arg_array(message):

    if not isinstance(message, Message):
        raise None