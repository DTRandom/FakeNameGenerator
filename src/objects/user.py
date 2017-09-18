from datetime import datetime as dt

import redis


import config

r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT,
                      db=config.REDIS_DB, password=config.REDIS_PASSWORD)


class User:
    """User base object."""

    def __init__(self, user):
        """
        Create an user object.
        :param user: Telegram's user object.
        """
        try:
            self.id = user.id
            self.rhash = 'user:' + str(user.id)
            if not self.isAdmin():
                r.hset(self.rhash, 'admin', 2000)
            if r.hget(self.rhash, 'id') != user.id:
                r.hset(self.rhash, 'id', user.id)
            if r.hget(self.rhash, 'username') != user.username:
                r.hset(self.rhash, 'username', user.username)
            r.hset(self.rhash, 'last_update', dt.now())
            if not self.state():
                r.hset(self.rhash, 'state', 'home')
            r.hset(self.rhash, "active", True)
            if not self.isMaster():
                r.hset(self.rhash, 'master', 0)
        except AttributeError:
            self.id = user
            self.rhash = 'user:' + str(user)
            if not self.isAdmin():
                self.isAdmin(2000)
            if r.hget(self.rhash, 'id') != user:
                r.hset(self.rhash, 'id', user)
            r.hset(self.rhash, 'last_update', dt.now())
            if not self.state():
                r.hset(self.rhash, 'state', 'home')
            r.hset(self.rhash, "active", True)
            if not self.isMaster():
                self.isMaster(0)

    def state(self, new_state=None):
        """
        Get current user state or set a new user state
        :param new_state: new state for the user
        :return: state
        """
        if not new_state:
            return r.hget(self.rhash, 'state')

        r.hset(self.rhash, 'state', new_state)
        return True

    def setRedis(self, key, value):
        """
        Set a redis value
        :param key: redis key
        :param value: redis value
        :return: value
        """
        return r.hset(self.rhash, key, value)

    def getRedis(self, key):
        """
        Get a redis value
        :param key: redis key
        :return: value
        """
        return r.hget(self.rhash, key)

    def delRedis(self, key):
        """
        Delete a redis value
        :param key: redis key
        :return: None
        """
        return r.hdel(self.rhash, key)

    def increaseStat(self, stat):
        """
        Increase a stat value
        :param stat: which stat increase
        :return: redis response
        """
        response = r.hincrby(self.rhash, stat)
        return response

    def isActive(self):
        return bool(r.hget(self.rhash, "active")) or False

    def getValue(self, key):
        return r.get(key)

    def isAdmin(self, new_value=None):
        """
        Get if current user is admin or set it admin.
        """
        if not new_value:
            return r.hget(self.rhash, 'admin')

        r.hset(self.rhash, 'admin', new_value)
        return True

    def isMaster(self, new_master=None):
        """Get if current user is master or set it master."""
        if not new_master:
            return r.hget(self.rhash, 'master')

        r.hset(self.rhash, 'master', new_master)
        return True

    def setLang(self, new_lang=None):
        """Get the current lang or set it new."""
        if not new_lang:
            return r.hget(self.rhash, 'lang')

        r.hset(self.rhash, 'lang', new_lang)
        return True
