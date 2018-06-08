from telegram import Message

__all__ = ['to_arg_array', 'build_menu']


def to_arg_array(message):

    if not isinstance(message, Message):
        raise None


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu