import config
from ..objects.error import Error
from ..objects.mysql import disconnectmysql, connectmysql
# from ..objects.user import r


def process_ridentity_callback(chat, query, bot, u, btns):
    cursor, cnx = connectmysql()
    current = int(u.getRedis('current'))
    if current == 150:
        return
    sqlquery = """
            SELECT gender, title, givenname, surname,
            streetaddress, city, state, statefull, zipcode,
            country, countryfull, birthday FROM fakenames
            WHERE number = {current}
            """.format(current=current)
    cursor.execute(sqlquery)
    current += 1
    u.setRedis('current', current)
    btns[0].callback("🔀 Random Identity", 'ridentity')
    for row in cursor.fetchall():
        text = "<b>Gender</b>: {gender}\n<b>Title</b>: {title}\n" + \
                "<b>Name</b>: {name}\n<b>Surname</b>: {surname}\n" + \
                "<b>Street</b>: {street}\n<b>City</b>: {city}\n" + \
                "<b>State</b>: {state}, {statefull}\n" + \
                "<b>Zip Code</b>: {zip}\n" + \
                "<b>Country</b>: {country}, {countryfull}\n" + \
                "<b>Birthday</b>: {birthday}"
        text = text.format(gender=row[0], title=row[1],
                           name=row[2], surname=row[3],
                           street=row[4], city=row[5],
                           state=row[6], statefull=row[7],
                           zip=row[8], country=row[9],
                           countryfull=row[10], birthday=row[11])
    chat.send(text, attach=btns)
