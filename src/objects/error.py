import config
import json
import redis
import datetime
r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT,
                      db=config.REDIS_DB, password=config.REDIS_PASSWORD)


class Error:
    """Default Error Class."""

    def __init__(self, chat_, bot_, user_):
        """Define the Error giving the chat and the bot."""
        self.chat = chat_
        self.bot = bot_
        self.user = user_

    def sendError(self, errorType):
        """Send the error to the Log Channel."""
        with open("./data/language/lang" +
                  r.get('lang').decode('utf-8') +
                  ".json") as j:
            jsonlang = json.load(j)
        text = "⚠️ Error ⚠️"
        for a in jsonlang["errors"]:
            if errorType == a["error"]:
                text = a["text"].format(chatid=str(self.chat.id),
                                        chattype=self.chat.type,
                                        userid=str(self.user.id),
                                        userfname=self.user.first_name,
                                        time=datetime.datetime.now())
        self.bot.api.call('sendMessage', {
            'chat_id': config.DEVELOPERID,
            'text': text,
            'parse_mode': 'HTML'
        })
