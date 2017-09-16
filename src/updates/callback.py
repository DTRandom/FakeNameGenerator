import config
from ..objects.language import callMess
from ..objects.error import Error
from ..objects.language import callMess
from ..objects.mysql import disconnectmysql, connectmysql
# from ..objects.user import r


def process_ridentity_callback(chat, query, bot, u, btns, data):
    """
    Get a new fake identity.

    Identities are given based on selected language.
    """
    cm = callMess(u.setLang().decode('utf-8'), u.state().decode('utf-8'))
    # print(data)
    u.state('ridentity')
    cursor, cnx = connectmysql()
    current = int(u.getRedis('current'))
    maxquery = """
               SELECT MAX(number) FROM fakenames{lang}
               """.format(lang=data)
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
                       lang=data)
    cursor.execute(sqlquery)
    current += 1
    u.setRedis('current', current)
    cbtext = cm.callbackText()
    btns = cm.callbackData(btns, cbtext, u.getRedis('lang').decode('utf-8'))
    text = cm.messageText()
    for row in cursor.fetchall():
        text = text.format(gender=row[0], title=row[1],
                           name=row[2], surname=row[3],
                           street=row[4], city=row[5],
                           state=row[6], statefull=row[7],
                           zip=row[8], country=row[9],
                           countryfull=row[10], birthday=row[11])
    chat.send(text, syntax='HTML', attach=btns)


def process_setlang_callback(chat, query, bot, u, btns, data):
    u.setLang('data')
