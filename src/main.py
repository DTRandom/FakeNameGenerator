import botogram
import config
import json
import time
from src.objects.user import User
from src.objects.error import Error
from src.updates import commands, callback
bot = botogram.create(config.BOT_TOKEN)


@bot.command('start')
def start_command(chat, message):
    """Default start command."""
    start_time = time.time()
    u = User(message.sender)
    if chat.type != 'private':
        e = Error(chat, bot, message.sender)
        e.sendError('noprivate')
    elif int(u.isAdmin()) == 2000:
        e = Error(chat, bot, message.sender)
        e.sendError('norights')
        u.isAdmin(1)
    elif int(u.isAdmin()) == 2:
        btns = botogram.Buttons()
        commands.process_start_command(chat, message, u, bot, btns)
    print('--- ' + str(time.time() - start_time) + ' ---' + " /start - " +
          str(message.sender.id))


@bot.callback('ridentity')
def ridentity_callback(chat, query):
    start_time = time.time()
    u = User(query.sender)
    if chat.type == 'private' and chat.id == config.ADMIN:
        btns = botogram.Buttons()
        callback.process_ridentity_callback(chat, query, bot, u, btns)
    print('--- ' + str(time.time() - start_time) + ' ---' + " ridentity - " +
          str(query.sender.id))
