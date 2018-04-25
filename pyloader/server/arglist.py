from telegram import Message

__all__ = ["ArgList"]


class ArgList:

    args = None
    text = None

    def __init__(self, message):

        if isinstance(message, str) or isinstance(message, Message):
            self.text = message.text

        self.args = self.text.split()[1:]


    def arg1(self):
        if len(self.args) == 1:
            return self.args[0]
        else:
            return None

    def arg2(self):
        if len(self.args) == 2:
            return self.args[1]
        else:
            return None

    def arg3(self):
        if len(self.args) == 3:
            return self.args[2]
        else:
            return None

    def __getitem__(self, key):
        if key < len(self.args):
            return self.args[key]
        else:
            return None

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError
