![http://152.53.132.41:1624](./assets/brownie.png)
*Hop on brownies :)*

# **IW4M-Admin Wrapper 🎮**

### An **easy-to-use** Python wrapper for interacting with IW4M-Admin

## **Introduction**

Welcome to the official wiki for the *IW4M-Admin Wrapper*! This wrapper allows you to **easily interact** with the IW4M-Admin server through a simple Python interface. Whether you're server staff or a developer, this wrapper simplifies your interactions with IW4M-Admin, enabling you to manage players, retrieve statistics, and more. 📊

---
## **Setting up iw4m**
**you need to get your iw4m server's URL in this case it would be `http://152.53.132.41:1624`**

![setting_up_1](./assets/image.png)
![setting_up_2](./assets/image-1.png)
![setting_up_3](./assets/image-2.png)
![setting_up_4](./assets/image-3.png)

----

## **Example Usage**
```py3
from iw4m import IW4MWrapper
from os import environ

iw4m = IW4MWrapper(
    base_url  = environ['IW4M_URL'],   # your server URL
    server_id = environ['IW4M_ID'],    # your server ID
    cookie    = environ['IW4M_HEADER'] # your IW4M-Admin cookie
)

# Creating an instance of Server class
server = iw4m.Server(iw4m) 

# Creating an instance of Player class
player = iw4m.Player(iw4m)

# Creating an instance of Command class
commands = iw4m.Commands(iw4m)

print(server.get_players())
# [
#    {'name': '[BSTR]FuRioSa_', 'role': 'user', 'url': '/Client/Profile/1480'},
#    {'name': 'BDQ', 'role': 'user', 'url': '/Client/Profile/455'},
#    {'name': 'LetikTV', 'role': 'user', 'url': '/Client/Profile/870'},
#    {'name': 'ziad_mohamed_6', 'role': 'user', 'url': '/Client/Profile/3835'}
# ]

print(player.info("1480"))
# {
#    'guid': '7062D',
#    'ip_address': '88.XX.XXX.XXX',
#    'level': 'User',
#    'link': 'http://152.53.132.41:1624/Client/Profile/1480',
#    'name': '[BSTR]FuRioSa_',
#    'old_ips': ['88.XX.130.XXX'],
#    'stats': {'Connections': '17',
#           'Hidden Ingame': 'Is not',
#           'Kills Per Death': '1.17',
#           'Last Map Played': 'Nuketown 2025',
#           'Last Server Played': 'Brownies Nuketown Sniper SND',
#           'Overall Ranking': '#56 of 138',
#           'Score Per Minute': '747.8',
#           'Total Deaths': '763',
#           'Total Kills': '889'},
#   'vpn_whitelist': False
# }

print(commands.privatemessage("[BSTR]FuRioSa_", "Bubi betta"))
# '[]' For some reason commands just return an empty list

```

---

# Explore More

**You can find additional example usages in the ``examples/`` directory**

**For further information, check out the [official wiki (coming soon...)]()**

----

# Come Play on Brownies SND 🍰
### Why Brownies? 🤔
- **Stability:** Brownies delivers a consistent, lag-free experience, making it the perfect choice for players who demand uninterrupted action
- **Community:** The players at Brownies are known for being helpful, competitive, and fun—something Orion can only dream of
- **Events & Features:** Brownies is constantly running unique events and offers more server-side customization options than Orion, ensuring every game feels fresh

---

#### [Brownies Discord](https://discord.gg/FAHB3mwrVF) | [Brownies IW4M](http://152.53.132.41:1624/) | Made With ❤️ By Budiworld