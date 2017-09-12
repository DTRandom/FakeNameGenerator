from ..objects.error import Error
from ..objects.language import callMess


def process_start_command(chat, message, u, bot, btns):
    """Process that responds to start command."""
    if not u.setLang():
        u.state('homef')
        cm = callMess(u.setLang().decode('utf-8'), u.state().decode('utf-8'))
        text = cm.messageText()
        cbtext = cm.callbackText()
        btns = cm.callbackData(btns, cbtext)
        return
    u.state('home')
    cm = callMess(u.setLang().decode('utf-8'), u.state().decode('utf-8'))
    text = cm.messageText()
    cbtext = cm.callbackText()
    btns = cm.callbackData(btns, cbtext)
    print(btns)
    chat.send(text, syntax='HTML', attach=btns)
