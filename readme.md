# IW4M-Admin API Wrapper 🚀
> A Python wrapper designed for the [IW4M-Admin](https://github.com/RaidMax/IW4M-Admin) server administration tool 🛠️

This wrapper provides an easy way to interact with IW4M-Admin servers, enabling server commands, retrieving player information, and managing penalties through Python scripts. It supports both synchronous and asynchronous usage

---

## Features 🌟

- **Command Execution**: Perform in-game commands like kick, ban, change map, and more
- **Player Management**: Fetch player stats, connection history, and chat history
- **Penalty Management**: Issue and track penalties (warnings, bans, etc)
- **Real-time Interaction**: Send messages to players and retrieve chat logs
- **Async Support**: Full asynchronous support


---

## Getting Started

### Initialization ⚙️
Create an instance of the `IW4MWrapper` class by providing your server details and authentication cookie

```python
from iw4m import IW4MWrapper

iw4m = IW4MWrapper(
    base_url="http://your.iw4m.com",       # Replace with your server address 
    server_id=1234567890,                  # Replace with your server ID
    cookie=".AspNetCore.Cookies=CfB_u..."  # Replace with your .AspNetCore cookie
)
```

### Commands 📜
Use the Commands class to interact with the server

```python
# Create an instance of Commands
commands = iw4m.Commands(iw4m)

# Example usage
response = commands.kick("<player>") 
print(response)

response = commands.ban("<player>", "<reason>")
print(response)

response = commands.tempban("<player>", "<duration>", "<reason>")
print(response)
```

---

### Initialization (Async) 🌐
Create an instance of the AsyncIW4MWrapper class by providing your cookie, server address, and server ID

```python
from iw4m import AsyncIW4MWrapper
import asyncio

iw4m = AsyncIW4MWrapper(
    base_url="http://your.iw4m.com",       # Replace with your server address 
    server_id=1234567890,                  # Replace with your server ID
    cookie=".AspNetCore.Cookies=CfB_u..."  # Replace with your .AspNetCore cookie
)
```

### Commands (Async) ⚡
Use the Commands class to interact with the server, all methods are asynchronous and should be awaited
```python
# Create an instance of Commands
commands = iw4m.Commands(iw4m)

async def main():
    # Example usage
    response = await commands.kick("<player>") 
    print(response)

    response = await commands.ban("<player>", "<reason>")
    print(response)

    response = await commands.tempban("<player>", "<duration>", "<reason>")
    print(response)

asyncio.run(main())
```

---

## Come Play on Brownies SND 🍰
### Why Brownies? 🤔
- **Stability:** Brownies delivers a consistent, lag-free experience, making it the perfect choice for players who demand uninterrupted action
- **Community:** The players at Brownies are known for being helpful, competitive, and fun—something Orion can only dream of
- **Events & Features:** Brownies is constantly running unique events and offers more server-side customization options than Orion, ensuring every game feels fresh

---

#### [Brownies Discord](https://discord.gg/FAHB3mwrVF) | [Brownies IW4M](http://141.11.196.83:1624/) | Made With ❤️ By Budiworld