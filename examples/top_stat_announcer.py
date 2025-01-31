# ---------------------------- #
# Top Stat Announcer Plugin
# Author:  Budiworld
# GitHub:  https://github.com/Yallamaztar/iw4m
# ---------------------------- #

import os, time
from iw4m import IW4MWrapper

class TopStatAnnouncerPlugin:
    def __init__(self):
        self.iw4m = IW4MWrapper(
            base_url=os.environ['IW4M_URL'],
            server_id=os.environ['IW4M_ID'],
            cookie=os.environ['IW4M_HEADER']
        )

        self.server = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)
        self.player = self.iw4m.Player(self.iw4m)
    
    def get_top_five_players(self):
        players = self.server.get_top_players()
        return players['#1'], players['#2'], players['#3'], players['#4'], players['#5']
    
    def get_server_name(self):
        return self.server.status()[0]['name']

    def start(self, i=1):
        while True:
            self.commands.say(f"^7[ ^3Top ^7Players On ^5{self.get_server_name()} ^7]")
            players = self.get_top_five_players()
            for player in players:
                self.commands.say(
                    f"^7[^5#{i}^7]: {player['name']} - ^5Kills^7: {player['stats']['total kills']} | ^5KDR^7: {player['stats']['kills per death']}"
                )
                i += 1
                time.sleep(0.15)

            time.sleep(15)
            i = 1

plugin = TopStatAnnouncerPlugin()
plugin.start()