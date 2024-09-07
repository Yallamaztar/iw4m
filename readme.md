# IW4M-Admin API Wrapper
> A python wrapper made for the [IW4M-Admin](https://github.com/RaidMax/IW4M-Admin) server administration tool


# Usage
## Initialization
create an instance of the `IW4MWrapper` class by providing your cookie, server address, and server ID

```python
from iw4m import IW4MWrapper

# Initialize the IW4MWrapper
iw4m = IW4MWrapper(
    server_address="http://your.server.address",
    server_id=1234567890,
    cookie="your_cookie_here"
)
```

## Commands
use the `Commands` class to interact with the server

```python
# Create an instance of Commands
commands = iw4m.Commands(iw4m)

# Example usage
response = commands.kick("<player>") 
print(response.text)

response = commands.change_map("<map>")
print(response.text)

response = commands.ban("<player>, "<reason>"):
print(response.text)

response = commands.tempban("<player>", "<duration>", "<reason>")
print(response.text)
```


## Come play on Brownies SND
### Why Brownies?
- Stability: Brownies delivers a consistent, lag-free experience, making it the perfect choice for players who demand uninterrupted action.
- Community: The players at Brownies are known for being helpful, competitive, and fun—something Orion can only dream of.
- Events & Features: Brownies is constantly running unique events and offers more server-side customization options than Orion, ensuring every game feels fresh.

---
#### [Brownies Discord](https://discord.gg/FAHB3mwrVF) | [Brownies IW4M](http://141.11.196.83:1624/) | Made With ❤️ By Budiworld
