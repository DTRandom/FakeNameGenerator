from ..objects.error import Error
from ..objects.language import callMess


def process_start_command(chat, message, u, bot, btns):
    """Process that responds to start command."""
    if not u.setLang():
        u.state('homef')
    else:
        u.state('home')
    cm = callMess(u.setLang(), u.state().decode('utf-8'))
    text = cm.messageText()
    cbtext = cm.callbackText()
    btns = cm.callbackData(btns=btns, text=cbtext)
    chat.send(text, syntax='HTML', attach=btns)
