
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
from requests import sessions
import aiohttp
import re
import json

class IW4MWrapper:
    def __init__(self, base_url: str, server_id: int, cookie: str):
        self.base_url = base_url 
        self.server_id = server_id
        self.session = sessions.Session()
        self.session.headers.update({ "Cookie": cookie })

    class Utils:
        def __init__(self, wrapper):
            self.wrapper = wrapper
        
        def does_role_exists(self, role: str):
            return role in self.wrapper.Server(self.wrapper).get_roles()
        
        def get_role_position(self, role: str):
            roles = self.wrapper.Server(self.wrapper).get_roles()
            return roles.index(role) if role in roles else -1

        def is_higher_role(self, role: str, role_to_check: str):
            roles = self.wrapper.Server(self.wrapper).get_roles()
            if role not in roles or role_to_check not in roles:
                return
            
            role_pos = roles.index(role)
            role_to_check_pos = roles.index(role_to_check)
            
            return role_pos < role_to_check_pos

        def is_lower_role(self, role: str, role_to_check: str):
            return not self.is_higher_role(role, role_to_check)
        
        def get_command_prefix(self):
            return self.wrapper.Server(self.wrapper).get_audit_logs()[0]['data'][0]

        def is_player_online(self, player_name: str):
            players = self.wrapper.Server(self.wrapper).get_players()
            return any(player['name'] == player_name for player in players)

        def get_player_count(self):
            return len(self.wrapper.Server(self.wrapper).get_players())
        
        def is_server_full(self):
            server_info = self.wrapper.Server(self.wrapper).info()
            return server_info['totalConnectedClients'] >= server_info['totalClientSlots']

        def get_online_players_by_role(self, role: str):
            players = []

            _players = self.wrapper.Server(self.wrapper).get_players()
            for player in _players:
                if player['role'].lower() == role.lower():
                    players.append(player)
            
            return players
        
        def find_admin(self, admin_name: str):
            admins = self.wrapper.Server(self.wrapper).get_admins()
            for admin in admins:
                if admin['name'].lower() == admin_name.lower():
                    return admin

    class Server:
        def __init__(self, wrapper):
            self.wrapper = wrapper

        def get_server_uptime(self):
            return self.wrapper.session.get(f"{self.wrapper.base_url}/Console/Execute?serverId=15253132414984&command=!uptime")

        def generate_login_token(self):
            return self.wrapper.session.get(f"{self.wrapper.base_url}/Action/GenerateLoginTokenAsync/").text

        def status(self):
            return self.wrapper.session.get(f"{self.wrapper.base_url}/api/status").json()
        
        def info(self):
            return self.wrapper.session.get(f"{self.wrapper.base_url}/api/info").json()
        
        def help(self):
            _help = {}
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Home/Help").text
            soup = bs(response, 'html.parser')
            
            command_list = soup.find('div', class_="command-assembly-container")
            if command_list:
                command_title = command_list.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                if command_title not in _help:
                    _help[command_title] = {}

                commands = command_list.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                for command in commands:
                    name = command.find('td', class_="font-weight-bold").text.strip()
                    alias = command.find_all('td')[1].text.strip()
                    description = command.find_all('td')[2].text.strip()
                    requires_target = command.find_all('td')[3].text.strip()
                    syntax = command.find_all('td')[4].text.strip()
                    min_level = command.find('td', class_="text-right").text.strip()

                    _help[command_title][name] = {
                        "alias": alias,
                        "description": description,
                        "requires_target": requires_target,
                        "syntax": syntax,
                        "min_level": min_level
                        }
            
            script_plugin = soup.find_all('div', class_="command-assembly-container")[1]
            if script_plugin:
                script_title = script_plugin.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                if script_title not in _help:
                    _help[script_title] = {}

                scripts = script_plugin.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                for script in scripts:
                    name = script.find('td', class_="font-weight-bold").text.strip()
                    alias = script.find_all('td')[1].text.strip()
                    description = script.find_all('td')[2].text.strip()
                    requires_target = script.find_all('td')[3].text.strip()
                    syntax = script.find_all('td')[4].text.strip()
                    min_level = script.find('td', class_="text-right").text.strip()

                    _help[script_title][name] = {
                        "alias": alias,
                        "description": description,
                        "requires_target": requires_target,
                        "syntax": syntax,
                        "min_level": min_level
                        }
            
            login = soup.find_all('div', class_="command-assembly-container")[2]
            if login:
                login_title = login.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                if login_title not in _help:
                    _help[login_title] = {}

                login_entries = login.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                for login_entry in login_entries:
                    name = login_entry.find('td', class_="font-weight-bold").text.strip()
                    alias = login_entry.find_all('td')[1].text.strip()
                    description = login_entry.find_all('td')[2].text.strip()
                    requires_target = login_entry.find_all('td')[3].text.strip()
                    syntax = login_entry.find_all('td')[4].text.strip()
                    min_level = login_entry.find('td', class_="text-right").text.strip()

                    _help[login_title][name] = {
                        "alias": alias,
                        "description": description,
                        "requires_target": requires_target,
                        "syntax": syntax,
                        "min_level": min_level
                        }

            mute = soup.find_all('div', class_="command-assembly-container")[3]
            if mute:
                mute_title = mute.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                if mute_title not in _help:
                    _help[mute_title] = {}

                mute_entries = mute.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                for mute_entry in mute_entries:
                    name = mute_entry.find('td', class_="font-weight-bold").text.strip()
                    alias = mute_entry.find_all('td')[1].text.strip()
                    description = mute_entry.find_all('td')[2].text.strip()
                    requires_target = mute_entry.find_all('td')[3].text.strip()
                    syntax = mute_entry.find_all('td')[4].text.strip()
                    min_level = mute_entry.find('td', class_="text-right").text.strip()

                    _help[mute_title][name] = {
                        "alias": alias,
                        "description": description,
                        "requires_target": requires_target,
                        "syntax": syntax,
                        "min_level": min_level
                        }

            simple_stats = soup.find_all('div', class_="command-assembly-container")[4]
            if simple_stats:
                simple_stats_title = simple_stats.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                if simple_stats_title not in _help:
                    _help[simple_stats_title] = {}

                simple_stats_entries = simple_stats.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                for simple_stats_entry in simple_stats_entries:
                    name = simple_stats_entry.find('td', class_="font-weight-bold").text.strip()
                    alias = simple_stats_entry.find_all('td')[1].text.strip()
                    description = simple_stats_entry.find_all('td')[2].text.strip()
                    requires_target = simple_stats_entry.find_all('td')[3].text.strip()
                    syntax = simple_stats_entry.find_all('td')[4].text.strip()
                    min_level = simple_stats_entry.find('td', class_="text-right").text.strip()

                    _help[simple_stats_title][name] = {
                        "alias": alias,
                        "description": description,
                        "requires_target": requires_target,
                        "syntax": syntax,
                        "min_level": min_level
                        }

            return _help
            
        def get_map_name(self): 
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/").text
            soup = bs(response, 'html.parser')

            map_div = soup.find('div', class_='col-12 align-self-center text-center text-lg-left col-lg-4')
            if map_div:
                spans = map_div.find_all('span')
                return spans[0].text

        def get_gamemode(self):
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/").text
            soup = bs(response, 'html.parser')

            map_div = soup.find('div', class_='col-12 align-self-center text-center text-lg-left col-lg-4')
            if map_div:
                spans = map_div.find_all('span')
                return spans[2].text

        def get_iw4m_version(self): 
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/").text
            soup = bs(response, 'html.parser')
            
            entries = soup.find_all('a', class_="sidebar-link")
            for entry in entries:
                span = entry.find('span', class_="text-primary")
                if span:
                    return span.text.strip()
        
        def logged_in_as(self):
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/").text
            soup = bs(response, 'html.parser')

            div = soup.find('div', class_="sidebar-link font-size-12 font-weight-light")
            if div:
                return div.find('colorcode').text.strip()
        
        def get_rules(self):
            rules = []

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/About").text
            soup = bs(response, 'html.parser')
            
            card_divs = soup.find_all('div', class_="card m-0 rounded")
            for card_div in card_divs:
                h5 = card_div.find('h5', class_="text-primary mt-0 mb-0")
                if h5:
                    divs = card_div.find_all('div', class_="rule")
                    for div in divs:
                        rules.append(div.text.strip())

            return rules
            
        def get_reports(self):
            reports = []

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Action/RecentReportsForm/").text
            soup = bs(response, 'html.parser')

            report_blocks = soup.find_all('div', class_='rounded bg-very-dark-dm bg-light-ex-lm mt-10 mb-10 p-10')
            for block in report_blocks:
                timestamp_tag = block.find('div', class_='font-weight-bold')
                timestamp = timestamp_tag.text.strip()

            entries = soup.find_all('div', class_="font-size-12")
            for entry in entries:
                origin_tag = entry.find('a')
                origin = origin_tag.text.strip()

                reason_tag = entry.find('span', class_='text-white-dm text-black-lm').find('colorcode')
                reason = reason_tag.text.strip()

                target_tag = entry.find('span', class_='text-highlight').find('a')
                target = target_tag.text.strip()

                reports.append({
                    'origin': origin,
                    'reason': reason,
                    'target': target,
                    'timestamp': timestamp
                })

            return reports

        def get_server_ids(self): 
            server_ids = []

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Console").text
            soup = bs(response, 'html.parser')

            select = soup.find('select', id="console_server_select")
            for option in select.find_all('option'):
                name = option.text.strip()
                id = option['value']

                server_ids.append({
                    'server': name,
                    'id': id
                })
            
            return server_ids

        def send_command(self, command: str): 
            try:
                encoded_command = quote(command)
                response = self.wrapper.session.get(
                    f"{self.wrapper.base_url}/Console/Execute?serverId={self.wrapper.server_id}&command={encoded_command}"
                )
                return response.text
            
            except Exception as e:
                print(response.status_code())
            return e, response.status_code
        
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

                    message = None
                    
                    message_span = entry.find_all('span')
                    if len(message_span) > 1:
                        message_tag = message_span[1].find('colorcode')
                        message = message_tag.get_text() if message_tag else None

                    if sender and message:
                        chat.append((sender, message))
    
            return chat
        
        def find_player(self, name: str = "", xuid: str = "", count: int = 100, 
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
            
            creators = soup.find_all('a', class_='level-color-6 no-decoration text-truncate ml-5 mr-5')
            for creator in creators:
                creator_colorcode = creator.find('colorcode')
                if creator_colorcode:
                    players.append({
                        'role': 'creator',
                        'name': creator_colorcode.text.strip(),
                        'xuid': creator.get('href').strip()[16:],
                        'url': creator.get('href').strip()
                    })

            owners = soup.find_all('a', class_='level-color-5 no-decoration text-truncate ml-5 mr-5')
            for owner in owners:
                owner_colorcode = owner.find('colorcode')
                if owner_colorcode:
                    players.append({
                        'role': 'owner',
                        'name': owner_colorcode.text.strip(),
                        'xuid': owner.get('href').strip()[16:],
                        'url': owner.get('href').strip()
                    })

            seniors = soup.find_all('a', class_='level-color-4 no-decoration text-truncate ml-5 mr-5')
            for senior in seniors:
                senior_colorcode = senior.find('colorcode')
                if senior_colorcode:
                    players.append({
                        'role': 'senior',
                        'name': senior_colorcode.text.strip(),
                        'xuid': senior.get('href').strip()[16:],
                        'url': senior.get('href').strip()
                    })

            admins = soup.find_all('a', class_='level-color-3 no-decoration text-truncate ml-5 mr-5')
            for admin in admins:
                admin_colorcode = admin.find('colorcode')
                if admin_colorcode:
                    players.append({
                        'role': 'admin',
                        'name': admin_colorcode.text.strip(),
                        'xuid': admin.get('href').strip()[16:],
                        'url': admin.get('href').strip()
                    })

            trusted = soup.find_all('a', class_='level-color-2 no-decoration text-truncate ml-5 mr-5')
            for trust in trusted:
                trusted_colorcode = trust.find('colorcode')
                if trusted_colorcode:
                    players.append({
                        'role': 'trusted',
                        'name': trusted_colorcode.text.strip(),
                        'xuid': trust.get('href').strip()[16:],
                        'url': trust.get('href').strip()
                    }) 

            users = soup.find_all('a', class_='text-light-dm text-dark-lm no-decoration text-truncate ml-5 mr-5')
            for user in users:
                colorcode = user.find('colorcode')
                if colorcode:
                    players.append({
                        'role': 'user',
                        'name': colorcode.text.strip(),
                        'xuid': user.get('href').strip()[16:],
                        'url': user.get('href').strip()
                    })
            
            flagged = soup.find_all('a', class_="level-color-1 no-decoration text-truncate ml-5 mr-5")
            for flag in flagged:
                flagged_colorcode = flag.find('colorcode')
                if flagged_colorcode:
                    players.append({
                        'role': 'flagged',
                        'name': flagged_colorcode.text.strip(),
                        'xuid': flag.get('href').strip()[16:],
                        'url': flag.get('href').strip()
                    })

            banned = soup.find_all('a', class_="level-color--1 no-decoration text-truncate ml-5 mr-5")
            for ban in banned:
                banned_colorcode = ban.find('colorcode')
                if banned_colorcode:
                    players.append({
                        'role': 'banned',
                        'name': banned_colorcode.text.strip(),
                        'xuid': ban.get('href').strip()[16:],
                        'url': ban.get('href').strip()
                    })

            return players

        def get_stock_roles(self):
            roles = []

            response = self.wrapper.session.get(f'{self.wrapper.base_url}/Action/editForm/?id=2&meta=""').text
            soup = bs(response, 'html.parser')

            select = soup.find('select', {'name': 'level'})
            if select:
                options = select.find_all('option')
                for option in options:
                    role = option.get('value')
                    if role: 
                        roles.append(role)
            
            return roles
        
        def get_roles(self):
            roles = []

            response = self.wrapper.session.get(f'{self.wrapper.base_url}/Action/editForm/?id=2&meta=""').text
            soup = bs(response, 'html.parser')

            select = soup.find('select')
            if select:
                options = select.find_all('option')
                for option in options:
                    colorcode = option.find('colorcode').text
                    roles.append(colorcode)


            return roles

        def recent_clients(self, offset: int = 0):
            recent_clients = []

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Action/RecentClientsForm?offset={offset}&count=20").text
            soup = bs(response, 'html.parser')  
            
            entries = soup.find_all('div', class_="bg-very-dark-dm bg-light-ex-lm p-15 rounded mb-10")
            for entry in entries:
                user = entry.find('div', class_="d-flex flex-row")
                if user:
                    
                    client_data = {}

                    name = user.find('a', class_="h4 mr-auto").find('colorcode').text
                    link = user.find('a')['href']
                    client_data['name'] = name
                    client_data['link'] = link

                    tooltip = user.find('div', {'data-toggle': 'tooltip'})
                    if tooltip:
                        country = tooltip.get('data-title')
                        client_data['country'] = country
          
                ip_address = entry.find('div', class_='align-self-center mr-auto').text.strip()
                last_seen = entry.find('div', class_='align-self-center text-muted font-size-12').text.strip()
                client_data['ip_address'] = ip_address
                client_data['last_seen'] = last_seen

                recent_clients.append(client_data)
            
            return recent_clients

        def get_recent_audit_log(self):
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Admin/AuditLog").text
            soup = bs(response, 'html.parser')

            tbody = soup.select_one('#audit_log_table_body')
            if not tbody:
                return 
            
            tr = tbody.select_one('tr.d-none.d-lg-table-row.bg-dark-dm.bg-light-lm')
            columns = tr.find_all('td')

            audit_log = {
                'type': columns[0].text.strip(),
                'origin': columns[1].find('a').text.strip(),
                'origin_rank': self.wrapper.Player(self.wrapper).player_rank_from_name(columns[1].find('a').text.strip()),
                'href': columns[1].find('a').get('href').strip(),
                'target': columns[2].find('a').text.strip() if columns[2].find('a') else columns[2].text.strip(),
                'data': columns[4].text.strip(),
                'time': columns[5].text.strip()
            }

            return audit_log

        def get_audit_logs(self, count: int = 15):
            audit_logs = []
        
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Admin/AuditLog").text
            soup = bs(response, 'html.parser')

            tbody = soup.select_one('#audit_log_table_body')
            if not tbody:
                return audit_logs 
            
            trs = tbody.select('tr.d-none.d-lg-table-row.bg-dark-dm.bg-light-lm')
            for tr in trs[:count]:
                columns = tr.find_all('td')

                audit_logs.append({
                    'type': columns[0].text.strip(),
                    'origin': columns[1].find('a').text.strip(),
                    'origin_rank': self.wrapper.Player(self.wrapper).player_rank_from_name(columns[1].find('a').text.strip()),
                    'href': columns[1].find('a').get('href').strip(),
                    'target': columns[2].find('a').text.strip() if columns[2].find('a') else columns[2].text.strip(),
                    'data': columns[4].text.strip(),
                    'time': columns[5].text.strip()
                })
            
            return audit_logs
        
        
        # ───────────────── # 
        #    do fix this    #
        # ───────────────── # 
        def get_client_penalties(self, penalty_type: int = 7, hide_automated_penalties: bool = False, count: int = None):
            """" Doesnt work gg """
            client_penalties = []   
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Penalty/List?showOnly={penalty_type}&hideAutomatedPenalties={hide_automated_penalties}")
            soup = bs(response.text, 'html.parser')

            entries = soup.find_all('tr', class_='d-none d-lg-table-row')
            for entry in entries:
                pass
            return client_penalties
                
        def get_admins(self, role: str = "all", count: int = None):
            admins = []

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Privileged").text
            soup = bs(response, 'html.parser')

            entries = soup.find_all('table', class_="table mb-20")
            for entry in entries[:count]:
                header = entry.find('thead').find('tr').find_all('th')
                _role = header[0].text.strip()

                if role == "all" or _role.lower() == role.lower():
                    for row in entry.find('tbody').find_all('tr'):
                        name = row.find('a', class_='text-force-break').text.strip()
                        game = row.find('div', class_='badge').text.strip() if row.find('div', class_='badge') else "N/A"
                        last_connected = row.find_all('td')[-1].text.strip()

                        admins.append({
                            'name': name,
                            'role': _role,
                            'game': game,
                            'last_connected': last_connected
                        })

                    if count is not None and len(admins) >= count:
                        break

            return admins
        
        def get_top_players(self, count: int = 30):
            top_players = {}

            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Stats/GetTopPlayersAsync?offset=0&count={count}&serverId=0").text
            soup = bs(response, 'html.parser')

            entries = soup.find_all('div', class_="card m-0 mt-15 p-20 d-flex flex-column flex-md-row justify-content-between")
            for entry in entries:

                rank_div = entry.find('div', class_="d-flex flex-column w-full w-md-quarter")
                if rank_div:
                    rank = rank_div.find('div', class_="d-flex text-muted").find('div').text
                    top_players["#"+rank] = {}

                    name_tag = rank_div.find('div', class_="d-flex flex-row")
                    if name_tag:

                        name = name_tag.find('colorcode').text
                        link = name_tag.find('a')['href']

                        top_players["#"+rank]['name'] = name
                        top_players["#"+rank]['link'] = link
                    
                    rating_tag = rank_div.find('div', class_="font-size-14").find('span').text.strip()
                    top_players["#"+rank]['rating'] = rating_tag

                    stats = {}
                    stats_tag = rank_div.find('div', class_="d-flex flex-column font-size-12 text-right text-md-left")
                    for div in stats_tag.find_all('div'):
                        primary_stat = div.find('span', class_='text-primary').text.strip()
                        secondary_stat = div.find('span', class_='text-muted').text.strip()
                        stats[secondary_stat] = primary_stat  
                    
                    top_players["#"+rank]['stats'] = stats

            return top_players
          
    class Player:
        def __init__(self, wrapper):
            self.wrapper = wrapper

        def stats(self, client_id: str):
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/api/stats/{client_id}")
            return response.text
        
        def advanced_stats(self, client_id: str):
            advanced_stats = {}
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/clientstatistics/{client_id}/advanced").text
            soup = bs(response, 'html.parser')

            top_card = soup.find('div', class_="align-self-center d-flex flex-column flex-lg-row flex-fill mb-15")
            if top_card:

                name_tag = top_card.find('a', class_="no-decoration")
                if name_tag:

                    advanced_stats['name'] = name_tag.text
                    advanced_stats['link'] = name_tag['href']

                icon = top_card.find('img', class_="img-fluid align-self-center w-75")

                advanced_stats['icon-url'] = self.wrapper.base_url + icon['src']
                advanced_stats['summary'] = top_card.find('div', id='client_stats_summary').text
            

            main_card = soup.find('div', class_="flex-fill flex-xl-grow-1")
            if main_card:
                
                advanced_stats['player_stats'] = []

                stats = main_card.find_all('div', class_='stat-card bg-very-dark-dm bg-light-ex-lm p-15 m-md-5 w-half w-md-200 rounded flex-fill')
                for stat in stats:
                    key = stat.find('div', class_='font-size-12 text-muted').text.strip()
                    value = stat.find('div', class_='m-0 font-size-16 text-primary').text.strip()
                    advanced_stats['player_stats'].append({key: value})
            
            bottom_div = soup.find('div', class_='d-flex flex-wrap flex-column-reverse flex-xl-row')
            if bottom_div:

                hit_locations = bottom_div.find_all('div', class_='mr-0 mr-xl-20 flex-fill flex-xl-grow-1')
                if hit_locations:

                    for location in hit_locations:
                        hit_title = location.find('h4', class_="content-title mb-15 mt-15").find('colorcode').text
                        hit_tbody = location.find('tbody')
                        if hit_tbody:

                            advanced_stats[hit_title] = []

                            hit_table_rows = hit_tbody.find_all('tr', class_="bg-dark-dm bg-light-lm d-none d-lg-table-row")
                            for hit_row in hit_table_rows:

                                hit_spans = hit_row.find_all('span')
                                if len(hit_spans) >= 4: 
                                    advanced_stats[hit_title].append({
                                        'location': hit_spans[0].text,
                                        'hits': hit_spans[1].text,
                                        'percentage': hit_spans[2].text,
                                        'damage': hit_spans[3].text
                                    })

                weapon_usages = bottom_div.find_all('div', class_='flex-fill flex-xl-grow-1')
                if weapon_usages:
                    for usage in weapon_usages:
                        weapon_title = usage.find('h4', class_='content-title mb-15 mt-15').find('colorcode').text
                        weapon_tbody = usage.find('tbody')
                        if weapon_tbody:
                            
                            advanced_stats[weapon_title] = []

                            weapon_table_rows = weapon_tbody.find_all('tr', 'bg-dark-dm bg-light-lm d-none d-lg-table-row')
                            for weapon_row in weapon_table_rows:
                                weapon_spans = weapon_row.find_all('span')
                                if len(weapon_spans) >= 5:
                                    advanced_stats[weapon_title].append({
                                        'weapon': weapon_spans[0].text,
                                        'favorite_attachments': weapon_spans[1].text,
                                        'kills': weapon_spans[2].text,
                                        'hits': weapon_spans[3].text,
                                        'damage': weapon_spans[4].text,
                                        'usage': weapon_spans[5].text,
                                    })

            return advanced_stats
        
        def client_info(self, client_id: str):
            return self.wrapper.session.get(f"{self.wrapper.base_url}/api/client/{client_id}").json()
        
        def player_rank_from_name(self, player_name: str):
            client_id = self.player_client_id_from_name(player_name)
            return self.client_info(client_id)['level']

        def player_xuid_from_name(self, player_name: str): 
            found_player = self.wrapper.Server(self.wrapper).find_player(name=player_name)
            player = json.loads(found_player)
            return player.get('clients')[0]['xuid']

        def player_name_from_xuid(self, xuid: str): 
            found_player = self.wrapper.Server(self.wrapper).find_player(xuid=xuid)
            player = json.loads(found_player)
            return player.get('clients')[0]['name']

        def player_name_from_client_id(self, client_id: str):
            return self.info(client_id)['name']
        
        def player_client_id_from_name(self, player_name: str):
            found_player = self.wrapper.Server(self.wrapper).find_player(name=player_name)
            player = json.loads(found_player)
            return player.get('clients')[0]['clientId']
        
        def find_player_by_partial_name(self, player_name: str):
            player_name  = player_name.lower()
            players = self.wrapper.Server(self.wrapper).get_players()

            for player in players:
                if player_name in player['name'].lower():
                    return player['name']

        def info(self, client_id: str):
            info = {}
            response = self.wrapper.session.get(f"{self.wrapper.base_url}/Client/Profile/{client_id}").text
            soup = bs(response, 'html.parser')

            info['link'] = f"{self.wrapper.base_url}/Client/Profile/{client_id}"

            name = soup.find('span', class_='font-size-20 font-weight-medium text-force-break')
            if name:
                info['name'] = name.find('colorcode').text

            xuid = soup.find('div', class_='text-muted', id='altGuidFormatsDropdown')
            if xuid:
                info['xuid'] = xuid.text

            note = soup.find('div', class_="align-self-center font-size-12 font-weight-light pl-10 pr-10")
            if note:
                note = note.text.strip()
                info['note'] = note

            ip = soup.find('div', class_='align-self-center align-self-md-start d-flex flex-row')
            if ip:
                info['ip_address'] = ip.find('span', class_="text-muted mr-5").text
                
                info['old_ips'] = []

                ips = ip.find_all('a', class_='profile-ip-lookup dropdown-item p-0 m-0')
                for tag in ips:
                    _ip = tag.get('data-ip')
                    if _ip:
                        info['old_ips'].append(_ip)

            level_div = soup.find('div', class_=lambda x: x and 'font-weight-bold' in x and 'font-size-16' in x)
            if level_div:
                level_class = " ".join(level_div.get('class', []))
        
                if 'level-color-0' in level_class:
                    info['level'] = 'User'
                elif 'level-color--1' in level_class:
                    info['level'] = 'Banned'
                elif 'level-color-1' in level_class:
                    info['level'] = 'Flagged'
                elif 'level-color-3' in level_class:
                    info['level'] = 'Administrator'
                elif 'level-color-4' in level_class:
                    info['level'] = 'SeniorAdmin'
                elif 'level-color-5' in level_class:
                    info['level'] = 'Owner'
                elif 'level-color-6' in level_class:
                    info['level'] = 'Creator'
                else:
                    info['level'] = 'User'

            vpn_whitelist = soup.find_all('div', class_="btn btn-block")
            if vpn_whitelist:
                for div in vpn_whitelist:
                    whitelisted = div.find('i', class_="oi oi-circle-x mr-5 font-size-12") #
                    if whitelisted:
                        w_span = div.find('span').text
                        if w_span:
                            info['vpn_whitelist'] = True
                    
                    not_whitelisted = div.find('i', class_="oi oi-circle-check mr-5 font-size-12")
                    if not_whitelisted:
                        n_span = div.find('span').text
                        if n_span:
                            info['vpn_whitelist'] = False                
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
            for entry in entries[:count]:
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
            for entry in entries[:count]:
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
            for entry in entries[:count]:
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
            for entry in entries[:count]:   
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
            self.game_utils = self.wrapper.Server(self.wrapper)
        
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
        
        def sayall(self, message):
            return self.game_utils.send_command(f"!sayall{message}")
        
        def say(self, message):
            return self.game_utils.send_command(f"!say {message}")

        def rules(self):
            return self.game_utils.send_command("!rules")
        
        def ping(self, player: str = None):
            if not player:
                return self.game_utils.send_command("!ping")
            else:
                return self.game_utils.send_command(f"!ping {player}")

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

class AsyncIW4MWrapper:
    def __init__(self, base_url: str, server_id: int, cookie: str):
        self.base_url = base_url
        self.server_id = server_id
        self.cookie = cookie
     
        class Utils:
            def __init__(self, wrapper):
                self.wrapper = wrapper
        
            async def does_role_exists(self, role: str):
                return role in await self.wrapper.Server(self.wrapper).get_roles()

            async def get_role_position(self, role: str):
                roles = await self.wrapper.Server(self.wrapper).get_roles()
                return roles.index(role) if role in roles else -1

            async def is_higher_role(self, role: str, role_to_check: str):
                roles = await self.wrapper.Server(self.wrapper).get_roles()
                if role not in roles or role_to_check not in roles:
                    return

                role_pos = roles.index(role)
                role_to_check_pos = roles.index(role_to_check)

                return role_pos < role_to_check_pos 

            async def is_lower_role(self, role: str, role_to_check: str):
                return not await self.is_higher_role(role, role_to_check)

            async def get_command_prefix(self):
                return await self.wrapper.Server(self.wrapper).get_audit_logs()[0]['data'][0]

            async def is_player_online(self, player_name: str):
                players = await self.wrapper.Server(self.wrapper).get_players()
                return any(player['name'] == player_name for player in players)
            
            async def get_player_count(self):
                return len(await self.wrapper.Server(self.wrapper).get_players())

            async def is_server_full(self):
                server_info = await self.wrapper.Server(self.wrapper).info()
                return server_info['totalConnectedClients'] >= server_info['totalClientSlots']

            async def get_online_players_by_role(self, role: str):
                players = []

                _players = self.wrapper.Server(self.wrapper).get_players()
                for player in _players:
                    if player['role'].lower() == role.lower():
                        players.append(player)

                return players

            async def find_admin(self, admin_name: str):
                admins = self.wrapper.Server(self.wrapper).get_admins()
                for admin in admins:
                    if admin['name'].lower() == admin_name.lower():
                        return admin

    class Server:
        def __init__(self, wrapper):
            self.wrapper = wrapper
        
        async def status(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/api/status",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response: 
                    return await response.json()
            
        async def info(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/api/info",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    return await response.json()
                
        async def help(self):
            _help = {}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Home/Help",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    text = await response.text()
                    soup = bs(text, 'html.parser')
                    
                    command_list = soup.find('div', class_="command-assembly-container")
                    if command_list:
                        command_title = command_list.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                        if command_title not in _help:
                            _help[command_title] = {}

                        commands = command_list.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                        for command in commands:
                            name = command.find('td', class_="font-weight-bold").text.strip()
                            alias = command.find_all('td')[1].text.strip()
                            description = command.find_all('td')[2].text.strip()
                            requires_target = command.find_all('td')[3].text.strip()
                            syntax = command.find_all('td')[4].text.strip()
                            min_level = command.find('td', class_="text-right").text.strip()

                            _help[command_title][name] = {
                                "alias": alias,
                                "description": description,
                                "requires_target": requires_target,
                                "syntax": syntax,
                                "min_level": min_level
                                }
            
                    script_plugin = soup.find_all('div', class_="command-assembly-container")[1]
                    if script_plugin:
                        script_title = script_plugin.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                        if script_title not in _help:
                            _help[script_title] = {}

                        scripts = script_plugin.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                        for script in scripts:
                            name = script.find('td', class_="font-weight-bold").text.strip()
                            alias = script.find_all('td')[1].text.strip()
                            description = script.find_all('td')[2].text.strip()
                            requires_target = script.find_all('td')[3].text.strip()
                            syntax = script.find_all('td')[4].text.strip()
                            min_level = script.find('td', class_="text-right").text.strip()

                            _help[script_title][name] = {
                                "alias": alias,
                                "description": description,
                                "requires_target": requires_target,
                                "syntax": syntax,
                                "min_level": min_level
                                }
            
                    login = soup.find_all('div', class_="command-assembly-container")[2]
                    if login:
                        login_title = login.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                        if login_title not in _help:
                            _help[login_title] = {}

                        login_entries = login.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                        for login_entry in login_entries:
                            name = login_entry.find('td', class_="font-weight-bold").text.strip()
                            alias = login_entry.find_all('td')[1].text.strip()
                            description = login_entry.find_all('td')[2].text.strip()
                            requires_target = login_entry.find_all('td')[3].text.strip()
                            syntax = login_entry.find_all('td')[4].text.strip()
                            min_level = login_entry.find('td', class_="text-right").text.strip()

                            _help[login_title][name] = {
                                "alias": alias,
                                "description": description,
                                "requires_target": requires_target,
                                "syntax": syntax,
                                "min_level": min_level
                                }

                    mute = soup.find_all('div', class_="command-assembly-container")[3]
                    if mute:
                        mute_title = mute.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                        if mute_title not in _help:
                            _help[mute_title] = {}

                        mute_entries = mute.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                        for mute_entry in mute_entries:
                            name = mute_entry.find('td', class_="font-weight-bold").text.strip()
                            alias = mute_entry.find_all('td')[1].text.strip()
                            description = mute_entry.find_all('td')[2].text.strip()
                            requires_target = mute_entry.find_all('td')[3].text.strip()
                            syntax = mute_entry.find_all('td')[4].text.strip()
                            min_level = mute_entry.find('td', class_="text-right").text.strip()

                            _help[mute_title][name] = {
                                "alias": alias,
                                "description": description,
                                "requires_target": requires_target,
                                "syntax": syntax,
                                "min_level": min_level
                                }

                    simple_stats = soup.find_all('div', class_="command-assembly-container")[4]
                    if simple_stats:
                        simple_stats_title = simple_stats.find('h2', class_="content-title mb-lg-20 mt-20").text.strip()
                        if simple_stats_title not in _help:
                            _help[simple_stats_title] = {}

                        simple_stats_entries = simple_stats.find_all('tr', class_="d-none d-lg-table-row bg-dark-dm bg-light-lm")
                        for simple_stats_entry in simple_stats_entries:
                            name = simple_stats_entry.find('td', class_="font-weight-bold").text.strip()
                            alias = simple_stats_entry.find_all('td')[1].text.strip()
                            description = simple_stats_entry.find_all('td')[2].text.strip()
                            requires_target = simple_stats_entry.find_all('td')[3].text.strip()
                            syntax = simple_stats_entry.find_all('td')[4].text.strip()
                            min_level = simple_stats_entry.find('td', class_="text-right").text.strip()

                            _help[simple_stats_title][name] = {
                                "alias": alias,
                                "description": description,
                                "requires_target": requires_target,
                                "syntax": syntax,
                                "min_level": min_level
                                }

            return _help

        async def get_map_name(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:

                    text = await response.text()
                    soup = bs(text, 'html.parser')

                    map_div = soup.find('div', class_='col-12 align-self-center text-center text-lg-left col-lg-4')
                    if map_div:
                        map_name = map_div.find('span')
                        if map_name:
                            return map_name.text.strip() 
        
        async def get_gamemode(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}",
                    headers={'Cookie': self.wrapper.cookie}
                ) as response:

                    text = await response.text()
                    soup = bs(text, 'html.parser')

                    map_div = soup.find('div', class_='col-12 align-self-center text-center text-lg-left col-lg-4')
                    if map_div:
                        spans = map_div.find_all('span')
                        if len(spans) > 2:
                            return spans[2].text.strip() 

        async def get_iw4m_version(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:

                    text = await response.text()
                    soup = bs(text, 'html.parser')

                    entries = soup.find_all('a', class_="sidebar-link")
                    for entry in entries:
                        span = entry.find('span', class_="text-primary")
                        if span:
                            return span.text.strip()
            
        async def logged_in_as(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:

                    text = await response.text()
                    soup = bs(text, 'html.parser')

                    div = soup.find('div', class_="sidebar-link font-size-12 font-weight-light")
                    if div:
                        colorcode = div.find('colorcode')
                        return colorcode.text.strip()

        async def get_rules(self):
            rules = []

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/About",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:

                    text = await response.text()
                    soup = bs(text, 'html.parser')

                    card_divs = soup.find_all('div', class_="card m-0 rounded")
                    for card_div in card_divs:
                        h5 = card_div.find('h5', class_="text-primary mt-0 mb-0")
                        if h5:
                            divs = card_div.find_all('div', class_="rule")
                            for div in divs:
                                rules.append(div.text.strip())

            return rules

        async def get_reports(self):
            reports = []

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/Action/RecentReportsForm/",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:

                    text = await response.text()
                    soup = bs(text, 'html.parser')

                    report_blocks = soup.find_all('div', class_='rounded bg-very-dark-dm bg-light-ex-lm mt-10 mb-10 p-10')
                    for block in report_blocks:
                        timestamp_tag = block.find('div', class_='font-weight-bold')
                        timestamp = timestamp_tag.text.strip()


                    entries = soup.find_all('div', class_="font-size-12")
                    for entry in entries:
                        origin_tag = entry.find('a')
                        origin = origin_tag.text.strip()

                        reason_tag = entry.find('span', class_='text-white-dm text-black-lm').find('colorcode')
                        reason = reason_tag.text.strip()

                        target_tag = entry.find('span', class_='text-highlight').find('a')
                        target = target_tag.text.strip()

                        reports.append({
                            'origin': origin,
                            'reason': reason,
                            'target': target,
                            'timestamp': timestamp
                        })

            return reports
                    
        async def get_server_ids(self): 
            server_ids = []

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Console",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    text = await response.text()
                    soup = bs(text, 'html.parser')

                    select = soup.find('select', id="console_server_select")
                    for option in select.find_all('option'):
                        name = option.text.strip()
                        id = option['value']
                        server_ids.append({
                            'server': name,
                            'id': id
                        })
            
                    return server_ids

        async def send_command(self, command: str):
            encoded_command = quote(command)
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(
                        f"{self.wrapper.base_url}/Console/Execute?serverId={self.wrapper.server_id}&command={encoded_command}",
                        headers={"Cookie": self.wrapper.cookie}
                    ) as response:
                        return await response.text()
        
                except aiohttp.ClientError as e:
                    raise
        
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
                            

        async def find_player(self, name: str = "", xuid: str = "", count: int = 100, 
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
                    
                    creators = soup.find_all('a', class_='level-color-6 no-decoration text-truncate ml-5 mr-5')
                    for creator in creators:
                        creator_colorcode = creator.find('colorcode')
                        if creator_colorcode:
                            players.append({
                                'role': 'creator',
                                'name': creator_colorcode.text.strip(),
                                'xuid': creator.get('href').strip()[16:],
                                'url': creator.get('href').strip()
                            })

                    owners = soup.find_all('a', class_='level-color-5 no-decoration text-truncate ml-5 mr-5')
                    for owner in owners:
                        owner_colorcode = owner.find('colorcode')
                        if owner_colorcode:
                            players.append({
                                'role': 'owner',
                                'name': owner_colorcode.text.strip(),
                                'xuid': owner.get('href').strip()[16:],
                                'url': owner.get('href').strip()
                            })

                    seniors = soup.find_all('a', class_='level-color-4 no-decoration text-truncate ml-5 mr-5')
                    for senior in seniors:
                        senior_colorcode = senior.find('colorcode')
                        if senior_colorcode:
                            players.append({
                                'role': 'senior',
                                'name': senior_colorcode.text.strip(),
                                'xuid': senior.get('href').strip()[16:],
                                'url': senior.get('href').strip()
                            })

                    admins = soup.find_all('a', class_='level-color-3 no-decoration text-truncate ml-5 mr-5')
                    for admin in admins:
                        admin_colorcode = admin.find('colorcode')
                        if admin_colorcode:
                            players.append({
                                'role': 'admin',
                                'name': admin_colorcode.text.strip(),
                                'xuid': admin.get('href').strip()[16:],
                                'url': admin.get('href').strip()
                            })

                    trusted = soup.find_all('a', class_='level-color-2 no-decoration text-truncate ml-5 mr-5')
                    for trust in trusted:
                        trusted_colorcode = trust.find('colorcode')
                        if trusted_colorcode:
                            players.append({
                                'role': 'trusted',
                                'name': trusted_colorcode.text.strip(),
                                'xuid': trust.get('href').strip()[16:],
                                'url': trust.get('href').strip()
                            }) 

                    users = soup.find_all('a', class_='text-light-dm text-dark-lm no-decoration text-truncate ml-5 mr-5')
                    for user in users:
                        colorcode = user.find('colorcode')
                        if colorcode:
                            players.append({
                                'role': 'user',
                                'name': colorcode.text.strip(),
                                'xuid': user.get('href').strip()[16:],
                                'url': user.get('href').strip()
                            })
            
                    flagged = soup.find_all('a', class_="level-color-1 no-decoration text-truncate ml-5 mr-5")
                    for flag in flagged:
                        flagged_colorcode = flag.find('colorcode')
                        if flagged_colorcode:
                            players.append({
                                'role': 'flagged',
                                'name': flagged_colorcode.text.strip(),
                                'xuid': flag.get('href').strip()[16:],
                                'url': flag.get('href').strip()
                            })

                    banned = soup.find_all('a', class_="level-color--1 no-decoration text-truncate ml-5 mr-5")
                    for ban in banned:
                        banned_colorcode = ban.find('colorcode')
                        if banned_colorcode:
                            players.append({
                                'role': 'banned',
                                'name': banned_colorcode.text.strip(),
                                'xuid': ban.get('href').strip()[16:],
                                'url': ban.get('href').strip()
                            })

                    return players


        async def get_stock_roles(self):
            roles = []

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.wrapper.base_url}/Action/editForm/?id=982&meta=""',
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    select = soup.find('select', {'name': 'level'})
                    if select:
                        options = select.find_all('option')
                        for option in options:
                            role = option.get('value')
                            if role: 
                                roles.append(role)
            return roles
        
        async def get_roles(self):
            roles = []

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.wrapper.base_url}/Action/editForm/?id=2&meta=""',
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:

                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    select = soup.find('select')
                    if select:
                        options = select.find_all('option')
                        for option in options:
                            colorcode = option.find('colorcode').text
                            roles.append(colorcode)

            return roles 

        async def recent_clients(self, offset: int = 0):
            recent_clients = []

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.wrapper.base_url}/Action/RecentClientsForm?offset={offset}&count=20",
                                       headers={"Cookie": self.wrapper.cookie}) as response:
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')
            
                    entries = soup.find_all('div', class_="bg-very-dark-dm bg-light-ex-lm p-15 rounded mb-10")
                    for entry in entries:
                        user = entry.find('div', class_="d-flex flex-row")
                        if user:
                            client_data = {}

                            name = user.find('a', class_="h4 mr-auto").find('colorcode').text
                            link = user.find('a')['href']
                            client_data['name'] = name
                            client_data['link'] = link

                            tooltip = user.find('div', {'data-toggle': 'tooltip'})
                            client_data['country'] = tooltip.get('data-title') if tooltip else None

                            ip_address = entry.find('div', class_='align-self-center mr-auto').text.strip()
                            last_seen = entry.find('div', class_='align-self-center text-muted font-size-12').text.strip()
                            client_data['ip_address'] = ip_address
                            client_data['last_seen'] = last_seen

                            recent_clients.append(client_data)
                    
            return recent_clients
        
        async def get_audit_logs(self):
            audit_logs = []

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Admin/AuditLog",
                    headers={"Cookie": self.wrapper.cookie}
                    ) as response:

                        response_text = await response.text()
                        soup = bs(response_text, 'html.parser')

                        tbody = soup.find('tbody', id='audit_log_table_body')
                        if not tbody:
                            return audit_logs

                        trs = tbody.find_all('tr', class_='d-none d-lg-table-row bg-dark-dm bg-light-lm')
                        for tr in trs:
                            columns = tr.find_all('td')

                            audit_log = {
                                'type': columns[0].text.strip(),
                                'origin': columns[1].find('a').text.strip(),
                                'origin_rank': self.wrapper.Player(self.wrapper).player_rank_from_name(columns[1].find('a').text.strip()),
                                'href': columns[1].find('a').get('href').strip(),
                                'target': columns[2].find('a').text.strip() if columns[2].find('a') else columns[2].text.strip(),
                                'data': columns[4].text.strip(),
                                'time': columns[5].text.strip()
                            }

                            audit_logs.append(audit_log)
            
            return audit_logs
        
        async def get_client_penalties(self, penalty_type: int = 7, hide_automated_penalties: bool = False, count: int = None):
            client_penalties = [] 

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Penalty/List?showOnly={penalty_type}&hideAutomatedPenalties={hide_automated_penalties}",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:

                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('tr', class_='d-none d-lg-table-row')
                    for entry in entries[:count]:
                        player_name_tag = entry.find('a', class_='level-color-flagged')
                        admin_name_tag = entry.find('a', class_='level-color-administrator')
                        penalty = entry.find('td', class_='penalties-color-kick')
                        reason = entry.find_all('colorcode')[0].text if entry.find_all('colorcode') else None
                        admin = admin_name_tag.find('colorcode').text if admin_name_tag else None
                        penalty_time = entry.find('span').text if entry.find('span') else None

                        roles = {
                            "owner": entry.find('a', class_="level-color-owner"),
                            "senioradmin": entry.find('a', class_="level-color-senioradmin"),
                            "admin": entry.find('a', class_="level-color-administrator"),
                            "trusted": entry.find('a', class_="level-color-trusted"),
                            "user": entry.find('a', class_="level-color-user"),
                            "flagged": entry.find('a', class_="level-color-flagged"),
                            "banned": entry.find('a', class_="level-color-banned")
                        }

                        present_roles = [role for role, tag in roles.items() if tag]

                        player_name = player_name_tag.get_text(strip=True) if player_name_tag else 'Unknown Player'

                        client_penalties.append({
                            'player_name': player_name,
                            'penalty': penalty.get_text(strip=True) if penalty else 'None',
                            'reason': reason,
                            'admin': admin,
                            'penalty_time': penalty_time,
                            'roles': present_roles 
                        })

                    return client_penalties

        async def get_admins(self, role: str = "all", count: int = None):
            admins = []

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Client/Privileged",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('table', class_="table mb-20")
                    for entry in entries:
                        if count is not None and len(admins) >= count:
                            break
                        
                        header = entry.find('thead').find('tr').find_all('th')
                        _role = header[0].text.strip()     

                        if role == "all" or _role.lower() == role.lower():
                            for row in entry.find('tbody').find_all('tr'):
                                name = row.find('a', class_='text-force-break').text.strip()
                                game = row.find('div', class_='badge').text.strip() if row.find('div', class_='badge') else "N/A"
                                last_connected = row.find_all('td')[-1].text.strip()

                                admins.append({
                                    'name': name,
                                    'role': _role,
                                    'game': game,
                                    'last_connected': last_connected
                                })

                                if count is not None and len(admins) >= count:
                                    break

                    return admins
                
        async def get_top_players(self, count: int = 20):
            top_players = {}

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wrapper.base_url}/Stats/GetTopPlayersAsync?offset=0&count={count}&serverId=0",
                    headers={"Cookie": self.wrapper.cookie}
                ) as response:
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    entries = soup.find_all('div', class_="card m-0 mt-15 p-20 d-flex flex-column flex-md-row justify-content-between")
                    for entry in entries:
                        rank_div = entry.find('div', class_="d-flex flex-column w-full w-md-quarter")
                        if rank_div:
                            rank = rank_div.find('div', class_="d-flex text-muted").find('div').text
                            top_players["#" + rank] = {}

                            name_tag = rank_div.find('div', class_="d-flex flex-row")
                            if name_tag:
                                name = name_tag.find('colorcode').text
                                link = name_tag.find('a')['href']

                                top_players["#" + rank]['name'] = name
                                top_players["#" + rank]['link'] = link

                            rating_tag = rank_div.find('div', class_="font-size-14").find('span').text.strip()
                            top_players["#" + rank]['rating'] = rating_tag

                            stats = {}
                            stats_tag = rank_div.find('div', class_="d-flex flex-column font-size-12 text-right text-md-left")
                            for div in stats_tag.find_all('div'):
                                primary_stat = div.find('span', class_='text-primary').text.strip()
                                secondary_stat = div.find('span', class_='text-muted').text.strip()
                                stats[secondary_stat] = primary_stat

                            top_players["#" + rank]['stats'] = stats

            return top_players
    
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
        
        async def advanced_stats(self, client_id: str):
            advanced_stats = {}
    
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.wrapper.base_url}/clientstatistics/{client_id}/advanced",
                                       headers={"Cookie": self.wrapper.cookie}) as response:
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    top_card = soup.find('div', class_="align-self-center d-flex flex-column flex-lg-row flex-fill mb-15")
                    if top_card:
                        name_tag = top_card.find('a', class_="no-decoration")
                        if name_tag:
                            advanced_stats['name'] = name_tag.text
                            advanced_stats['link'] = name_tag['href']

                        icon = top_card.find('img', class_="img-fluid align-self-center w-75")
                        if icon:
                            advanced_stats['icon-url'] = self.wrapper.base_url + icon['src']
                
                        summary = top_card.find('div', id='client_stats_summary')
                        advanced_stats['summary'] = summary.text if summary else None

                    main_card = soup.find('div', class_="flex-fill flex-xl-grow-1")
                    if main_card:
                        advanced_stats['player_stats'] = []
                        stats = main_card.find_all('div', class_='stat-card bg-very-dark-dm bg-light-ex-lm p-15 m-md-5 w-half w-md-200 rounded flex-fill')

                        for stat in stats:
                            key = stat.find('div', class_='font-size-12 text-muted').text.strip()
                            value = stat.find('div', class_='m-0 font-size-16 text-primary').text.strip()
                            advanced_stats['player_stats'].append({key: value})

                    bottom_div = soup.find('div', class_='d-flex flex-wrap flex-column-reverse flex-xl-row')
                    if bottom_div:
                        hit_locations = bottom_div.find_all('div', class_='mr-0 mr-xl-20 flex-fill flex-xl-grow-1')
                        for location in hit_locations:
                            hit_title = location.find('h4', class_="content-title mb-15 mt-15").find('colorcode').text
                            hit_tbody = location.find('tbody')
                            if hit_tbody:
                                advanced_stats[hit_title] = []
                                hit_table_rows = hit_tbody.find_all('tr', class_="bg-dark-dm bg-light-lm d-none d-lg-table-row")
                                for hit_row in hit_table_rows:
                                    hit_spans = hit_row.find_all('span')
                                    if len(hit_spans) >= 4:
                                        advanced_stats[hit_title].append({
                                            'location': hit_spans[0].text,
                                            'hits': hit_spans[1].text,
                                            'percentage': hit_spans[2].text,
                                            'damage': hit_spans[3].text
                                        })

                        weapon_usages = bottom_div.find_all('div', class_='flex-fill flex-xl-grow-1')
                        for usage in weapon_usages:
                            weapon_title = usage.find('h4', class_='content-title mb-15 mt-15').find('colorcode').text
                            weapon_tbody = usage.find('tbody')
                            if weapon_tbody:
                                advanced_stats[weapon_title] = []
                                weapon_table_rows = weapon_tbody.find_all('tr', 'bg-dark-dm bg-light-lm d-none d-lg-table-row')
                                for weapon_row in weapon_table_rows:
                                    weapon_spans = weapon_row.find_all('span')
                                    if len(weapon_spans) >= 5:
                                        advanced_stats[weapon_title].append({
                                            'weapon': weapon_spans[0].text,
                                            'favorite_attachments': weapon_spans[1].text,
                                            'kills': weapon_spans[2].text,
                                            'hits': weapon_spans[3].text,
                                            'damage': weapon_spans[4].text,
                                            'usage': weapon_spans[5].text,
                                        })

            return advanced_stats
        
        async def client_info(self, client_id: str):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.wrapper.base_url}/api/client/{client_id}", headers={"Cookie": self.wrapper.cookie}) as response:
                    return await response.json()


        async def info(self, client_id: str):
            info = {}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.wrapper.base_url}/Client/Profile/{client_id}", headers={"Cookie": self.wrapper.cookie}) as response:
                    response_text = await response.text()
                    soup = bs(response_text, 'html.parser')

                    info['link'] = f"{self.wrapper.base_url}/Client/Profile/{client_id}"

                    name = soup.find('span', class_='font-size-20 font-weight-medium text-force-break')
                    if name:
                        info['name'] = name.find('colorcode').text

                    guid = soup.find('div', class_='text-muted', id='altGuidFormatsDropdown')
                    if guid:
                        info['guid'] = guid.text

                    note = soup.find('div', class_="align-self-center font-size-12 font-weight-light pl-10 pr-10")
                    if note:
                        info['note'] = note.text.strip()

                    ip = soup.find('div', class_='align-self-center align-self-md-start d-flex flex-row')
                    if ip:
                        info['ip_address'] = ip.find('span', class_="text-muted mr-5").text
                        info['old_ips'] = []

                        ips = ip.find_all('a', class_='profile-ip-lookup dropdown-item p-0 m-0')
                        for tag in ips:
                            _ip = tag.get('data-ip')
                            if _ip:
                                info['old_ips'].append(_ip)

                    level_div = soup.find('div', class_=lambda x: x and 'font-weight-bold' in x and 'font-size-16' in x)
                    if level_div:
                        level_class = " ".join(level_div.get('class', []))
                        if 'level-color-0' in level_class:
                            info['level'] = 'User'
                        elif 'level-color--1' in level_class:
                            info['level'] = 'Banned'
                        elif 'level-color-1' in level_class:
                            info['level'] = 'Flagged'
                        elif 'level-color-3' in level_class:
                            info['level'] = 'Administrator'
                        elif 'level-color-4' in level_class:
                            info['level'] = 'SeniorAdmin'
                        elif 'level-color-5' in level_class:
                            info['level'] = 'Owner'
                        elif 'level-color-6' in level_class:
                            info['level'] = 'Creator'
                        else:
                            info['level'] = 'User'
                    
                    vpn_whitelist = soup.find_all('div', class_="btn btn-block")
                    if vpn_whitelist:
                        for div in vpn_whitelist:
                            whitelisted = div.find('i', class_="oi oi-circle-x mr-5 font-size-12") #
                            if whitelisted:
                                w_span = div.find('span').text
                                if w_span:
                                    info['vpn_whitelist'] = True
                    
                            not_whitelisted = div.find('i', class_="oi oi-circle-check mr-5 font-size-12")
                            if not_whitelisted:
                                n_span = div.find('span').text
                                if n_span:
                                    info['vpn_whitelist'] = False

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

        async def player_rank_from_name(self, player_name: str):
            client_id = await self.player_client_id_from_name(player_name)
            return self.client_info(client_id)['level']

        async def player_xuid_from_name(self, player_name: str):
            found_player = await self.wrapper.Server(self.wrapper).find_player(name=player_name)
            player = json.loads(found_player)
            return player.get('clients')[0]['xuid']

        async def player_name_from_xuid(self, xuid: str):
            found_player = self.wrapper.Server(self.wrapper).find_player(xuid=xuid)
            player = json.loads(found_player)
            return player.get('clients')[0]['name']

        async def player_name_from_client_id(self, client_id: str):
            return await self.info(client_id)['name']

        async def player_client_id_from_name(self, player_name: str):
            found_player = await self.wrapper.Server(self.wrapper).find_player(name=player_name)
            player = json.loads(found_player)
            return player.get('clients')[0]['clientId']

        async def find_player_by_partial_name(self, player_name: str):
            player_name  = player_name.lower()
            players = await self.wrapper.Server(self.wrapper).get_players()

            for player in players:
                if player_name in player['name'].lower():
                    return player['name']

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
                    for entry in entries[:count]:
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
                    for entry in entries[:count]:
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
                    for entry in entries[:count]:
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
                    for entry in entries[:count]:
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
            self.game_utils = self.wrapper.Server(self.wrapper)
    
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
        
        async def sayall(self, message):
            return await self.game_utils.send_command(f"!sayall {message}")
        
        async def say(self, message):
            return await self.game_utils.send_command(f"!say {message}")

        async def rules(self):
            return await self.game_utils.send_command("!rules")
        
        async def ping(self, player):
            return await self.game_utils.send_command(f"!ping {player}")
        
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
