# ---------------------------- #
# VPN detection example
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

server   = iw4m.Server(iw4m)
commands = iw4m.Commands(iw4m)
player   = iw4m.Player(iw4m)

SERVER_KICK_VPNS_NOTALLOWED = "VPN's Aren't Allowed On This Server"

def is_whitelisted(guid: int) -> bool:
    return player.info(guid)['vpn_whitelist']

def is_vpn(ip_address: str) -> bool:
    r = requests.get(f"https://api.xdefcon.com/proxy/check/?ip={ip_address}").json()
    if r['success']:
        return r['proxy']

def get_player_info(guid: int) -> str:
    return player.info(guid)['ip_address'], player.info(guid)['name']

def main() -> None:
    while True:
        players = server.get_players()
        for player in players:
            guid = player['url'][16:]
            ip_addr, client = get_player_info(guid)

            if not is_whitelisted(guid) and is_vpn(ip_addr):
                commands.kick(client, SERVER_KICK_VPNS_NOTALLOWED)

        time.sleep(2.5)

if __name__ == '__main__':
    main()
        