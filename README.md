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

### Installation 📦
To install the IW4M-Admin API Wrapper you can use pip:

#### Windows
```bash 
pip install iw4m
```

#### Linux/Mac
```bash
pip3 install iw4m
```

---

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
All available commands can be found at your server's help page, and the function names in the Commands class match the command names listed there.


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
All available commands can be found at your server's help page, and the function names in the Commands class match the command names listed there.


---

## GameUtils Class 🎮
The `GameUtils` class provides utility functions for interacting with the IW4M-Admin server
### Methods
`send_command(command: str)`

**executes an iw4m-admin console command and returns the response**

    Parameters:
        command (str): The command to execute

    Returns:
        (str): Response from the server

    Raises:
        Exception if the request fails

`color_handler(color: str)`

**Converts a color name to its corresponding color code used by the T6 server**

    Parameters:
        color (str): The color name (e.g., "red", "green")

    Returns:
        (str): The color code for the specified color, or an empty string if the color is unknown

`read_chat()`

**Retrieves chat messages from the server**

    Returns:
        (list): A list of tuples, each containing the sender's name and their message

```find_player(name: str = "", xuid: str = "", count: int = 1, offset: int = 0, direction: int = 0)```

**Finds players on the server by name or XUID**

    Parameters:
        name (str, optional): The player's name
        xuid (str, optional): The player's XUID
        count (int, optional): Number of players to return (default is 1)
        offset (int, optional): Offset for pagination (default is 0)
        direction (int, optional): Search direction (default is 0)

    Returns:
        (str): The response from the server containing player information

`get_players()`

**Retrieves a list of players currently connected to the server**

    Returns:
        (list): A list of tuples, each containing a player's name and their link


---

## Player Class 👾
The `Player` class provides methods for retrieving and managing player information

### Methods
`stats(client_id: str)`

**Fetches the statistics for a specific player**

    Parameters:
        client_id (str): The client ID of the player
    Returns:
        (str): The response from the server containing player statistics

`info(client_id: str)`

**Retrieves detailed information about a player**

    Parameters:
        client_id (str): The client ID of the player
    Returns:
        (dict): A dictionary containing the player's name, GUID, IP address, and statistics

`chat_history(client_id: str, count: int)`

**Fetches the chat history for a specified client id**

    Parameters:
        client_id (str): The player's client_id 
        count (int): The number of messages to retrieve
    Returns:
        (list): A list of chat messages sent by the player
 
`name_changes(client_id: str)`

**Retrieves the name changes for a specified client id**

    Parameters:
        client_id (str): The player's client_id 
    Returns:
        (list): A list of tuples containing the old username, IP address, and date of change

`administered_penalties(client_id: int, count: int = 30)`

**Retrieves penalties administered to players**

    Parameters:
        client_id (int): The client ID of the player
        count (int, optional): The number of penalties to return (default is 30)
    Returns:
        (list): A list of dictionaries containing details about the administered penalties

`received_penalties(client_id: int, count: int = 30)`

**Retrieves penalties received by the player**

    Parameters:
        client_id (int): The client ID of the player
        count (int, optional): The number of penalties to return (default is 30)
    Returns:
        (list): A list of dictionaries containing details about the received penalties

`connection_history(client_id: int, count: int = 30)`

**Fetches the connection history for a specified player**

    Parameters:
        client_id (int): The client ID of the player
        count (int, optional): The number of connection entries to return (default is 30)
    Returns:
        (list): A list of dictionaries containing connection history details

`permissions(client_id: int, count: int = 30)`

**Retrieves the permission levels for a specified player**

    Parameters:
        client_id (int): The client ID of the player
        count (int, optional): The number of permission entries to return (default is 30)
    Returns:
        (list): A list of dictionaries containing permission change details


---

## Come Play on Brownies SND 🍰
### Why Brownies? 🤔
- **Stability:** Brownies delivers a consistent, lag-free experience, making it the perfect choice for players who demand uninterrupted action
- **Community:** The players at Brownies are known for being helpful, competitive, and fun—something Orion can only dream of
- **Events & Features:** Brownies is constantly running unique events and offers more server-side customization options than Orion, ensuring every game feels fresh

---

#### [Brownies Discord](https://discord.gg/FAHB3mwrVF) | [Brownies IW4M](http://141.11.196.83:1624/) | Made With ❤️ By Budiworld
