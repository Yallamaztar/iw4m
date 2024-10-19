
from bs4 import BeautifulSoup as bs
from requests import sessions
import aiohttp
import re

class IW4MWrapper():
    def __init__(self, base_url: str, server_id: int, cookie: str):
        self.base_url = base_url 
        self.server_id = server_id
        self.session = sessions.Session()
        self.session.headers.update({ "Cookie": cookie })
    
    class GameUtils:
        def __init__(self, wrapper):
            self.wrapper = wrapper
            
        def send_command(self, command: str): 
            try:
                response = self.wrapper.session.get(f"{self.wrapper.base_url}/Console/Execute?serverId={self.wrapper.server_id}&command={command}")
                return response.text
            
            except Exception as e:
                print(response.status_code())
            return e, response.status_code
        
        def color_handler(self, color: str):
            color = color.lower()
            colors = {
                "black": "^0", "red": "^1", "green": "^2", 
                "yellow": "^3","dblue": "^4","lblue": "^5", 
                "pink": "^6", "white": "^7", "gray": "^8", 
                "brown": "^9", "blink": "^F", "box": "^HH"
            }
            return colors.get(color, "")
        
        def read_chat(self):
            chat = []
            
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/").text
            soup = bs(response, 'html.parser')
            entries = soup.find_all('div', class_='text-truncate')
    
            for entry in entries:
                sender_span = entry.find('span')
                if sender_span:
                    sender_tag = sender_span.find('colorcode')
                    sender = sender_tag.get_text() if sender_tag else None

                    message_span = entry.find_all('span')
                    if len(message_span) > 1:
                        message_tag = message_span[1].find('colorcode')
                        message = message_tag.get_text() if message_tag else None

                    chat.append((
                        sender,
                        message
                    ))
    
            return chat
        
        def find_player(self, name: str = "", xuid: str = "", count: int = 1, 
                        offset: int = 0, direction: int = 0):
            if not name and not xuid:
                return None

            response = self.wrapper.session.get(
                f"{self.wrapper.base_url}/api/client/find",
                params={
                    "name": name,
                    "xuid": xuid,
                    "count": count,
                    "offset": offset,
                    "direction": direction
                }
            ).text
            return response
        
        def get_players(self):
            players = []
            
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/").text
            soup = bs(response, 'html.parser')
            
            links = soup.find_all('a', class_='text-light-dm text-dark-lm no-decoration text-truncate ml-5 mr-5')
            for link in links:
                colorcode = link.find('colorcode')
                if colorcode:
                    player = colorcode.text
                    href   = link.get('href')
                    players.append((player, href))
            
            return players

    class Player:
        def __init__(self, wrapper):
            self.wrapper = wrapper

        def stats(self, client_id: str):
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/api/stats/{client_id}")
            return response.text
        
        def info(self, client_id: str):
            info = {}
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Profile/{client_id}").text
            soup = bs(response, 'html.parser')

            name = soup.find('span', class_='font-size-20 font-weight-medium text-force-break')
            if name:
                info['name'] = name.find('colorcode').text

            guid = soup.find('div', class_='text-muted', id='altGuidFormatsDropdown')
            if guid:
                info['guid'] = guid.text

            ip = soup.find('div', class_='align-self-center align-self-md-start d-flex flex-row')
            if ip:
                info['ip_address'] = ip.find('span', class_="text-muted mr-5").text

            stats = {}
            entries = soup.find_all('div', class_="profile-meta-entry")
            for entry in entries:
                _value, _title = entry.find('div', class_="profile-meta-value"), entry.find('div', "profile-meta-title")
                if _value and _title:
                    value = _value.find('colorcode').text.strip()
                    title = ' '.join(_title.stripped_strings).strip()
                    stats[title] = value
            
            info['stats'] = stats 
            return info
        
        def chat_history(self, client_id: str, count: int):
            messages = []
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Meta/{client_id}?offset=30&count={count}").text
            soup = bs(response, 'html.parser')

            entries = soup.find_all('div', class_='profile-meta-entry')

            for entry in entries:
                message = entry.find('span', class_='client-message')
                if message:
                    messages.append(message.text.strip())    

            return messages
        
        def name_changes(self, client_id: str):
            name_changes = []
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=AliasUpdate").text
            soup = bs(response, 'html.parser')

            entries = soup.find_all('div', class_='profile-meta-entry')
            for entry in entries:
                colorcode = entry.find('colorcode')
                username = colorcode.text if colorcode else None

                ip_address_tag = re.search(r'\[(\d{1,3}(?:\.\d{1,3}){3})\]', entry.text)
                ip_address = ip_address_tag.group(1) if ip_address_tag else None

                date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                date = date_tag.find('span', class_='text-light-dm text-dark-lm').text if date_tag else None

                if all([username, ip_address, date]):
                    name_changes.append((username, ip_address, date))

            return name_changes
        
        def administered_penalties(self, client_id: int, count: int = 30):
            administered_penalties = []
            
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=Penalized").text
            soup = bs(response, 'html.parser')

            entries = soup.find_all('div', class_='profile-meta-entry')
            for entry in entries:
                if len(administered_penalties) >= count:
                    break

                action_tag = entry.find('span', class_=re.compile(r'penalties-color'))
                action = action_tag.text.strip() if action_tag else None

                player_tag = entry.find('span', class_='text-highlight')
                if player_tag:
                    colorcode_tag = player_tag.find('colorcode')
                    player = colorcode_tag.text.strip() if colorcode_tag else None

                reason_tag = entry.find_all('colorcode')
                reason = reason_tag[-1].text.strip() if reason_tag else None

                date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                if date_tag:
                    date_span = date_tag.find('span', class_='text-light-dm text-dark-lm')
                    date = date_span.text.strip() if date_span else None

                if action and player and reason:
                    administered_penalties.append({
                        'action': action,
                        'player': player,
                        'reason': reason,
                        'date': date
                    })

            return administered_penalties
        
        def received_penalties(self, client_id: int, count: int = 30):
            received_penalties = []

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=ReceivedPenalty").text
            soup = bs(response, 'html.parser')

            entries = soup.find_all('div', class_='profile-meta-entry')
            for entry in entries:
                if len(received_penalties) >= count:
                    break

                action_tag = entry.find('span', class_=re.compile(r'penalties-color-'))
                action = action_tag.text.strip() if action_tag else None

                player_tag = entry.find('span', class_='text-highlight')
                if player_tag:
                    colorcode_tag = player_tag.find('colorcode')
                    player = colorcode_tag.text.strip() if colorcode_tag else None

                reason_tag = entry.find_all('colorcode')
                reason = reason_tag[-1].text.strip() if reason_tag else None

                date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                if date_tag:
                    date_span = date_tag.find('span', class_='text-light-dm text-dark-lm')
                    date = date_span.text.strip() if date_span else None

                if action and player and reason:
                    received_penalties.append({
                        'action': action,
                        'player': player,
                        'reason': reason,
                        'date': date,
                    })
            return received_penalties
        
        def connection_history(self, client_id: int, count: int = 30):
            connection_history = []

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=ConnectionHistory").text
            soup = bs(response, 'html.parser')

            entries = soup.find_all('div', class_='profile-meta-entry')
            for entry in entries:
                if len(connection_history) >= count:
                        break

                action_tag = entry.find('span', class_='text-secondary') or entry.find('span', class_='text-light-green')
                action = action_tag.get_text(strip=True) if action_tag else None

                context_tag = entry.find('colorcode')
                context = context_tag.get_text(strip=True) if context_tag else None

                date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                date = None
                if date_tag:
                    date_span = date_tag.find('span', class_='text-light-dm text-dark-lm')
                    date = date_span.get_text(strip=True) if date_span else None

                if action and context and date:
                    connection_history.append({
                        'action': action,
                        'context': context,
                        'date': date
                    })

            return connection_history
        
        def permissions(self, client_id: int, count: int = 30):
            permissions = []

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=PermissionLevel").text
            soup = bs(response, 'html.parser')
        
            entries = soup.find_all('div', class_='profile-meta-entry')
            for entry in entries:
                if len(permissions) >= count:
                    break
            
                level_tag = entry.find('span', class_=re.compile(r'level-color-'))
                level = level_tag.text.strip() if level_tag else 'Unknown'

                user_tag = entry.find('span', class_='text-highlight')
                user = None
                if user_tag:
                    colorcode_tag = user_tag.find('colorcode')
                    user = colorcode_tag.get_text(strip=True) if colorcode_tag else None

                date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                date = None
                if date_tag:
                    date_span = date_tag.find('span', class_='text-light-dm text-dark-lm')
                    date = date_span.get_text(strip=True) if date_span else None

                action = f"changed to {level} by {user}"

                if action and user and date:
                    permissions.append({
                        'action': action,
                        'date': date
                    })
                    
            return permissions
    
    class Commands:
        def __init__(self, wrapper):
            self.wrapper = wrapper
            self.game_utils = self.wrapper.GameUtils(self.wrapper)
        
        #  Command List   #
        def setlevel(self, player: str, level: str):
            return self.game_utils.send_command(f"!setlevel {player} {level}")

        def change_map(self, map_name: str):
            return self.game_utils.send_command(f"!map {map_name}")
        
        def ban(self, player: str, reason: str):
            return self.game_utils.send_command(f"!ban {player} {reason}")
            
        def unban(self, player: str, reason: str):
            return self.game_utils.send_command(f"!unban {player} {reason}")

        def fastrestart(self):
            return self.game_utils.send_command("!fastrestart")

        def maprotate(self):
            return self.game_utils.send_command("!mr")
        
        def requesttoken(self):
            return self.game_utils.send_command("!requesttoken")
        
        def clearallreports(self):
            return self.game_utils.send_command("!clearallreports")
        
        def alias(self, player: str):
            return self.game_utils.send_command(f"!alias {player}")

        def whoami(self):
            return self.game_utils.send_command("!whoami")
        
        def warn(self, player: str, reason: str):
            return self.game_utils.send_command(f"!warn {player} {reason}")

        def warnclear(self, player: str):
            return self.game_utils.send_command(f"!warnclear {player}")

        def kick(self, player: str, reason: str):
            return self.game_utils.send_command(f"!kick {player} {reason}")

        def tempban(self, player: str, duration: str, reason: str):
            return self.game_utils.send_command(f"!tempban {player} {duration} {reason}")

        def usage(self):
            return self.game_utils.send_command("!usage")
        
        def uptime(self):
            return self.game_utils.send_command("!uptime")
        
        def flag(self, player: str, reason: str):
            return self.game_utils.send_command(f"!flag {player} {reason}")
        
        def unflag(self, player: str, reason: str):
            return self.game_utils.send_command(f"!unflag {player} {reason}")

        def mask(self):
            return self.game_utils.send_command("!mask")
        
        def baninfo(self, player: str):
            return self.game_utils.send_command(f"!baninfo {player}")

        def setpassword(self, password: str):
            return self.game_utils.send_command(f"!setpassword {password}")

        def runas(self, command):
            return self.game_utils.send_command(f"!runas {command}")
        
        def addnote(self, player, note):
            return self.game_utils.send_command(f"!addnote {player} {note}")
        
        def list_players(self):
            return self.game_utils.send_command("!list")
        
        def plugins(self):
            return self.game_utils.send_command("!plugins")
        
        def reports(self):
            return self.game_utils.send_command("!reports")
        
        def offlinemessages(self):
            return self.game_utils.send_command("!offlinemessages")
        
        def sayall(self, message, color=None):
            return self.game_utils.send_command(f"!sayall {self.wrapper.color_handler(color)}{message}")
        
        def say(self, message, color=None):
            return self.game_utils.send_command(f"!say {self.wrapper.color_handler(color)}{message}")

        def rules(self):
            return self.game_utils.send_command("!rules")
        
        def ping(self):
            return self.game_utils.send_command("!ping")
        
        def setgravatar(self, email):
            return self.game_utils.send_command(f"!setgravatar {email}")
        
        def help(self):
            return self.game_utils.send_command("!help")
        
        def admins(self):
            return self.game_utils.send_command("!admins")
        
        def privatemessage(self, player, message):
            return self.game_utils.send_command(f"!privatemessage {player} {message}")
        
        def readmessage(self):
            return self.game_utils.send_command("!readmessage")
        
        def report(self, player, reason): 
            return self.game_utils.send_command(f"!report {player} {reason}")

        #  Script Plugin  #
        def giveweapon(self, player, weapon):
            return self.game_utils.send_command(f"!giveweapon {player} {weapon}")
        
        def takeweapons(self, player):
            return self.game_utils.send_command(f"!takeweapons {player}")
        
        def lockcontrols(self, player):
            return self.game_utils.send_command(f"!lockcontrols {player}")

        def noclip(self):
            return self.game_utils.send_command("!noclip")
        
        def alert(self, player, message):
            return self.game_utils.send_command(f"!alert {player} {message}")
        
        def gotoplayer(self, player):
            return self.game_utils.send_command(f"!gotoplayer {player}")
        
        def playertome(self, player):
            return self.game_utils.send_command(f"!playertome {player}")
        
        def goto(self, x, y ,z):
            return self.game_utils.send_command(f"!goto {x} {y} {z}")
        
        def kill(self, player):
            return self.game_utils.send_command(f"!kill {player}")

        def setspectator(self, player):
            return self.game_utils.send_command(f"!setspectator {player}")
        
        def whitelistvpn(self, player):
            return self.game_utils.send_command(f"!whitelistvpn {player}")

        def disallowvpn(self, player):
            return self.game_utils.send_command(f"!disallowvpn {player}")
        
        def bansubnet(self, subnet):
            return self.game_utils.send_command(f"!bansubnet {subnet}")
        
        def unbansubnet(self, subnet):
            return self.game_utils.send_command(f"!unbansubnet {subnet}")
        
        def switchteam(self, player):
            return self.game_utils.send_command(f"!switchteam {player}")

        #      Login      #
        def login(self, password):
            return self.game_utils.send_command(f"!login {password}")

        #       Mute      #
        def mute(self, player, reason):
            return self.game_utils.send_command(f"!mute {player} {reason}")
        
        def muteinfo(self, player):
            return self.game_utils.send_command(f"!muteinfo {player}")
        
        def tempmute(self, player, duration, reason):
            return self.game_utils.send_command(f"!tempmute {player} {duration} {reason}")
        
        def unmute(self, player, reason):
            return self.game_utils.send_command(f"!unmute {player} {reason}")
        
        #  Simple Status  #
        def mostkills(self):
            return self.game_utils.send_command("!mostkills")
        
        def mostplayed(self):
            return self.game_utils.send_command("!mostplayed")
        
        def rxs(self):
            return self.game_utils.send_command("!rxs")
        
        def topstats(self):
            return self.game_utils.send_command("!topstats")
        
        def stats(self, player=None):
            if player == None:
                return self.game_utils.send_command("!x")
            else:
                return self.game_utils.send_command(f"!x {player}")

class AsyncIW4MWrapper():
    def __init__(self, base_url: str, server_id: int, cookie: str):
        self.base_url = base_url
        self.server_id = server_id
        self.cookie = cookie
        
    class GameUtils:
        def __init__(self, wrapper):
            self.wrapper = wrapper
            
        async def send_command(self, command: str):
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(
                        f"{self.wrapper.base_url}/Console/Execute?serverId={self.wrapper.server_id}&command={command}",
                        headers={"Cookie": self.wrapper.cookie}
                    ) as response:
                        return await response.text()
        
                except aiohttp.ClientError as e:
                    raise

        async def color_handler(self, color: str):
            if color is None:
                return ""
            color = color.lower()
            colors = {
                "black": "^0", "red": "^1", "green": "^2", 
                "yellow": "^3","dblue": "^4","lblue": "^5", 
                "pink": "^6", "white": "^7", "gray": "^8", 
                "brown": "^9", "blink": "^F", "box": "^HH"
            }
            return await colors.get(color, "")
        
        
        async def read_chat(self):
            chat = []
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    text = await response.text()
                    soup = bs(text, 'html.parser')
                    
                    entries = soup.find_all('div', class_="text-truncate")
                    for entry in entries:
                        span = entry.find('span')
                        if span:
                            sender_tag = span.find('colorcode')
                            sender = sender_tag.get_text() if sender_tag else None
                            message_span = entry.find_all('span')
                            if len(message_span) > 1:
                                message_tag = message_span[1].find('colorcode')
                                message = message_tag.get_text() if message_tag else None

                            if sender and message:
                                chat.append((
                                    sender,
                                    message
                                ))
            return chat
                            

        async def find_player(self, name: str = "", xuid: str = "", count: int = 1, 
                              offset: int = 0, direction: int = 0):
            if not name and not xuid:
                return 
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/api/client/find",
                    headers={"Cookie": self.wrapper.cookie},
                    params={
                        "name": name,
                        "xuid": xuid,
                        "count": count,
                        "offset": offset,
                        "direction": direction
                    }
                ) as response:
                    
                    response_text = await response.text()
                    return response_text
        
        async def get_players(self):
            players = []
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    links = soup.find_all('a', class_='text-light-dm text-dark-lm no-decoration text-truncate ml-5 mr-5')
                    for link in links:
                        colorcode = link.find('colorcode')
                        if colorcode:
                            player = colorcode.text
                            href = link.get('href')
                            players.append((player, href))

            return players
    
    class Player:
        def __init__(self, wrapper):
            self.wrapper = wrapper
        
        async def stats(self, client_id: str):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/api/stats/{client_id}",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    response_text = await response.text()
                    return response_text
        
        async def info(self, client_id: str):
            info = {}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Client/Profile/{client_id}",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    name = soup.find('span', class_='font-size-20 font-weight-medium text-force-break')
                    if name:
                        info['name'] = name.find('colorcode').text

                    guid = soup.find('div', class_='text-muted', id='altGuidFormatsDropdown')
                    if guid:
                        info['guid'] = guid.text

                    ip = soup.find('div', class_='align-self-center align-self-md-start d-flex flex-row')
                    if ip:
                        info['ip_address'] = ip.find('span', class_="text-muted mr-5").text

                    stats = {}
                    entries = soup.find_all('div', class_="profile-meta-entry")
                    for entry in entries:
                        _value = entry.find('div', class_="profile-meta-value")
                        _title = entry.find('div', class_="profile-meta-title")
                        if _value and _title:
                            value = _value.find('colorcode').text.strip()
                            title = ' '.join(_title.stripped_strings).strip()
                            stats[title] = value

                    info['stats'] = stats

            return info
        
        async def chat_history(self, client_id: str, count: int):
            messages = []
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Client/Meta/{client_id}?offset=30&count={count}",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('div', class_='profile-meta-entry')
                    for entry in entries:
                        message = entry.find('span', class_='client-message')
                        if message:
                            messages.append(message.text.strip())

            return messages
        
        async def name_changes(self, client_id: int):
            name_changes = []
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=AliasUpdate",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('div', class_='profile-meta-entry')
                    for entry in entries:
                        colorcode = entry.find('colorcode')
                        username = colorcode.text if colorcode else None

                        ip_address_tag = re.search(r'\[(\d{1,3}(?:\.\d{1,3}){3})\]', entry.text)
                        ip_address = ip_address_tag.group(1) if ip_address_tag else None

                        date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                        date = date_tag.find('span', class_='text-light-dm text-dark-lm').text if date_tag else None

                        if all([username, ip_address, date]):
                            name_changes.append((username, ip_address, date))

            return name_changes
        
        async def administered_penalties(self, client_id: int, count: int = 30):
            administered_penalties = []
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=Penalized",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('div', class_='profile-meta-entry')
                    for entry in entries:
                        if len(administered_penalties) >= count:
                            break

                        action_tag = entry.find('span', class_=re.compile(r'penalties-color'))
                        action = action_tag.text.strip() if action_tag else None

                        player_tag = entry.find('span', class_='text-highlight')
                        if player_tag:
                            colorcode_tag = player_tag.find('colorcode')
                            player = colorcode_tag.text.strip() if colorcode_tag else None

                        reason_tag = entry.find_all('colorcode')
                        reason = reason_tag[-1].text.strip() if reason_tag else None

                        date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                        if date_tag:
                            date_span = date_tag.find('span', class_='text-light-dm text-dark-lm')
                            date = date_span.text.strip() if date_span else None

                        if action and player and reason:
                            administered_penalties.append({
                                'action': action,
                                'player': player,
                                'reason': reason,
                                'date': date
                            })

            return administered_penalties

        async def received_penalties(self, client_id: int, count: int = 30):
            received_penalties = []
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=ReceivedPenalty",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('div', class_='profile-meta-entry')
                    for entry in entries:
                        if len(received_penalties) >= count:
                            break

                        action_tag = entry.find('span', class_=re.compile(r'penalties-color-'))
                        action = action_tag.text.strip() if action_tag else None

                        player_tag = entry.find('span', class_='text-highlight')
                        if player_tag:
                            colorcode_tag = player_tag.find('colorcode')
                            player = colorcode_tag.text.strip() if colorcode_tag else None

                        reason_tag = entry.find_all('colorcode')
                        reason = reason_tag[-1].text.strip() if reason_tag else None

                        date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                        if date_tag:
                            date_span = date_tag.find('span', class_='text-light-dm text-dark-lm')
                            date = date_span.text.strip() if date_span else None

                        if action and player and reason:
                            received_penalties.append({
                                'action': action,
                                'player': player,
                                'reason': reason,
                                'date': date,
                            })

            return received_penalties
        
        async def connection_history(self, client_id: int, count: int = 30):
            connection_history = []
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=ConnectionHistory",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('div', class_='profile-meta-entry')
                    for entry in entries:
                        if len(connection_history) >= count:
                            break

                        action_tag = entry.find('span', class_='text-secondary') or entry.find('span', class_='text-light-green')
                        action = action_tag.get_text(strip=True) if action_tag else None

                        context_tag = entry.find('colorcode')
                        context = context_tag.get_text(strip=True) if context_tag else None

                        date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                        date = None
                        if date_tag:
                            date_span = date_tag.find('span', class_='text-light-dm text-dark-lm')
                            date = date_span.get_text(strip=True) if date_span else None

                        if action and context and date:
                            connection_history.append({
                                'action': action,
                                'context': context,
                                'date': date
                            })

            return connection_history
        
        async def permissions(self, client_id: int, count: int = 30):
            permissions = []
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Client/Profile/{client_id}?metaFilterType=PermissionLevel",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('div', class_='profile-meta-entry')
                    for entry in entries:
                        if len(permissions) >= count:
                            break

                        level_tag = entry.find('span', class_=re.compile(r'level-color-'))
                        level = level_tag.text.strip() if level_tag else 'Unknown'

                        user_tag = entry.find('span', class_='text-highlight')
                        user = None
                        if user_tag:
                            colorcode_tag = user_tag.find('colorcode')
                            user = colorcode_tag.get_text(strip=True) if colorcode_tag else None

                        date_tag = entry.find('div', id=re.compile(r'metaContextDateToggle'))
                        date = None
                        if date_tag:
                            date_span = date_tag.find('span', class_='text-light-dm text-dark-lm')
                            date = date_span.get_text(strip=True) if date_span else None

                        action = f"changed to {level} by {user}"

                        if action and user and date:
                            permissions.append({
                                'action': action,
                                'date': date
                            })

            return permissions
    
    class Commands:
        def __init__(self, wrapper):
            self.wrapper = wrapper
            self.game_utils = self.wrapper.GameUtils(self.wrapper)
    
        #  Command List   #
        async def setlevel(self, player: str, level: str):
            return await self.game_utils.send_command(f"!setlevel {player} {level}")

        async def change_map(self, map_name: str):
            return await self.game_utils.send_command(f"!map {map_name}")
    
        async def ban(self, player: str, reason: str):
            return await self.game_utils.send_command(f"!ban {player} {reason}")
        
        async def unban(self, player: str, reason: str):
            return await self.game_utils.send_command(f"!unban {player} {reason}")

        async def fastrestart(self):
            return await self.game_utils.send_command("!fastrestart")

        async def maprotate(self):
            return await self.game_utils.send_command("!mr")
    
        async def requesttoken(self):
            return await self.game_utils.send_command("!requesttoken")
    
        async def clearallreports(self):
            return await self.game_utils.send_command("!clearallreports")
    
        async def alias(self, player: str):
            return await self.game_utils.send_command(f"!alias {player}")

        async def whoami(self):
            return await self.game_utils.send_command("!whoami")
    
        async def warn(self, player: str, reason: str):
            return await self.game_utils.send_command(f"!warn {player} {reason}")
        
        async def warnclear(self, player: str):
            return await self.game_utils.send_command(f"!warnclear {player}")
        
        async def kick(self, player: str, reason: str):
            return await self.game_utils.send_command(f"!kick {player} {reason}")

        async def tempban(self, player: str, duration: str, reason: str):
            return await self.game_utils.send_command(f"!tempban {player} {duration} {reason}")

        async def usage(self):
            return await self.game_utils.send_command("!usage")
        
        async def uptime(self):
            return await self.game_utils.send_command("!uptime")
        
        async def flag(self, player: str, reason: str):
            return await self.game_utils.send_command(f"!flag {player} {reason}")
        
        async def unflag(self, player: str, reason: str):
            return await self.game_utils.send_command(f"!unflag {player} {reason}")

        async def mask(self):
            return await self.game_utils.send_command("!mask")
        
        async def baninfo(self, player: str):
            return await self.game_utils.send_command(f"!baninfo {player}")

        async def setpassword(self, password: str):
            return await self.game_utils.send_command(f"!setpassword {password}")

        async def runas(self, command):
            return await self.game_utils.send_command(f"!runas {command}")
        
        async def addnote(self, player, note):
            return await self.game_utils.send_command(f"!addnote {player} {note}")
        
        async def list_players(self):
            return await self.game_utils.send_command("!list")
        
        async def plugins(self):
            return await self.game_utils.send_command("!plugins")
        
        async def reports(self):
            return await self.game_utils.send_command("!reports")
        
        async def offlinemessages(self):
            return await self.game_utils.send_command("!offlinemessages")
        
        async def sayall(self, message, color=None):
            return await self.game_utils.send_command(f"!sayall {self.wrapper.color_handler(color)}{message}")
        
        async def say(self, message, color=None):
            return await self.game_utils.send_command(f"!say {self.wrapper.color_handler(color)}{message}")

        async def rules(self):
            return await self.game_utils.send_command("!rules")
        
        async def ping(self):
            return await self.game_utils.send_command("!ping")
        
        async def setgravatar(self, email):
            return await self.game_utils.send_command(f"!setgravatar {email}")
        
        async def help(self):
            return await self.game_utils.send_command("!help")
        
        async def admins(self):
            return await self.game_utils.send_command("!admins")
        
        async def privatemessage(self, player, message):
            return await self.game_utils.send_command(f"!privatemessage {player} {message}")
        
        async def readmessage(self):
            return await self.game_utils.send_command("!readmessage")
        
        async def report(self, player, reason): 
            return await self.game_utils.send_command(f"!report {player} {reason}")

        #  Script Plugin  #
        async def giveweapon(self, player, weapon):
            return await self.game_utils.send_command(f"!giveweapon {player} {weapon}")
        
        async def takeweapons(self, player):
            return await self.game_utils.send_command(f"!takeweapons {player}")
        
        async def lockcontrols(self, player):
            return await self.game_utils.send_command(f"!lockcontrols {player}")

        async def noclip(self):
            return await self.game_utils.send_command("!noclip")
        
        async def alert(self, player, message):
            return await self.game_utils.send_command(f"!alert {player} {message}")
        
        async def gotoplayer(self, player):
            return await self.game_utils.send_command(f"!gotoplayer {player}")
        
        async def playertome(self, player):
            return await self.game_utils.send_command(f"!playertome {player}")
        
        async def goto(self, x, y ,z):
            return await self.game_utils.send_command(f"!goto {x} {y} {z}")
        
        async def kill(self, player):
            return await self.game_utils.send_command(f"!kill {player}")

        async def setspectator(self, player):
            return await self.game_utils.send_command(f"!setspectator {player}")
        
        async def whitelistvpn(self, player):
            return await self.game_utils.send_command(f"!whitelistvpn {player}")

        async def disallowvpn(self, player):
            return await self.game_utils.send_command(f"!disallowvpn {player}")
        
        async def bansubnet(self, subnet):
            return await self.game_utils.send_command(f"!bansubnet {subnet}")
        
        async def unbansubnet(self, subnet):
            return await self.game_utils.send_command(f"!unbansubnet {subnet}")
        
        async def switchteam(self, player):
            return await self.game_utils.send_command(f"!switchteam {player}")

        #      Login      #
        async def login(self, password):
            return await self.game_utils.send_command(f"!login {password}")

        #       Mute      #
        async def mute(self, player, reason):
            return await self.game_utils.send_command(f"!mute {player} {reason}")
        
        async def muteinfo(self, player):
            return await self.game_utils.send_command(f"!muteinfo {player}")
        
        async def tempmute(self, player, duration, reason):
            return await self.game_utils.send_command(f"!tempmute {player} {duration} {reason}")
        
        async def unmute(self, player, reason):
            return await self.game_utils.send_command(f"!unmute {player} {reason}")
        
        #  Simple Status  #
        async def mostkills(self):
            return await self.game_utils.send_command("!mostkills")
        
        async def mostplayed(self):
            return await self.game_utils.send_command("!mostplayed")
        
        async def rxs(self):
            return await self.game_utils.send_command("!rxs")
        
        async def topstats(self):
            return await self.game_utils.send_command("!topstats")
        
        async def stats(self, player=None):
            if player == None:
                return await self.game_utils.send_command("!x")
            else:
                return await self.game_utils.send_command(f"!x {player}")