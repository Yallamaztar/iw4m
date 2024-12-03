import os, time
import detectlanguage
from iw4m import IW4MWrapper


class LanguageRestrictorPlugin:
    SERVER_KICK_LANGUAGENOTALLOWED = "This language isn't allowed on this server"

    def __init__(self):
        self.banned_languages = []
        self.last_seen_meesage = set()
        
        self.iw4m = IW4MWrapper(
            base_url  = os.environ['IW4M_URL'],
            server_id = os.environ['IW4M_ID'],
            cookie    = os.environ['IW4M_HEADER']
        )

        self.server   = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)
        self.player   = self.iw4m.Player(self.iw4m) 

        detectlanguage.configuration.api_key = os.environ['LANG_DETECT_API'] # Get your API key at [ https://detectlanguage.com/ ]

    def add_language(self, language: str):
        self.banned_languages.append(language)

    def detect_language(self, message: str):
        data = detectlanguage.detect(message)
        for item in data:
            if item['language'] in self.banned_languages:
                return item['isReliable']

            break

    def start(self, interval: float = 1.5):
        while True:
            chat = self.server.read_chat()[0]
            if chat not in self.last_seen_meesage:
                if self.detect_language(chat[1]):
                    self.commands.warn(chat[0], self.SERVER_KICK_LANGUAGENOTALLOWED)
                self.last_seen_meesage.add(chat)

            time.sleep(interval)

if __name__ == '__main__':
    plugin = LanguageRestrictorPlugin()
    plugin.add_language("fr") # France
    plugin.start(interval=86.4) 
