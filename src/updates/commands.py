import config


def process_start_command(chat, message, u, bot, btns):
    """Process that responds to start command."""
    u.state('home')
    btns[0].callback("🔀 Random Identity", 'ridentity', u.getRedis('lang').decode('utf-8'))
    btns[0].callback("⚙️ Settings", 'settings')
    text = "Click the button below to get a <b>Random Identity</b>"
    chat.send(text, syntax='HTML', attach=btns)
