# ---------------------------- #
# Map Manager Plugin
# Author:  Budiworld
# GitHub:  https://github.com/Yallamaztar/iw4m
# ---------------------------- #

import os, time
from iw4m import IW4MWrapper

class MapManagerPlugin:
    def __init__(self):
        self.last_command = set()
        self.iw4m = IW4MWrapper(
            base_url=os.environ['IW4M_URL'],
            server_id=os.environ['IW4M_ID'],
            cookie=os.environ['IW4M_HEADER']
        )

        self.server   = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)
        self.player   = self.iw4m.Player(self.iw4m) 

    def extract_data(self, auditlog: dict) -> list:
        return auditlog.get('data', '').strip(), auditlog.get('origin', ''), auditlog.get('origin_rank', '')

    def monitor_auditlogs(self):
        while True:
            auditlog = self.server.get_recent_audit_log()
            command, origin, rank = self.extract_data(auditlog)

            is_allowed_command = command.startswith(("!map", "!m"))
            is_authorized = (rank == "SeniorAdmin" or origin == "[ACOG]budiwrld")
            is_new_command = (origin, command) not in self.last_command

            if is_allowed_command and is_authorized and is_new_command:
                self.last_command.clear()
                self.server.send_command(command)
                self.last_command.add((origin, command))

            time.sleep(0.5)

    def start(self):
        self.monitor_auditlogs()

if __name__ == '__main__':
    MapManagerPlugin().start()