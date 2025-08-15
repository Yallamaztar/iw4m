from iw4m import IW4MWrapper
from os import environ

iw4m = IW4MWrapper(
    base_url  = environ['IW4M_URL'],   # your server URL
    server_id = environ['IW4M_ID'],    # your server ID
    cookie    = environ['IW4M_HEADER'] # your IW4M-Admin cookie
)

player = iw4m.Player(iw4m)
print(player.ban_reason("28407"))
