
import aiohttp, aiofiles
from requests import sessions
from bs4 import BeautifulSoup as bs
import os, tempfile, re
import logging

class IW4MWrapper():
    def __init__(self, base_url: str, server_id: int, cookie: str, _logging: bool = False) -> None:
        self.base_url = base_url
        self.server_id = server_id
        self.session = sessions.Session()
        self.session.headers.update({ "Cookie": cookie })
        self._logging = _logging

        if self._logging:
            logging.basicConfig(
                filename=os.path.join(os.path.dirname(__file__), 'tmp', 'iw4mAdmin.log'),
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
            )
            logging.info(f"Initialized IW4MWrapper for server {self.base_url} with ID {self.server_id}")

    def send_command(self, command: str) -> str:
        if self._logging:
            logging.info(f"Sending command '{command}' to server {self.base_url} with ID {self.server_id}")
            
        try:
            response = self.session.get(f"{self.base_url}/Console/Execute?serverId={self.server_id}&command={command}")
            if self._logging:
                logging.info(f"Command '{command}' executed successfully with response status: {response.status_code}")
                
            return response.text
        
        except Exception as e:
            if self._logging:
                logging.error(f"Error executing command '{command}': {e}")
            raise

    def get_logs(self) -> str:
        temp_dir = tempfile.gettempdir()
        logs = [file for file in os.listdir(temp_dir) if file.startswith("IW4MWrapper.py") and file.endswith(".log")]

        if not logs:
            logging.exception("No log files found")

        files = sorted(logs, key=lambda file: os.path.getctime(os.path.join(temp_dir, file)), reverse=True)
        path = os.path.join(temp_dir, files[0])

        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error reading log file: {e}")  
            return f"Error reading log file: {e}"   

    def color_handler(self, color) -> str:
        if color == None:
            return 
        color = color.lower()
        colors = {
            "black": "^0", "red": "^1", "green": "^2", 
            "yellow": "^3","dblue": "^4","lblue": "^5", 
            "pink": "^6", "white": "^7", "gray": "^8", 
            "brown": "^9", "blink": "^F", "box": "^HH"
        }
        return colors.get(color, "")
    
    class PlayerUtils:
        def __init__(self, wrapper) -> None:
            self.wrapper = wrapper
        
        def read_chat(self) -> list:
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

        def get_players(self) -> list:
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

        def info(self, player: str) -> dict:
            info = {}
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/{player}").text
            soup = bs(response, 'html.parser')

            name = soup.find('span', class_='font-size-20 font-weight-medium text-force-break')
            info['name'] = name.find('colorcode').text

            guid = soup.find('div', class_='text-muted', id='altGuidFormatsDropdown')
            info['guid'] = guid.text

            ip_div = soup.find('div', class_='align-self-center align-self-md-start d-flex flex-row')
            info['ip_address'] = ip_div.find('span', class_="text-muted mr-5").text

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
        
        def chat_history(self, player: str, count: int) -> list:
            messages = []
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Meta/{player}?offset=30&count={count}").text
            soup = bs(response, 'html.parser')

            entries = soup.find_all('div', class_='profile-meta-entry')

            for entry in entries:
                message = entry.find('span', class_='client-message')
                if message:
                    messages.append(message.text.strip())    

            return messages
        
        def name_changes(self, player: str) -> list:
            name_changes = []
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Profile/{player}?metaFilterType=AliasUpdate").text
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

        def administered_penalties(self, player: str) -> list:
            pass

        def received_penalties(self, player: str) -> list:
            pass

        def search_player(self, chat: bool = False, player: str = None, ip_address: str = None, guid: str = None, perm_level: str = None, 
                          game: str = None, connected_since: str = None, older_first: bool = False):
            pass


    class Commands:
        def __init__(self, wrapper) -> None:
            self.wrapper = wrapper

        #  Command List   #
        def setlevel(self, player: str, level: str):
            return self.wrapper.send_command(f"!setlevel {player} {level}")

        def change_map(self, map_name: str):
            return self.wrapper.send_command(f"!map {map_name}")
        
        def ban(self, player: str, reason: str):
            return self.wrapper.send_command(f"!ban {player} {reason}")
            
        def unban(self, player: str, reason: str):
            return self.wrapper.send_command(f"!unban {player} {reason}")

        def fastrestart(self):
            return self.wrapper.send_command("!fastrestart")

        def maprotate(self):
            return self.wrapper.send_command("!mr")
        
        def requesttoken(self):
            return self.wrapper.send_command("!requesttoken")
        
        def clearallreports(self):
            return self.wrapper.send_command("!clearallreports")
        
        def alias(self, player: str):
            return self.wrapper.send_command(f"!alias {player}")

        def whoami(self):
            return self.wrapper.send_command("!whoami")
        
        def warn(self, player: str, reason: str):
            return self.wrapper.send_command(f"!warn {player} {reason}")

        def warnclear(self, player: str):
            return self.wrapper.send_command(f"!warnclear {player}")

        def kick(self, player: str):
            return self.wrapper.send_command(f"!kick {player}")

        def tempban(self, player: str, duration: str, reason: str):
            return self.wrapper.send_command(f"!tempban {player} {duration} {reason}")

        def usage(self):
            return self.wrapper.send_command("!usage")
        
        def uptime(self):
            return self.wrapper.send_command("!uptime")
        
        def flag(self, player: str, reason: str):
            return self.wrapper.send_command(f"!flag {player} {reason}")
        
        def unflag(self, player: str, reason: str):
            return self.wrapper.send_command(f"!unflag {player} {reason}")

        def mask(self):
            return self.wrapper.send_command("!mask")
        
        def baninfo(self, player: str):
            return self.wrapper.send_command(f"!baninfo {player}")

        def setpassword(self, password: str):
            return self.wrapper.send_command(f"!setpassword {password}")

        def runas(self, command):
            return self.wrapper.send_command(f"!runas {command}")
        
        def addnote(self, player, note):
            return self.wrapper.send_command(f"!addnote {player} {note}")
        
        def list_players(self):
            return self.wrapper.send_command("!list")
        
        def plugins(self):
            return self.wrapper.send_command("!plugins")
        
        def reports(self):
            return self.wrapper.send_command("!reports")
        
        def offlinemessages(self):
            return self.wrapper.send_command("!offlinemessages")
        
        def sayall(self, message, color=None):
            return self.wrapper.send_command(f"!sayall {self.wrapper.color_handler(color)}{message}")
        
        def say(self, message, color=None):
            return self.wrapper.send_command(f"!say {self.wrapper.color_handler(color)}{message}")

        def rules(self):
            return self.wrapper.send_command("!rules")
        
        def ping(self):
            return self.wrapper.send_command("!ping")
        
        def setgravatar(self, email):
            return self.wrapper.send_command(f"!setgravatar {email}")
        
        def help(self):
            return self.wrapper.send_command("!help")
        
        def admins(self):
            return self.wrapper.send_command("!admins")
        
        def privatemessage(self, player, message):
            return self.wrapper.send_command(f"!privatemessage {player} {message}")
        
        def readmessage(self):
            return self.wrapper.send_command("!readmessage")
        
        def report(self, player, reason): 
            return self.wrapper.send_command(f"!report {player} {reason}")

        #  Script Plugin  #
        def giveweapon(self, player, weapon):
            return self.wrapper.send_command(f"!giveweapon {player} {weapon}")
        
        def takeweapons(self, player):
            return self.wrapper.send_command(f"!takeweapons {player}")
        
        def lockcontrols(self, player):
            return self.wrapper.send_command(f"!lockcontrols {player}")

        def noclip(self):
            return self.wrapper.send_command("!noclip")
        
        def alert(self, player, message):
            return self.wrapper.send_command(f"!alert {player} {message}")
        
        def gotoplayer(self, player):
            return self.wrapper.send_command(f"!gotoplayer {player}")
        
        def playertome(self, player):
            return self.wrapper.send_command(f"!playertome {player}")
        
        def goto(self, x, y ,z):
            return self.wrapper.send_command(f"!goto {x} {y} {z}")
        
        def kill(self, player):
            return self.wrapper.send_command(f"!kill {player}")

        def setspectator(self, player):
            return self.wrapper.send_command(f"!setspectator {player}")
        
        def whitelistvpn(self, player):
            return self.wrapper.send_command(f"!whitelistvpn {player}")

        def disallowvpn(self, player):
            return self.wrapper.send_command(f"!disallowvpn {player}")
        
        def bansubnet(self, subnet):
            return self.wrapper.send_command(f"!bansubnet {subnet}")
        
        def unbansubnet(self, subnet):
            return self.wrapper.send_command(f"!unbansubnet {subnet}")
        
        def switchteam(self, player):
            return self.wrapper.send_command(f"!switchteam {player}")

        #      Login      #
        def login(self, password):
            return self.wrapper.send_command(f"!login {password}")

        #       Mute      #
        def mute(self, player, reason):
            return self.wrapper.send_command(f"!mute {player} {reason}")
        
        def muteinfo(self, player):
            return self.wrapper.send_command(f"!muteinfo {player}")
        
        def tempmute(self, player, duration, reason):
            return self.wrapper.send_command(f"!tempmute {player} {duration} {reason}")
        
        def unmute(self, player, reason):
            return self.wrapper.send_command(f"!unmute {player} {reason}")
        
        #  Simple Status  #
        def mostkills(self):
            return self.wrapper.send_command("!mostkills")
        
        def mostplayed(self):
            return self.wrapper.send_command("!mostplayed")
        
        def rxs(self):
            return self.wrapper.send_command("!rxs")
        
        def topstats(self):
            return self.wrapper.send_command("!topstats")
        
        def stats(self, player=None):
            if player == None:
                return self.wrapper.send_command("!x")
            else:
                return self.wrapper.send_command(f"!x {player}")

class AsyncIW4MWrapper():
    def __init__(self, base_url: str, server_id: int, cookie: str, _logging: bool) -> None:
        self.base_url = base_url
        self.server_id = server_id
        self.cookie = cookie
        self._logging = _logging

        if self._logging:
            logging.basicConfig(
                filename=os.path.join(os.path.dirname(__file__), 'tmp', 'iw4mAdmin.log'),
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
            )
            logging.info(f"Initialized AsyncIW4MWrapper for server {self.base_url} with ID {self.server_id}")

    async def send_command(self, command) -> str:
        if self._logging:
            logging.info(f"Sending command '{command}' to server {self.base_url} with ID {self.server_id}")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.base_url}/Console/Execute?serverId={self.server_id}&command={command}",
                    headers={"Cookie": self.cookie}
                ) as response:
                    res = await response.text()
                    if response.status == 200:
                        logging.info(f"Command '{command}' executed successfully with response status: {response.status}")
                        return f"Success: {res}" 
                    elif response.status == 400:
                        logging.error(f"Command '{command}' failed - Player not found. Status: {response.status}")
                        return f"Error: Player not found (Status {response.status})"
                    else:
                        logging.error(f"Command '{command}' failed with response status: {response.status}")
                        return f"Error: {res} (Status {response.status})"
            
            except aiohttp.ClientError as e:
                if self._logging:
                    logging.error(f"Error executing command '{command}': {e}")
                raise


    async def get_logs(self) -> str:
        temp_dir = tempfile.gettempdir()
        logs = [file for file in os.listdir(temp_dir) if file.endswith(".log")]

        if not logs:
            logging.exception("No log files found")
            return "No log files found"
        
        files = sorted(logs, key=lambda file: os.path.getctime(os.path.join(temp_dir, file)), reverse=True)
        path = os.path.join(temp_dir, files[0])

        try:
            async with aiofiles.open(path, 'r') as f:
                contents = await f.read()
                return contents
        except Exception as e:
            logging.error(f"Error reading log file: {e}")
            return f"Error reading log file: {e}"

    async def color_handler(self, color: str) -> str:
        if color is None:
            return ""
        color = color.lower()
        colors = {
            "black": "^0", "red": "^1", "green": "^2", 
            "yellow": "^3","dblue": "^4","lblue": "^5", 
            "pink": "^6", "white": "^7", "gray": "^8", 
            "brown": "^9", "blink": "^F"
        }
        return await colors.get(color, "")
    
    class PlayerUtils:
        def __init__(self, wrapper):
            self.wrapper = wrapper

        async def read_chat(self):
            pass


    class Commands:
        def __init__(self, wrapper):
            self.wrapper = wrapper

        #  Command List   #
        async def setlevel(self, player, level):
            return await self.wrapper.send_command(f"!setlevel {player} {level}")

        async def change_map(self, map_name):
            return await self.wrapper.send_command(f"!map {map_name}")
    
        async def ban(self, player, reason):
            return await self.wrapper.send_command(f"!ban {player} {reason}")
        
        async def unban(self, player, reason):
            return await self.wrapper.send_command(f"!unban {player} {reason}")

        async def fastrestart(self):
            return await self.wrapper.send_command("!fastrestart")

        async def maprotate(self):
            return await self.wrapper.send_command("!mr")
    
        async def requesttoken(self):
            return await self.wrapper.send_command("!requesttoken")
    
        async def clearallreports(self):
            return await self.wrapper.send_command("!clearallreports")
    
        async def alias(self, player):
            return await self.wrapper.send_command(f"!alias {player}")

        async def whoami(self):
            return await self.wrapper.send_command("!whoami")
    
        async def warn(self, player, reason):
            return await self.wrapper.send_command(f"!warn {player} {reason}")

        async def warnclear(self, player):
            return await self.wrapper.send_command(f"!warnclear {player}")

        async def kick(self, player):
            return await self.wrapper.send_command(f"!kick {player}")

        async def tempban(self, player, duration, reason):
            return await self.wrapper.send_command(f"!tempban {player} {duration} {reason}")

        async def usage(self):
            return await self.wrapper.send_command("!usage")
    
        async def uptime(self):
            return await self.wrapper.send_command("!uptime")
    
        async def flag(self, player, reason):
            return await self.wrapper.send_command(f"!flag {player} {reason}")
    
        async def unflag(self, player, reason):
            return await self.wrapper.send_command(f"!unflag {player} {reason}")

        async def mask(self):
            return await self.wrapper.send_command("!mask")
    
        async def baninfo(self, player):
            return await self.wrapper.send_command(f"!baninfo {player}")

        async def setpassword(self, password):
            return await self.wrapper.send_command(f"!setpassword {password}")

        async def runas(self, command):
            return await self.wrapper.send_command(f"!runas {command}")
    
        async def addnote(self, player, note):
            return await self.wrapper.send_command(f"!addnote {player} {note}")
    
        async def list_players(self):
            return await self.wrapper.send_command("!list")
    
        async def plugins(self):
            return await self.wrapper.send_command("!plugins")
    
        async def reports(self):
            return await self.wrapper.send_command("!reports")

        async def offlinemessages(self):
            return await self.wrapper.send_command("!offlinemessages")
    
        async def sayall(self, message, color=None):
            return await self.wrapper.send_command(f"!sayall {await self.wrapper.color_handler(color)}{message}")
    
        async def say(self, message, color=None):
            return await self.wrapper.send_command(f"!say {await self.wrapper.color_handler(color)}{message}")
        
        async def rules(self):
            return await self.wrapper.send_command("!rules")
    
        async def ping(self):
            return await self.wrapper.send_command("!ping")
    
        async def setgravatar(self, email):
            return await self.wrapper.send_command(f"!setgravatar {email}")
    
        async def help(self):
            return await self.wrapper.send_command("!help")
    
        async def admins(self):
            return await self.wrapper.send_command("!admins")
    
        async def privatemessage(self, player, message):
            return await self.wrapper.send_command(f"!privatemessage {player} {message}")
    
        async def readmessage(self):
            return await self.wrapper.send_command("!readmessage")
    
        async def report(self, player, reason): 
            return await self.wrapper.send_command(f"!report {player} {reason}")
        
        #  Script Plugin  #
        async def giveweapon(self, player, weapon):
            return await self.wrapper.send_command(f"!giveweapon {player} {weapon}")
    
        async def takeweapons(self, player):
            return await self.wrapper.send_command(f"!takeweapons {player}")
    
        async def lockcontrols(self, player):
            return await self.wrapper.send_command(f"!lockcontrols {player}")

        async def noclip(self):
            return await self.wrapper.send_command("!noclip")
    
        async def alert(self, player, message):
            return await self.wrapper.send_command(f"!alert {player} {message}")
    
        async def gotoplayer(self, player):
            return await self.wrapper.send_command(f"!gotoplayer {player}")
    
        async def playertome(self, player):
            return await self.wrapper.send_command(f"!playertome {player}")
    
        async def goto(self, x, y ,z):
            return await self.wrapper.send_command(f"!goto {x} {y} {z}")
    
        async def kill(self, player):
            return await self.wrapper.send_command(f"!kill {player}")

        async def setspectator(self, player):
            return await self.wrapper.send_command(f"!setspectator {player}")
    
        async def whitelistvpn(self, player):
            return await self.wrapper.send_command(f"!whitelistvpn {player}")

        async def disallowvpn(self, player):
            return await self.wrapper.send_command(f"!disallowvpn {player}")
    
        async def bansubnet(self, subnet):
            return await self.wrapper.send_command(f"!bansubnet {subnet}")
    
        async def unbansubnet(self, subnet):
            return await self.wrapper.send_command(f"!unbansubnet {subnet}")
    
        async def switchteam(self, player):
            return await self.wrapper.send_command(f"!switchteam {player}")
        
        #      Login      #
        async def login(self, password):
            return await self.wrapper.send_command(f"!login {password}")

        #       Mute      #
        async def mute(self, player, reason):
            return await self.wrapper.send_command(f"!mute {player} {reason}")
    
        async def muteinfo(self, player):
            return await self.wrapper.send_command(f"!muteinfo {player}")
    
        async def tempmute(self, player, duration, reason):
            return await self.wrapper.send_command(f"!tempmute {player} {duration} {reason}")
    
        async def unmute(self, player, reason):
            return await self.wrapper.send_command(f"!unmute {player} {reason}")
        
        #  Simple Status  #
        async def mostkills(self):
            return await self.wrapper.send_command("!mostkills")
    
        async def mostplayed(self):
            return await self.wrapper.send_command("!mostplayed")
    
        async def rxs(self):
            return await self.wrapper.send_command("!rxs")

        async def topstats(self):
            return await self.wrapper.send_command("!topstats")
    
        async def stats(self, player=None):
            if player is None:
                return await self.wrapper.send_command("!x")
            else:
                return await self.wrapper.send_command(f"!x {player}")
