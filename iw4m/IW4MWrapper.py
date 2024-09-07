
from requests import sessions

class IW4MWrapper():
    def __init__(self, server_address: str, server_id: int, cookie: str):
        self.server_address = server_address
        self.server_id = server_id
        self.session = sessions.Session()
        self.session.headers.update({ "Cookie": cookie })


    def send_command(self, command):
        return self.session.get(f"{self.server_address}/Console/Execute?serverId={self.server_id}&command={command}")

    class Commands:
        def __init__(self, wrapper):
            self.wrapper = wrapper

        #-----------------#
        #  Command List   #
        #-----------------#

        def setlevel(self, player, level):
            return self.wrapper.send_command(f"!setlevel {player} {level}")

        def change_map(self, map_name):
            return self.wrapper.send_command(f"!map {map_name}")
        
        def ban(self, player, reason):
            return self.wrapper.send_command(f"!ban {player} {reason}")
            
        def unban(self, player, reason):
            return self.wrapper.send_command(f"!unban {player} {reason}")

        def fastrestart(self):
            return self.wrapper.send_command("!fastrestart")

        def maprotate(self):
            return self.wrapper.send_command("!mr")
        
        def requesttoken(self):
            return self.wrapper.send_command("!requesttoken")
        
        def clearallreports(self):
            return self.wrapper.send_command("!clearallreports")
        
        def alias(self, player):
            return self.wrapper.send_command(f"!alias {player}")

        def whoami(self):
            return self.wrapper.send_command("!whoami")
        
        def warn(self, player, reason):
            return self.wrapper.send_command(f"!warn {player} {reason}")

        def warnclear(self, player):
            return self.wrapper.send_command(f"!warnclear {player}")

        def kick(self, player):
            return self.wrapper.send_command(f"!kick {player}")

        def tempban(self, player, duration, reason):
            return self.wrapper.send_command(f"!tempban {player} {duration} {reason}")

        def usage(self):
            return self.wrapper.send_command("!usage")
        
        def uptime(self):
            return self.wrapper.send_command("!uptime")
        
        def flag(self, player, reason):
            return self.wrapper.send_command(f"!flag {player} {reason}")
        
        def unflag(self, player, reason):
            return self.wrapper.send_command(f"!unflag {player} {reason}")

        def mask(self):
            return self.wrapper.send_command("!mask")
        
        def baninfo(self, player):
            return self.wrapper.send_command(f"!baninfo {player}")

        def setpassword(self, password):
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
        
        def sayall(self, message):
            return self.wrapper.send_command(f"!sayall {message}")
        
        def say(self, message):
            return self.wrapper.send_command(f"!say {message}")

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
        
        #-----------------#
        #  Script Plugin  #
        #-----------------#

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
        
        #-----------------#
        #      Login      #
        #-----------------#

        def login(self, password):
            return self.wrapper.send_command(f"!login {password}")
        
        #-----------------#
        #       Mute      #
        #-----------------#

        def mute(self, player, reason):
            return self.wrapper.send_command(f"!mute {player} {reason}")
        
        def muteinfo(self, player):
            return self.wrapper.send_command(f"!muteinfo {player}")
        
        def tempmute(self, player, duration, reason):
            return self.wrapper.send_command(f"!tempmute {player} {duration} {reason}")
        
        def unmute(self, player, reason):
            return self.wrapper.send_command(f"!unmute {player} {reason}")
        
        #-----------------#
        #  Simple Status  #
        #-----------------#

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
