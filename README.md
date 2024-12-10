![http://152.53.132.41:1624](https://files.oaiusercontent.com/file-H9NcrwXUEUXJB4GMeaBseM?se=2024-12-10T08%3A25%3A59Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D1c0b305a-43d6-4160-bf38-56c221bc2c7e.webp&sig=5S4iSXttKAyvEKs1LrmmKg7emkjiK39xjZ0LashQA6k%3D)
hop on brownies :)

<div style="padding-bottom: 1.5rem;"></div>

<div align="center">
    <h1 style="font-size: 2.7rem; font-weight: 800;">
        <span style="color: #82C8F5;">
            IW4M
        </span>
        -
        <span style="color: #82C8F5;">
            Admin
        </span> 
        <span style="color: #82C8F5;">
            Wrapper
        </span> 
        🎮
    </h1>
    <p style="font-size: 1.25rem; font-weight: 500; margin-bottom: -0.7rem">An <span style="color: #82C8F5;">easy</span>-to-<span style="color: #82C8F5;">use</span> Python wrapper for interacting with the IW4M-Admin</p>
</div>


## <h1 style="font-weight: 800; font-size:2.5rem; border: solid transparent; margin-bottom: 1rem;">Intro<span style="color: #82C8F5;">duction</span></h1>

<p style="font-size: 1.1rem;">Welcome to <strong>the official wiki</strong> for the <em>IW4M-Admin Wrapper</em>! This wrapper allows you to <strong>easily interact with the IW4M-Admin server</strong> through a simple Python interface. Whether you're  server staff or a developer, this wrapper will simplify your interactions with IW4M-Admin, enabling you to manage players, retrieve statistics, and much more 📊</p>

---

<div align="center">
    <h1 style="margin-bottom: -1.5rem; border: solid transparent; font-weight: 800; font-size: 3rem;">Table of Contents</h1>
</div>

<div style="display: flex; gap: 1rem; padding: 20px; border: solid transparent; flex-wrap: wrap;">
    <!-- Server Class Section -->
    <div style="flex: 1; border: 0.15rem solid #82C8F5; border-radius: 10px; padding: 15px;">
        <h2 style="font-size: 2.5rem; font-weight: 700;">
            <a href="#server-class" style="text-decoration: none; color: white;">
                Server <span style="color: #82C8F5;">Class</span> 🎮
            </a>
        </h2>
        <ul style="list-style: none; padding: 0; line-height: 1.8;">
            <li><a href="#status" style="color: #91C1E6; font-size: 1.1rem;">status()</a></li>
            <li><a href="#info" style="color: #91C1E6;">info()</a></li>
            <li><a href="#get_server_ids" style="color: #91C1E6;">get_server_ids()</a></li>
            <li><a href="#send_command" style="color: #91C1E6;">send_command()</a></li>
            <li><a href="#read_chat" style="color: #91C1E6;">read_chat()</a></li>
            <li><a href="#recent_clients" style="color: #91C1E6;">recent_clients()</a></li>
            <li><a href="#find_player" style="color: #91C1E6;">find_player()</a></li>
            <li><a href="#get_users" style="color: #91C1E6;">get_users()</a></li>
            <li><a href="#get_players" style="color: #91C1E6;">get_players()</a></li>
            <li><a href="#get_roles" style="color: #91C1E6;">get_roles()</a></li>
            <li><a href="#get_admins" style="color: #91C1E6;">get_admins()</a></li>
            <li><a href="#get_audit_logs" style="color: #91C1E6;">get_audit_logs()</a></li>
            <li><a href="#get_client_penalties" style="color: #91C1E6;">get_client_penalties()</a></li>
            <li><a href="#get_top_players" style="color: #91C1E6;">get_top_players()</a></li>
        </ul>
    </div>
    <!-- Player Class Section -->
    <div style="flex: 1; border: 0.15rem solid #82C8F5; border-radius: 10px; padding: 15px; background-color: transparent;">
        <h2 style="font-size: 2.5rem; font-weight: 700;">
            <a href="#server-class" style="text-decoration: none; color: white;">
                Player <span style="color: #82C8F5;">Class</span>👾
            </a>
        </h2>
        <ul style="list-style: none; padding: 0; line-height: 1.8;">
            <li><a href="#stats" style="color: #91C1E6; font-size: 1.1rem;">stats()</a></li>
            <li><a href="#advanced_stats" style="color: #91C1E6; font-size: 1.1rem;">advanced_stats()</a></li>
            <li><a href="#client_info" style="color: #91C1E6; font-size: 1.1rem;">client_info()</a></li>
            <li><a href="#info" style="color: #91C1E6; font-size: 1.1rem;">info()</a></li>
            <li><a href="#chat_history" style="color: #91C1E6; font-size: 1.1rem;">chat_history()</a></li>
            <li><a href="#name_changes" style="color: #91C1E6; font-size: 1.1rem;">name_changes()</a></li>
            <li><a href="#administered_penalties" style="color: #91C1E6; font-size: 1.1rem;">administered_penalties()</a></li>
            <li><a href="#received_penalties" style="color: #91C1E6; font-size: 1.1rem;">received_penalties()</a></li>
            <li><a href="#connection_history" style="color: #91C1E6; font-size: 1.1rem;">connection_history()</a></li>
            <li><a href="#permissions" style="color: #91C1E6; font-size: 1.1rem;">permissions()</a></li>
        </ul>
    </div>
</div>

<div align="center" id="server-class">
    <h1 style="padding-top: 5rem; padding-bottom: 0.2rem; font-weight: 800; font-size: 3rem;">Server Class 💻</h1>
    <p style="font-size: 1.2rem; color: #white;">The Server class provides utility functions for interacting with the IW4M-Admin servers</p>
</div>

![http://152.53.132.41:1624](https://files.oaiusercontent.com/file-H9NcrwXUEUXJB4GMeaBseM?se=2024-12-10T08%3A25%3A59Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D1c0b305a-43d6-4160-bf38-56c221bc2c7e.webp&sig=5S4iSXttKAyvEKs1LrmmKg7emkjiK39xjZ0LashQA6k%3D)
hop on brownies :)

<div style="padding-bottom: 1.5rem;"></div>

<div align="center">
    <h1 style="font-size: 2.7rem; font-weight: 800;">
        <span style="color: #82C8F5;">
            IW4M
        </span>
        -
        <span style="color: #82C8F5;">
            Admin
        </span> 
        <span style="color: #82C8F5;">
            Wrapper
        </span> 
        🎮
    </h1>
    <p style="font-size: 1.25rem; font-weight: 500; margin-bottom: -0.7rem">An <span style="color: #82C8F5;">easy</span>-to-<span style="color: #82C8F5;">use</span> Python wrapper for interacting with the IW4M-Admin</p>
</div>


## <h1 style="font-weight: 800; font-size:2.5rem; border: solid transparent; margin-bottom: 1rem;">Intro<span style="color: #82C8F5;">duction</span></h1>

<p style="font-size: 1.1rem;">Welcome to <strong>the official wiki</strong> for the <em>IW4M-Admin Wrapper</em>! This wrapper allows you to <strong>easily interact with the IW4M-Admin server</strong> through a simple Python interface. Whether you're  server staff or a developer, this wrapper will simplify your interactions with IW4M-Admin, enabling you to manage players, retrieve statistics, and much more 📊</p>

---

<div align="center">
    <h1 style="margin-bottom: -1.5rem; border: solid transparent; font-weight: 800; font-size: 3rem;">Table of Contents</h1>
</div>

<div style="display: flex; gap: 1rem; padding: 20px; border: solid transparent; flex-wrap: wrap;">
    <!-- Server Class Section -->
    <div style="flex: 1; border: 0.15rem solid #82C8F5; border-radius: 10px; padding: 15px;">
        <h2 style="font-size: 2.5rem; font-weight: 700;">
            <a href="#server-class" style="text-decoration: none; color: white;">
                Server <span style="color: #82C8F5;">Class</span> 🎮
            </a>
        </h2>
        <ul style="list-style: none; padding: 0; line-height: 1.8;">
            <li><a href="#status" style="color: #91C1E6; font-size: 1.1rem;">status()</a></li>
            <li><a href="#info" style="color: #91C1E6;">info()</a></li>
            <li><a href="#get_server_ids" style="color: #91C1E6;">get_server_ids()</a></li>
            <li><a href="#send_command" style="color: #91C1E6;">send_command()</a></li>
            <li><a href="#read_chat" style="color: #91C1E6;">read_chat()</a></li>
            <li><a href="#recent_clients" style="color: #91C1E6;">recent_clients()</a></li>
            <li><a href="#find_player" style="color: #91C1E6;">find_player()</a></li>
            <li><a href="#get_users" style="color: #91C1E6;">get_users()</a></li>
            <li><a href="#get_players" style="color: #91C1E6;">get_players()</a></li>
            <li><a href="#get_roles" style="color: #91C1E6;">get_roles()</a></li>
            <li><a href="#get_admins" style="color: #91C1E6;">get_admins()</a></li>
            <li><a href="#get_audit_logs" style="color: #91C1E6;">get_audit_logs()</a></li>
            <li><a href="#get_client_penalties" style="color: #91C1E6;">get_client_penalties()</a></li>
            <li><a href="#get_top_players" style="color: #91C1E6;">get_top_players()</a></li>
        </ul>
    </div>
    <!-- Player Class Section -->
    <div style="flex: 1; border: 0.15rem solid #82C8F5; border-radius: 10px; padding: 15px; background-color: transparent;">
        <h2 style="font-size: 2.5rem; font-weight: 700;">
            <a href="#player-class" style="text-decoration: none; color: white;">
                Player <span style="color: #82C8F5;">Class</span>👾
            </a>
        </h2>
        <ul style="list-style: none; padding: 0; line-height: 1.8;">
            <li><a href="#stats" style="color: #91C1E6; font-size: 1.1rem;">stats()</a></li>
            <li><a href="#advanced_stats" style="color: #91C1E6; font-size: 1.1rem;">advanced_stats()</a></li>
            <li><a href="#client_info" style="color: #91C1E6; font-size: 1.1rem;">client_info()</a></li>
            <li><a href="#info" style="color: #91C1E6; font-size: 1.1rem;">info()</a></li>
            <li><a href="#chat_history" style="color: #91C1E6; font-size: 1.1rem;">chat_history()</a></li>
            <li><a href="#name_changes" style="color: #91C1E6; font-size: 1.1rem;">name_changes()</a></li>
            <li><a href="#administered_penalties" style="color: #91C1E6; font-size: 1.1rem;">administered_penalties()</a></li>
            <li><a href="#received_penalties" style="color: #91C1E6; font-size: 1.1rem;">received_penalties()</a></li>
            <li><a href="#connection_history" style="color: #91C1E6; font-size: 1.1rem;">connection_history()</a></li>
            <li><a href="#permissions" style="color: #91C1E6; font-size: 1.1rem;">permissions()</a></li>
        </ul>
    </div>
</div>

<div align="center" id="server-class">
    <h1 style="padding-top: 5rem; padding-bottom: 0.2rem; font-weight: 800; font-size: 3rem;">Server Class 💻</h1>
    <p style="font-size: 1.2rem; color: white;">The Server class provides utility functions for interacting with the IW4M-Admin servers</p>
</div>

<div style="display: flex; gap: 1rem; padding: 20px; border: solid transparent; flex-wrap: wrap;">
    <div style="flex: 1; border: 0.15rem solid #82C8F5; border-radius: 10px; padding: 1rem; padding-left: 1.5rem;">
        <h2 style="font-size: 2.5rem; font-weight: 700;">Methods</h2>
        <ul style="list-style: none; padding: 0; line-height: 1.8;">
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="status">
                <strong><code style="font-size: 1.2rem;">status()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the current status of the server</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(dict)</code> - The status information from the server in JSON format.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="info">
                <strong><code>info()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the server information.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(dict)</code> - Information about the server in JSON format.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="get_server_ids">
                <strong><code>get_server_ids()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves a list of available servers and their corresponding IDs.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of dictionaries, each containing:
                        <ul>
                            <li>server (str): The name of the server</li>
                            <li>id (str): The unique identifier for the server</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="send_command">
                <strong><code>send_command(command: str)</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Executes an iw4m-admin console command and returns the response.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Parameters:</strong> <code>command (str)</code> - The command to execute.</li>
                    <li><strong>Returns:</strong> <code>(str)</code> - Response from the server.</li>
                    <li><strong>Raises:</strong> Exception if the request fails.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="read_chat">
                <strong><code>read_chat()</code></strong><br>
                <span style="font-size: 1rem; color: white;">Retrieves chat messages from the server.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of tuples, each containing the sender's name and their message.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="recent_clients">
                <strong><code>recent_clients(offset: int = 0)</code></strong><br>
                <span style="font-size: 1rem; color: white;">Retrieves a list of recent clients.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Parameters:</strong> <code>offset (int, optional)</code> - The offset for pagination (default is 0).</li>
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of dictionaries containing details about recent clients.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="find_player">
                <strong><code>find_player(name: str = "", xuid: str = "", count: int = 1, offset: int = 0, direction: int = 0)</code></strong><br>
                <span style="font-size: 1rem; color: white;">Finds players on the server by name or XUID.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Parameters:</strong> 
                        <ul>
                            <li><code>name (str, optional)</code>: The player's name</li>
                            <li><code>xuid (str, optional)</code>: The player's XUID</li>
                            <li><code>count (int, optional)</code>: Number of players to return (default is 1)</li>
                            <li><code>offset (int, optional)</code>: Offset for pagination (default is 0)</li>
                            <li><code>direction (int, optional)</code>: Search direction (default is 0)</li>
                        </ul>
                    </li>
                    <li><strong>Returns:</strong> <code>(str)</code> - The response from the server containing player information.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="get_users">
                <strong><code>get_users()</code></strong><br>
                <span style="font-size: 1rem; color: white;">Retrieves a list of users with their corresponding links.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of tuples, each containing:
                        <ul>
                            <li>player (str): The name of the user</li>
                            <li>href (str): The corresponding link of the user</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="get_players">
                <strong><code>get_players()</code></strong><br>
                <span style="font-size: 1rem; color: white;">Retrieves a list of players with their roles and corresponding links.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of dictionaries, each containing:
                        <ul>
                            <li>role (str): The role of the player (e.g., owner, senior, admin, user)</li>
                            <li>name (str): The name of the player</li>
                            <li>url (str): The corresponding link to the player</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="get_roles">
                <strong><code>get_roles()</code></strong><br>
                <span style="font-size: 1rem; color: white;">Retrieves a list of available roles on the server.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> A list of roles available.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="get_admins">
                <strong><code>get_admins(role: str = "all", count: int = None)</code></strong><br>
                <span style="font-size: 1rem; color: white;">Retrieves a list of administrators based on their role.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Parameters:</strong>
                        <ul>
                            <li><code>role (str)</code>: The role to filter by (default is "all")</li>
                            <li><code>count (int, optional)</code>: The number of admins to return (default is unlimited)</li>
                        </ul>
                    </li>
                    <li><strong>Returns:</strong> A list of dictionaries containing details about the administrators.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="get_audit_logs">
                <strong><code>get_audit_logs()</code></strong><br>
                <span style="font-size: 1rem; color: white;">Retrieves a list of audit logs from the server.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> A list of dictionaries containing:
                        <ul>
                            <li>type (str): The type of the audit log entry</li>
                            <li>origin (str): The origin of the log</li>
                            <li>href (str): The link to the log</li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
</div>

<div align="center" id="player-class">
    <h1 style="padding-top: 5rem; padding-bottom: 0.2rem; font-weight: 800; font-size: 3rem;">Player Class 👾</h1>
    <p style="font-size: 1.2rem; color: white;">The Player class provides utility functions for interacting with players on the IW4M-Admin server</p>
</div>


<div style="display: flex; gap: 1rem; padding: 20px; border: solid transparent; flex-wrap: wrap;">
    <div style="flex: 1; border: 0.15rem solid #82C8F5; border-radius: 10px; padding: 1rem; padding-left: 1.5rem;">
        <h2 style="font-size: 2.5rem; font-weight: 700;">Methods</h2>
        <ul style="list-style: none; padding: 0; line-height: 1.8;">
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="stats">
                <strong><code style="font-size: 1rem; color: white;">stats()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves statistics about the player.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(dict)</code> - Player statistics in JSON format.</li>
                </ul>
            </li> 
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="advanced_stats">
                <strong><code style="font-size: 1rem; color: white;">advanced_stats()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves advanced statistics for the player.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(dict)</code> - Advanced player statistics in JSON format.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="client_info">
                <strong><code style="font-size: 1rem; color: white;">client_info()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the client's information.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(dict)</code> - Client information in JSON format.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="info">
                <strong><code style="font-size: 1rem; color: white;">info()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the basic information about the player.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(dict)</code> - Player information in JSON format.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="chat_history">
                <strong><code style="font-size: 1rem; color: white;">chat_history()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the player's chat history.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of chat messages sent by the player.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="name_changes">
                <strong><code style="font-size: 1rem; color: white;">name_changes()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the history of the player's name changes.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of previous names.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="administered_penalties">
                <strong><code style="font-size: 1rem; color: white;">administered_penalties()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the penalties administered to the player.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of administered penalties.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="received_penalties">
                <strong><code style="font-size: 1rem; color: white;">received_penalties()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the penalties the player has received.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of received penalties.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="connection_history">
                <strong><code style="font-size: 1rem; color: white;">connection_history()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the player's connection history to the server.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of connection events.</li>
                </ul>
            </li>
            <li style="border-bottom: 1px solid #82C8F5; padding-bottom: 10px; margin-bottom: 10px;" id="permissions">
                <strong><code style="font-size: 1rem; color: white;">permissions()</code></strong><br>
                <span style="font-size: 1rem; font-weight: 500; color: white">Retrieves the permissions assigned to the player.</span>
                <ul style="margin-top: 5px; padding-left: 1.2rem;">
                    <li><strong>Returns:</strong> <code>(list)</code> - A list of permissions.</li>
                </ul>
            </li>
        </ul>
    </div>
</div>

<div style="padding-bottom: 2.5rem;"></div>

<h1>Come Play on Brownies SND 🍰</h1>
### Why Brownies? 🤔
- **Stability:** Brownies delivers a consistent, lag-free experience, making it the perfect choice for players who demand uninterrupted action
- **Community:** The players at Brownies are known for being helpful, competitive, and fun—something Orion can only dream of
- **Events & Features:** Brownies is constantly running unique events and offers more server-side customization options than Orion, ensuring every game feels fresh

---

#### [Brownies Discord](https://discord.gg/FAHB3mwrVF) | [Brownies IW4M](http://152.53.132.41:1624/) | Made With ❤️ By Budiworld

