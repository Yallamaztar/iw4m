# ---------------------------- #
# User crash example
# Author:  Budiworld
# GitHub:  https://github.com/Yallamaztar/iw4m
# ---------------------------- #

import os
from iw4m import IW4MWrapper

iw4m = IW4MWrapper(
    base_url  = os.environ['IW4M_URL'],      
    server_id = os.environ['IW4M_ID'],              
    cookie    = os.environ['IW4M_HEADER']
)

server   = iw4m.Server(iw4m)
commands = iw4m.Commands(iw4m)


def main(role: str):
    players  = server.get_players()

    for player in players:
        if player['role'] == f'{role}': 
            commands.privatemessage(player['name'], '^Hæææ') 


if __name__ == '__main__':
    main("user")