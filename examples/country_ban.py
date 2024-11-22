 # ---------------------------- #
# Country Ban example
# Author:  Budiworld
# GitHub:  https://github.com/Yallamaztar/iw4m
# ---------------------------- #

import os, time, requests
from iw4m import IW4MWrapper

iw4m = IW4MWrapper(
    base_url  = os.environ['IW4M_URL'],      
    server_id = os.environ['IW4M_ID'],              
    cookie    = os.environ['IW4M_HEADER']
)

_server   = iw4m.Server(iw4m)
_commands = iw4m.Commands(iw4m)
_player   = iw4m.Player(iw4m)

SERVER_KICK_COUNTRY_BANNED = "This country is not allowed on this server"

class CountryBanPlugin:
    def __init__(self) -> None:
        self.banned_countries = []
    
    def add_banned_country(self, country: str) -> None:
        country = country.lower()
        self.banned_countries.append(country)
        print(f"Successfully Banned Country: {country.capitalize()}")   
    
    def remove_banned_country(self, country: str) -> None:
        country = country.lower()
        if country in self.banned_countries:
            self.banned_countries.remove(country)
            print(f"Successfully Unbanned Country: {country.capitalize()}")
    
    def is_banned(self, country: str) -> bool:
        country = country.lower() 
        return country in self.banned_countries
    
    def get_player_info(guid: int) -> str:
        return _player.info(guid)['ip_address'], _player.info(guid)['name']
    
    def get_country(self, ip_address: str) -> str:
        return requests.get(f"http://ip-api.com/json/{ip_address}").json()['country']
        
    def _start(self) -> None:
        while True:

            players = _server.get_players()
            for player in players:

                guid = player['url'][16:]
                ip_addr, client = self.get_player_info(guid)
                country = self.get_country(ip_addr).lower()

                if self.is_banned(country):
                    _commands.kick(client, SERVER_KICK_COUNTRY_BANNED)

            time.sleep(2.5)

if __name__ == '__main__':
    plugin = CountryBanPlugin() 
    plugin.add_banned_country("tunisia")
    plugin._start()

    
        
        

        
