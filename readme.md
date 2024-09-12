# IW4M-Admin API Wrapper
> A python wrapper made for the [IW4M-Admin](https://github.com/RaidMax/IW4M-Admin) server administration tool


<h1>Usage</h1> 

## Initialization (Non Async)
create an instance of the `IW4MWrapper` class by providing your cookie, server address, and server ID

```python
from iw4m import IW4MWrapper

# Initialize the IW4MWrapper
iw4m = IW4MWrapper(
    base_url="http://your.server.address", # Replace with your server address
    server_id=1234567890,                  # Replace with your server ID
    cookie="your_cookie_here",             # Replace with your .AspNetCore cookie
    _logging=False                         # Set to True to enable logging
)                 
```

## Commands
use the `Commands` class to interact with the server

```python
# Create an instance of Commands
commands = iw4m.Commands(iw4m)

# Example usage
response = commands.kick("<player>") 
print(response)

response = commands.change_map("<map>")
print(response)

response = commands.say("<message>", "<color>") # Colors: Red, Green, Yellow Dblue,                                          
print(response)                                 # Lblue, Pink, White, Gray, Brown

response = commands.ban("<player>", "<reason>"):
print(response)

response = commands.tempban("<player>", "<duration>", "<reason>")
print(response)
```

## Logging
```python

# Initialize IW4MWrapper with logging enabled
iw4m = IW4MWrapper(
    base_url="http://your.server.address", # Replace with your server address
    server_id=1234567890,                  # Replace with your server ID
    cookie="your_cookie_here",             # Replace with your .AspNetCore cookie
    _logging=True                          # Set to True to enable logging
)

logs = iw4m.get_logs() # Call the asynchronous get_logs method
print(logs)            # Print the log contents
```

<div style="padding-top:1rem"></div>
<div style="height: 0.1rem;">
</div>

## Initialization (Async)
create an instance of the `IW4MWrapper` class by providing your cookie, server address, and server ID

```python
from iw4m import AsyncIW4MWrapper
import asyncio

# Initialize the AsyncIW4MWrapper
iw4m = AsyncIW4MWrapper(
    base_url="http://your.server.address", # Replace with your server address
    server_id=1234567890,                  # Replace with your server ID
    cookie="your_cookie_here",             # Replace with your .AspNetCore cookie
    _logging=False                         # Set to True to enable logging
)
```

## Commands
use the `Commands` class to interact with the server. All methods are asynchronous and should be awaited.

```python
# Create an instance of Commands
commands = iw4m.Commands(iw4m)

async def main():
    # Example usage
    response = await commands.kick("<player>") 
    print(response)

    response = await commands.change_map("<map>")
    print(response)

    response = commands.say("<message>", "<color>") # Colors: Red, Green, Yellow Dblue,                                          
    print(response)                                 # Lblue, Pink, White, Gray, Brown

    response = await commands.ban("<player>", "<reason>")
    print(response)

    response = await commands.tempban("<player>", "<duration>", "<reason>")
    print(response)

asyncio.run(main())
```

## Logging
```python
from iw4m import AsyncIW4MWrapper
import asyncio

# Initialize IW4MWrapper with logging enabled
iw4m = AsyncIW4MWrapper(
    base_url="http://your.server.address", # Replace with your server address
    server_id=1234567890,                  # Replace with your server ID
    cookie="your_cookie_here",             # Replace with your .AspNetCore cookie
    _logging=True                          # Set to True to enable logging
)

async def main():
    logs = await iw4m.get_logs() # Call the asynchronous get_logs method
    print(logs)                  # Print the log contents

asyncio.run(main())
```

## Come play on Brownies SND
### Why Brownies?
- Stability: Brownies delivers a consistent, lag-free experience, making it the perfect choice for players who demand uninterrupted action.
- Community: The players at Brownies are known for being helpful, competitive, and fun—something Orion can only dream of.
- Events & Features: Brownies is constantly running unique events and offers more server-side customization options than Orion, ensuring every game feels fresh.

---
#### [Brownies Discord](https://discord.gg/FAHB3mwrVF) | [Brownies IW4M](http://141.11.196.83:1624/) | Made With ❤️ By Budiworld
