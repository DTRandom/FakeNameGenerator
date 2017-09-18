import json


class callMess:
    """Get the message text and buttons callbacks / url."""

    def __init__(self, lang, status):
        try:
            self.lang = lang.decode('utf-8')
        except AttributeError:
            self.lang = 'US'
        self.state = status
        with open('./data/language/lang' + self.lang + ".json") as j:
            self.jsonlang = json.load(j)
        with open('./data/callback/callback.json') as j:
            self.jsoncallback = json.load(j)

    def messageText(self):
        """Get the message text based on the status and the language."""
        text = "⚠️ Errore ⚠️"
        for a in self.jsonlang["status"]:
            if a["state"] == self.state:
                text = a["text"]
        return text

    def callbackText(self):
        """Get the buttons text."""
        buttons = []
        for a in self.jsonlang["status"]:
            if a["state"] == self.state:
                for b in a["buttons"]:
                    for c in b["row"]:
                        row = []
                        for d in c["column"]:
                            row.append(d["text"])
                        buttons.append(row)
        print(buttons)
        return buttons

    def callbackData(self, btns, text):
        """Get the buttons data."""
        x = 0
        y = 0
        print('asd')
        for a in self.jsoncallback["status"]:
            if a["state"] == self.state:
                print(a, '\n')
                for b in a["buttons"]:
                    print(b, '\n')
                    for c in b["row"]:
                        print(c, '\n')
                        for d in c["column"]:
                            if d["type"] == 'url':
                                btns[x].url(str(text[x][y]), d["cb"])
                            else:
                                if d["data"] != 'None':
                                    btns[x].callback(str(text[x][y]),
                                                     d["cb"], data=d["data"])
                                else:
                                    btns[x].callback(str(text[x][y]),
                                                     d["cb"], data=None)
                            y += 1
                        y = 0
                        x += 1
                return btns
