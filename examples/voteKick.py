# ---------------------------- #
# Vote Kick Plugin
# Author:  Budiworld
# GitHub:  https://github.com/Yallamaztar/iw4m
# ---------------------------- #

import os, time
import threading
from iw4m import IW4MWrapper

class VoteKickPlugin:
    def __init__(self):
        self.voted_yes = set()
        self.voted_no  = set()
        self.in_progress = False

        self.iw4m = IW4MWrapper(
            base_url=os.environ['IW4M_URL'],
            server_id=os.environ['IW4M_ID'],
            cookie=os.environ['IW4M_HEADER']
        )

        self.server   = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)
        self.player   = self.iw4m.Player(self.iw4m) 

    def process_vote(self, auditlog: dict): 
        command = auditlog.get('data', '') 
        voter = auditlog.get('origin')
        
        command.lower()
        if command.startswith("!yes") and voter not in self.voted_yes:
            self.voted_yes.add(voter)
            self.voted_no.discard(voter)
            self.commands.say(f"^7{voter} voted ^5YES")
        elif command.startswith("!no") and voter not in self.voted_no:
            self.voted_no.add(voter)
            self.voted_yes.discard(voter)
            self.commands.say(f"^7{voter} voted ^1NO")

    def collect_votes(self, duration: int):
        start_time = time.time()
        while time.time() - start_time < duration:
            auditlog = self.server.get_recent_audit_log()
            self.process_vote(auditlog)
            time.sleep(0.5)

    def clear_votes(self):
        self.voted_yes.clear()
        self.voted_no.clear()

    def start_vote(self, target: str, duration: int = 30):
        self.in_progress = True
        self.clear_votes()

        players = len(self.server.get_players())
        min_requirement = players // 2 - 1

        self.commands.say(f"^7Vote kick started for ^5{target.capitalize()}")
        self.commands.say("^7Type ^5!yes ^7to vote YES or ^1!no ^7to vote NO")
        self.commands.say(f"^7Minium votes required: {min_requirement}")

        self.collect_votes(duration)
     
        yes_count = len(self.voted_yes)
        no_count  = len(self.voted_no)
        self.commands.say(f"^7Vote ended: {yes_count} YES vs {no_count} NO")        

        if yes_count > no_count and yes_count >= min_requirement:
            self.commands.say(f"^5Vote kick passed. Kicking {target.capitalize()}.")
            self.commands.kick(target, "Vote Kick Passed")
        else:
            self.commands.say(f"^7Not enough players voted")

        self.in_progress = False

    def monitor_auditlogs(self):
        while True:
            auditlog = self.server.get_recent_audit_log()
            command  = auditlog.get('data', '')
            origin   = auditlog.get('origin', '')

            if command.startswith(("!votekick", "!vk")):
                if self.in_progress:
                    self.commands.privatemessage(origin, "^7A vote is ^1already ^7in progress")
                    continue

                parts = command.split()
                if len(parts) < 2:
                    self.commands.privatemessage(origin, "Usage: !votekick ^5<player>")
                    continue

                target = parts[1]
                threading.Thread(target=self.start_vote, args=(target,), daemon=True).start()
            
            time.sleep(1)

    def start(self):
        self.monitor_auditlogs()

if __name__ == '__main__':
    VoteKickPlugin().start()
