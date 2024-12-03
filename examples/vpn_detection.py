# ---------------------------- #
# VPN Detection Plugin
# Author:  Budiworld
# GitHub:  https://github.com/Yallamaztar/iw4m
# ---------------------------- #

import os, time, requests
from iw4m import IW4MWrapper

class VPNDetectionPlugin:
    SERVER_KICK_VPNS_NOTALLOWED = "VPN's Aren't Allowed On This Server"
    
    def __init__(self):
        self.iw4m = IW4MWrapper(
            base_url=os.environ['IW4M_URL'],
            server_id=os.environ['IW4M_ID'],
            cookie=os.environ['IW4M_HEADER']
        )

        self.server = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)
        self.player = self.iw4m.Player(self.iw4m)

    def is_whitelisted(self, guid: int) -> bool:
        return self.player.info(guid)['vpn_whitelist']
    
    def is_vpn(self, ip_address: str) -> bool:
        r = requests.get(f"https://api.xdefcon.com/proxy/check/?ip={ip_address}").json()
        return r['success'] and r['proxy']

    def get_player_info(self, guid: int) -> tuple:
        info = self.player.info(guid)
        return info['ip_address'], info['name']
    
    def check_players(self):
        players = self.server.get_players()
        for player in players:
            guid = player['url'][16:]
            ip_addr, client = self.get_player_info(guid)

            if not self.is_whitelisted(guid) and self.is_vpn(ip_addr):
                self.commands.kick(client, self.SERVER_KICK_VPNS_NOTALLOWED)
                print(f"Kicked player: {client} with IP: {ip_addr}")

    def start(self):
        while True:
            self.check_players()
            time.sleep(2.5)

if __name__ == '__main__':
    plugin = VPNDetectionPlugin()
    plugin.start()
