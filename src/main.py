import botogram
import config
import time
import redis
from src.objects.user import User
from src.objects.error import Error
from src.updates import commands, callback

bot = botogram.create(config.BOT_TOKEN)

r = redis.StrictRedis(host=config.REDIS_HOST,
                      password=config.REDIS_PASSWORD,
                      db=config.REDIS_DB, port=config.REDIS_PORT)


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
    elif int(u.isAdmin()) == 2 or int(r.get('open')) == 2:
        btns = botogram.Buttons()
        commands.process_start_command(chat, message, u, bot, btns)
    print('--- ' + str(time.time() - start_time) + ' ---' + " /start - " +
          str(message.sender.id))


# Scusate ma il cazzo di codice mi stava facendo bestemmiare 🎉
@bot.callback('porcoddiocane')
def ridentity_callback(chat, query):
    start_time = time.time()
    u = User(query.sender)
    if chat.type == 'private' and int(u.isAdmin()) == 2 or int(r.get('open')) == 2:
        btns = botogram.Buttons()
        callback.process_ridentity_callback(chat, query, bot, u, btns)
    print('--- ' + str(time.time() - start_time) + ' ---' + " ridentity - " +
          str(query.sender.id))


@bot.callback('lang')
def lang_callback(chat, query, data):
    start_time = time.time()
    u = User(query.sender)
    if chat.type == 'private' and int(u.isAdmin()) == 2 or int(r.get('open')) == 2:
        btns = botogram.Buttons()
        callback.process_lang_callback(chat, query, bot, u, btns, data)
    print('--- ' + str(time.time() - start_time) + ' ---' + " lang - " +
          str(query.sender.id))


@bot.callback('home')
def home_callback(chat, query, data):
    start_time = time.time()
    u = User(query.sender)
    if chat.type == 'private' and int(u.isAdmin()) == 2 or int(r.get('open')) == 2:
        btns = botogram.Buttons()
        callback.process_home_callback(chat, query, bot, u, btns, data)
    print('--- ' + str(time.time() - start_time) + ' ---' + " home - " +
          str(query.sender.id))


@bot.callback('settings')
def settings_callback(chat, query, data):
    start_time = time.time()
    u = User(query.sender)
    if chat.type == 'private' and int(u.isAdmin()) == 2 or int(r.get('open')) == 2:
        btns = botogram.Buttons()
        callback.process_settings_callback(chat, query, bot, u, btns, data)
    print('--- ' + str(time.time() - start_time) + ' ---' + " settings@" +
          data + " - " +
          str(query.sender.id))


@bot.callback('info')
def info_callback(chat, query, data):
    start_time = time.time()
    u = User(query.sender)
    if chat.type == 'private' and int(u.isAdmin()) == 2 or int(r.get('open')) == 2:
        btns = botogram.Buttons()
        callback.process_info_callback(chat, query, bot, u, btns, data)
    print('--- ' + str(time.time() - start_time) + ' ---' + " info - " +
          str(query.sender.id))


@bot.callback('open')
def open_callback(chat, query, data):
    start_time = time.time()
    u = User(query.sender)
    if chat.type == 'private' and int(u.isAdmin()) == 2 or int(r.get('open')) == 2:
        btns = botogram.Buttons()
        callback.process_open_callback(chat, query, bot, u, btns, data)
    print('--- ' + str(time.time() - start_time) + ' ---' + " info - " +
          str(query.sender.id))
