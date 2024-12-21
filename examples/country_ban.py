# ---------------------------- #
# Country Ban Plugin
# Author:  Budiworld
# GitHub:  https://github.com/Yallamaztar/iw4m
# ---------------------------- #

import os, time, requests
from iw4m import IW4MWrapper

class CountryBanPlugin:
    SERVER_KICK_COUNTRY_BANNED = "This country is not allowed on this server"

    def __init__(self):
        self.banned_countries = []

        self.iw4m = IW4MWrapper(
            base_url=os.environ['IW4M_URL'],
            server_id=os.environ['IW4M_ID'],
            cookie=os.environ['IW4M_HEADER']
        )

        self.server   = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)
        self.player   = self.iw4m.Player(self.iw4m) 

    def add_banned_country(self, country: str):
        country = country.lower()
        if country not in self.banned_countries:
            self.banned_countries.append(country)

    def remove_banned_country(self, country: str):
        country = country.lower()
        if country in self.banned_countries:
            self.banned_countries.remove(country)

    def is_banned(self, country: str) -> bool:
        return country.lower() in self.banned_countries

    def get_player_info(self, guid: int) -> tuple:
        info = self.player.info(guid)
        return info['ip_address'], info['name']

    def get_country(self, ip_address: str) -> str:
        return requests.get(f"http://ip-api.com/json/{ip_address}").json()['country']

    def start(self, interval: float = 2.5):
        while True:
            players = self.server.get_players()
            for player in players:
                guid = player['url'][16:]
                ip_addr, client = self.get_player_info(guid)

                if ip_addr and client:
                    country = self.get_country(ip_addr).lower()

                    if self.is_banned(country):
                        self.commands.kick(client, self.SERVER_KICK_COUNTRY_BANNED)
                        print(f"Kicked player: {client} from {country.capitalize()}")

            time.sleep(interval)

if __name__ == '__main__':
    plugin = CountryBanPlugin()
    plugin.add_banned_country("The Netherlands")
    plugin.start(interval=3.5)
