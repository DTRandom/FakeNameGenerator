import config
from ..objects.language import callMess
from ..objects.error import Error
from ..objects.language import callMess
from ..objects.mysql import disconnectmysql, connectmysql
import redis
# from ..objects.user import r

r = redis.StrictRedis(host=config.REDIS_HOST,
                      password=config.REDIS_PASSWORD,
                      db=config.REDIS_DB, port=config.REDIS_PORT)


def process_ridentity_callback(chat, query, bot, u, btns):
    """
    Get a new fake identity.

    Identities are given based on selected language.
    """
    u.state('ridentity')
    cm = callMess(u.setLang(), u.state().decode('utf-8'))
    # print(data)
    cursor, cnx = connectmysql()
    current = int(u.getRedis('current'))
    maxquery = """
               SELECT MAX(number) FROM fakenames{lang}
               """.format(lang=u.setLang().decode('utf-8'))
    cursor.execute(maxquery)
    for row in cursor.fetchall():
        maxvalue = row[0]
    if current == maxvalue:
        current = 1
    sqlquery = """
            SELECT gender, title, givenname, surname,
            streetaddress, city, state, statefull, zipcode,
            country, countryfull, birthday FROM fakenames{lang}
            WHERE number = {current}
            """.format(current=current,
                       lang=u.setLang().decode('utf-8'))
    cursor.execute(sqlquery)
    current += 1
    u.setRedis('current', current)
    cbtext = cm.callbackText()
    btns = cm.callbackData(btns, cbtext)
    text = cm.messageText()
    query.notify(cm.notifyData())
    for row in cursor.fetchall():
        text = text.format(gender=row[0], title=row[1],
                           name=row[2], surname=row[3],
                           street=row[4], city=row[5],
                           state=row[6], statefull=row[7],
                           zip=row[8], country=row[9],
                           countryfull=row[10], birthday=row[11])
    query.message.edit(text, syntax='HTML', attach=btns)


def process_lang_callback(chat, query, bot, u, btns, data):
    """Set the BOT language when started for the first time."""
    u.setLang(data)
    u.state('homev')
    cm = callMess(u.setLang(), u.state().decode('utf-8'))
    text = cm.messageText()
    btnstext = cm.callbackText()
    btns = cm.callbackData(btns, btnstext)
    query.notify(cm.notifyData())
    query.message.edit(text, attach=btns)


def process_home_callback(chat, query, bot, u, btns, data):
    """Same as /start command but it's a callback :P."""
    if not u.setLang():
        u.state('homef')
    else:
        u.state('home')
    cm = callMess(u.setLang(), u.state().decode('utf-8'))
    text = cm.messageText()
    cbtext = cm.callbackText()
    btns = cm.callbackData(btns=btns, text=cbtext)
    query.notify(cm.notifyData())
    query.message.edit(text, syntax='HTML', attach=btns)


def process_settings_callback(chat, query, bot, u, btns, data):
    """Config page for the BOT."""
    if data == 'main':
        if query.sender.id != config.ADMIN:
            u.state('settings')
        else:
            u.state('settings@a')
    elif data == 'language':
        u.state('settings@language')
    elif data == 'open':
        u.state('settings@o')
    cm = callMess(u.setLang(), u.state().decode('utf-8'))
    text = cm.messageText()
    cbtext = cm.callbackText()
    btns = cm.callbackData(btns, cbtext)
    query.notify(cm.notifyData())
    query.message.edit(text, syntax='HTML', attach=btns)


def process_open_callback(chat, query, bot, u, btns, data):
    """Set the BOT language when started for the first time."""
    r.set('open', data)
    u.state('homev')
    cm = callMess(u.setLang(), u.state().decode('utf-8'))
    text = cm.messageText()
    btnstext = cm.callbackText()
    btns = cm.callbackData(btns, btnstext)
    query.notify(cm.notifyData())
    query.message.edit(text, attach=btns)


def process_info_callback(chat, query, bot, u, btns, data):
    """Get various infos."""
    u.state('info')
    cm = callMess(u.setLang(), u.state().decode('utf-8'))
    text = cm.messageText()
    btnstext = cm.callbackText()
    query.notify(cm.notifyData())
    btns = cm.callbackData(btns, btnstext)
    query.message.edit(text, attach=btns)
