import MySQLdb
import config


def disconnectmysql(cursor, cnx):# noqa: D100
    try:
        cursor.close()
        cnx.commit()
        cnx.close()
        return True
    except Exception:
        return False

def connectmysql():# noqa: D100
    cnx = MySQLdb.connect(user=config.MARIADB_USER,
                          password=config.MARIADB_PASSWORD,
                          host=config.MARIADB_HOST,
                          database=config.MARIADB_DATABASE)
    cursor = cnx.cursor()

    return cursor, cnx
