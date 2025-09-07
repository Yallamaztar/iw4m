from iw4m import IW4MWrapper
from collections import deque
import os, time

iw4m = IW4MWrapper(
    base_url  = os.environ['IW4M_URL'],
    server_id = os.environ['IW4M_ID'],
    cookie    = os.environ['IW4M_HEADER']
)

server = iw4m.Server(iw4m)
commands = iw4m.Commands(iw4m)

def custom_command_example() -> None:
    commands.say("I got called from a custom command!")

def run(command_name: str = "custom_command") -> None:
    last_seen = deque(maxlen=50)
    while True:
        audit_log = server.get_recent_audit_log()
        if (audit_log['origin'], audit_log['data'], audit_log['time']) in last_seen:
            time.sleep(0.5); continue 
        if audit_log['origin'] == server.logged_in_as():
            time.sleep(0.5); continue

        if audit_log['data'].startswith(f"!{command_name}"):
            custom_command_example(audit_log)

        last_seen.append((audit_log['origin'], audit_log['data'], audit_log['time']))

if __name__ == '__main__':
    run()
