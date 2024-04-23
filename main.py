import os, json, re, requests, time

def __main__():
    # Load user data
    user_info = get_user_info()

    # Title display
    print("\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m")
    print("██████╗░██╗░██████╗░█████╗░░█████╗░██████╗░██████╗░  ██████╗░░█████╗░████████╗░█████╗░")
    print("██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗")
    print("██║░░██║██║╚█████╗░██║░░╚═╝██║░░██║██████╔╝██║░░██║  ██║░░██║███████║░░░██║░░░███████║")
    print("██║░░██║██║░╚═══██╗██║░░██╗██║░░██║██╔══██╗██║░░██║  ██║░░██║██╔══██║░░░██║░░░██╔══██║")
    print("██████╔╝██║██████╔╝╚█████╔╝╚█████╔╝██║░░██║██████╔╝  ██████╔╝██║░░██║░░░██║░░░██║░░██║")
    print("╚═════╝░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░  ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝")
    print()
    print("░██████╗░█████╗░██████╗░████████╗███████╗██████╗░")
    print("██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗")
    print("╚█████╗░██║░░██║██████╔╝░░░██║░░░█████╗░░██████╔╝")
    print("░╚═══██╗██║░░██║██╔══██╗░░░██║░░░██╔══╝░░██╔══██╗")
    print("██████╔╝╚█████╔╝██║░░██║░░░██║░░░███████╗██║░░██║")
    print("╚═════╝░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝")
    print("\033[0m")
    print("By Spencer Boggs\n")

    # Main menu
    print("\033[1mMain Menu\033[0m")

    # print a table of the user's data
    print(f"{'User':<15}  {'Email':<27}  {'ID':<20}  {'IP':<15}  {'Phone':<20}")
    print(f"{user_info[0]:<15}  {user_info[1]:<27}  {user_info[2]:<20}  {user_info[3]:<15}  {user_info[4]:<20}")
    print("")

    # Load server and invite data
    print("Loading data...")
    servers = get_servers()
    invites = get_server_invites()
    valid_invites = []
    print("Data loaded\n")

    # Main menu loop
    while True:
        print("1. Get servers")
        print("2. Get all invites")
        print("3. Get valid invites (slow)")
        print("4. Get total messages")
        print("5. Search messages")
        print("6. Display all messages")
        print("7. Search messages from unknown servers")
        print("8. Display all messages from unknown servers")
        print("9. Exit")
        choice = input("Enter a choice: ")

        # Get all servers
        if choice == '1':
            print("\nIn order of creation: ")
            print("\n".join(servers))
            print(f"\nFound {len(servers)} servers you are in")
            print("")
            input("Press enter to continue...") 

        # Get all invites
        elif choice == '2':
            print("\nAll server invites you have sent: ")
            for i in range(0, len(invites), 10):
                print(f"\nDisplaying invites {i+1} to {min(i+10, len(invites))} of {len(invites)}:")
                print("\n".join(invites[i:i+10]))
            print(f"\nFound {len(invites)} invites sent by you")
            print("")
            input("Press enter to continue...") 

        # Get valid invites
        elif choice == '3':
            print("\nChecking for valid invites...\n")
            valid_invites = get_working_invites()

            if valid_invites != []:
                print("\n")
                os.system('cls' if os.name == 'nt' else 'clear')

                print("All valid invites have already been found")
                print("\nValid invites: ")
                for i in range(0, len(valid_invites), 10):
                    print(f"\nDisplaying invites {i+1} to {min(i+10, len(valid_invites))} of {len(valid_invites)}:")
                    print("\n".join(valid_invites[i:i+10]))
                print(f"\nFound {len(valid_invites)} valid invites sent by you")
            input("Press enter to continue...") 

        # Get total messages
        elif choice == '4':
            print(f"\nTotal messages sent by you in this data package: {total_messages()}")
            print("")
            input("Press enter to continue...") 

        # Search messages
        elif choice == '5':
            while True:
                print()
                messages = search_messages_menu()
                print("\n\n".join(messages))
                print(f"\nFound {len(messages)} messages sent by you")
                print("")
                choice = input("Type 'e' to exit. Enter to continue: ")
                if choice == 'e':
                    break

        # Display all messages
        elif choice == '6':
            display_all_messages()

        # Search messages from unknown servers
        elif choice == '7':
            while True:
                print()
                messages = search_messages_unknown_servers_menu()
                print("\n\n".join(messages))
                print(f"\nFound {len(messages)} messages sent by you in unknown servers")
                print("")
                choice = input("Type 'e' to exit. Enter to continue: ")
                if choice == 'e':
                    break

        # Display all messages from unknown servers
        elif choice == '8':
            display_all_unknown_messages()

        # Exit
        elif choice == '9':
            print("\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        # Easter eggs
        elif choice == "69" or choice == "420":
            print()
            print("Very funny...")
            input("Press enter to continue...") 

        # Invalid choice
        else:
            print("Invalid choice")

        print("\n")
        os.system('cls' if os.name == 'nt' else 'clear')


def get_user_info():
    """ 
        Returns the user's global name, email, id, ip, and phone number
    """
    with open('package/account/user.json', 'r') as file:
        data = json.load(file)
        return data['global_name'], data['email'], data['id'], data['ip'], data['phone']


def get_servers():
    """ 
        Returns a list of servers the user is in
    """
    servers = []
    for server in os.listdir('package/servers'):
        if os.path.isdir(f'package/servers/{server}'):
            with open(f'package/servers/{server}/guild.json', 'r') as file:
                data = json.load(file)
                servers.append(f'{data["id"]} - {data["name"]}')
    # sort by lowest number first
    servers.sort(key=lambda x: int(x.split(' - ')[0]))
    return servers


def get_server_invites():
    """
    Returns a list of all invites the user has sent
    """
    invites = set()
    for channel_dir in os.listdir('package/messages'):
        channel_path = os.path.join('package/messages', channel_dir)
        if os.path.isdir(channel_path):
            for file_name in os.listdir(channel_path):
                file_path = os.path.join(channel_path, file_name)
                if file_name.endswith('.json'):  # Check for JSON files
                    with open(file_path, 'r', encoding='utf-8') as file:
                        try:
                            data = json.load(file)
                            if isinstance(data, list):  # Ensure data is a list
                                for message in data:
                                    if isinstance(message, dict):  # Ensure message is a dictionary
                                        invite_link = extract_invite_link(message.get('Contents', ''))
                                        if is_valid_invite(invite_link):
                                            invites.add(invite_link)
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in file: {file_path}")
                            continue
    invites_list = list(invites)
    invites_list.sort()
    return invites_list




def extract_invite_link(contents):
    """ 
        Extracts an invite link from message contents
    """
    match = re.search(r'https?://(?:www\.)?(?:discord\.gg/[^\s,]+|discord\.com/invite/[^\s,]+)', contents)
    if match:
        return match.group(0).rstrip(',').rstrip('"')
    return None

def is_valid_invite(invite_link):
    """ 
        Checks if an invite link is valid
    """
    return invite_link is not None



def get_invite_codes():
    """ 
        Returns a list of invite codes
    """
    full_links = get_server_invites()
    return [link.split('/')[-1] for link in full_links]


def get_working_invites():
    """
        Returns a list of valid invite links
    """
    code_list = get_invite_codes()
    if os.path.exists('invites.json'):
        with open('invites.json', 'r') as file:
            data = json.load(file)
            if data['all']:
                print("All invites have been checked. Skipping to the end.")
                return [f"https://discord.gg/{code}" for code in data['valid']]
            
            elif data['latest'] in code_list:
                print(f"Skipping to the latest checked invite: {data['latest']}")
                code_list = code_list[code_list.index(data['latest'])+1:]
                print(f"Valid codes found so far: ")
                print("\n".join([f"https://discord.gg/{code}" for code in data['valid']]), "\n")
                print(f"Remaining invites to check: {len(code_list)}")
    else:
        with open('invites.json', 'w') as file:
            json.dump({"valid": [], "invalid": [], "latest": "", "all": False}, file)

    valid_codes = []
    valid_links = []

    print("Notes:\n - The valid invites found are sometimes buggy. \n - Sometimes they claim to be invalid but are actually valid. \n - Try codes in your browser and not on discord. \n - This process is slow due to discord API rate limits.\n")

    print(f"Estimated time: {len(code_list) * 2} seconds\n")

    for invite_code in code_list:

        api_endpoint = f"https://discord.com/api/v9/invites/{invite_code}"
        headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type": "application/json",
        }

        response = requests.get(api_endpoint, headers=headers)

        if response.status_code == 429:
            print("Rate limited. Try again later.")
            print("Wait at least 15 minutes (can last up to an hour). Discord api rate limits are strict.")
            print("The valid codes found so far are saved. You can continue from where you left off later.\n")

            if len(valid_codes) > len(data['valid']):
                with open('invites.json', 'w') as file:
                    json.dump({"valid": valid_codes, "latest": invite_code, "all": False}, file)

            return []
        
        if response.status_code == 200:
            valid_codes.append(invite_code)
            valid_links.append("https://discord.gg/" + invite_code)
            print("Valid invite found: https://discord.gg/" + invite_code)

        time.sleep(1.2)

    with open('invites.json', 'w') as file:
        json.dump({"valid": valid_codes, "latest": "", "all": True}, file)

    return valid_links


def search_messages_menu():
    """ 
        Prompts the user for a search term and returns a list of messages containing the search term
    """
    print("\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Notes: \n - Searching for numbers also returns dates and times as well as message IDs. \n - Searching for non alphanumeric characters may return unexpected results. \n - Results with over 1000 messages may be truncated.\n\t(If you use VScode the max messages displayed is 330 cmd is 3330) \n - Some messages may be missing due to impropper json formatting.\n\t(Blame discord, not me. I ain't trying to work around that shit) \n")
    search_term = input('Enter a search term: ')
    print("Seaching. This may take a minute.")
    messages = search_messages(search_term)
    return messages


def search_messages(search_term):
    """ 
        Searches through the messages folder for all messages containing search_term  
    """
    if not search_term:
        print("No search term entered")
        return []
    messages = []

    for channel_dir in os.listdir('package/messages'):
        channel_path = os.path.join('package/messages', channel_dir)

        if os.path.isdir(channel_path):
            for file_name in os.listdir(channel_path):
                file_path = os.path.join(channel_path, file_name)

                if file_name.endswith('.json'):  # Check for JSON files
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        for message in data:
                            if 'Contents' in message:
                                server_name = ""
                                date_time = message['Timestamp']
                                content = message['Contents']
                                if os.path.exists(os.path.join(channel_path, 'channel.json')):
                                    with open(os.path.join(channel_path, 'channel.json'), 'r', encoding='utf-8') as guild_file:
                                        data = json.load(guild_file)
                                        if data.get('guild'):
                                            server_name = (f"{data['guild']['name']} in {data['name']}")
                                        else:
                                            with open('package/messages/index.json', 'r', encoding='utf-8') as index_file:
                                                index_data = json.load(index_file)
                                                temp = channel_dir[1:]
                                                if temp in index_data:
                                                    server_name = index_data[temp]
                                if search_term.lower() in content.lower():
                                    if server_name:
                                        messages.append(f"\033[1;34mMessage sent in {server_name}\033[0m\n{date_time} - {content}")
                                    else:
                                        messages.append(f"\033[1;34mMessage sent in Unknown server\033[0m\n{date_time} - {content}")

    messages.sort(key=lambda x: x.split('\n')[1])
    return messages


def total_messages():
    """ 
        Returns the total number of messages in the messages folder
    """
    total = 0
    for channel_dir in os.listdir('package/messages'):
        channel_path = os.path.join('package/messages', channel_dir)
        if os.path.isdir(channel_path):
            for file_name in os.listdir(channel_path):
                file_path = os.path.join(channel_path, file_name)
                if file_name.endswith('.json'):  # Check for JSON files
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        total += len(data)
    return total



def display_all_messages():
    """ 
        Displays all messages from all channels
    """
    print("\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    
    messages = []

    print(f"Compiling messages from all channels...")
    print("This may take a minute\n")

    for channel_dir in os.listdir('package/messages'):
        channel_path = os.path.join('package/messages', channel_dir)

        if os.path.isdir(channel_path):
            for file_name in os.listdir(channel_path):
                file_path = os.path.join(channel_path, file_name)

                if file_name.endswith('.json'):  # Check for JSON files
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        for message in data:
                            if 'Contents' in message:
                                server_name = ""
                                date_time = message['Timestamp']
                                content = message['Contents']
                                if os.path.exists(os.path.join(channel_path, 'channel.json')):
                                    with open(os.path.join(channel_path, 'channel.json'), 'r', encoding='utf-8') as guild_file:
                                        data = json.load(guild_file)
                                        if data.get('guild'):
                                            server_name = (f"{data['guild']['name']} in {data['name']}")
                                        else:
                                            with open('package/messages/index.json', 'r', encoding='utf-8') as index_file:
                                                index_data = json.load(index_file)
                                                temp = channel_dir[1:]
                                                if temp in index_data:
                                                    server_name = index_data[temp]
                                if server_name:
                                    messages.append(f"\033[1;34mMessage sent in {server_name}\033[0m\n{date_time} - {content}")
                                else:
                                    messages.append(f"\033[1;34mMessage sent in Unknown server\033[0m\n{date_time} - {content}")

    messages.sort(key=lambda x: x.split('\n')[1])

    num_per_page = None
    while not num_per_page:
        try:
            num_per_page = int(input("Enter the number of messages to display per page: "))
        except ValueError:
            print("Invalid input")
        if num_per_page < 1:
            print("Invalid input")
            num_per_page = None
        if num_per_page > 1000:
            if num_per_page > len(messages) and len(messages) < 1000:
                print(f"Max messages per page is {len(messages)}")
            else:
                print("Max messages per page is 1000")
            num_per_page = None
    
    for i in range(0, len(messages), num_per_page):
        print("")
        print("\n\n".join(messages[i:i+num_per_page]))
        print(f"\nDisplaying messages {i+1} to {min(i+num_per_page, len(messages))} of {len(messages)}")
        print()
        choice = input("Type 'e' to exit. Enter to continue: ") 
        if choice == 'e':
            break
        os.system('cls' if os.name == 'nt' else 'clear')



def search_messages_unknown_servers_menu():
    """ 
        Prompts the user for a search term and returns a list of messages sent from unknown servers containing the search term
    """
    print("\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Notes: \n - Searching for numbers also returns dates and times as well as message IDs. \n - Searching for non alphanumeric characters may return unexpected results. \n - Results with over 1000 messages may be truncated.\n\t(If you use VScode the max messages displayed is 330 cmd is 3330) \n - Some messages may be missing due to impropper json formatting.\n\t(Blame discord, not me. I ain't trying to work around that) \n")
    search_term = input('Enter a search term: ')
    print("Seaching. This may take a minute.")
    messages = search_messages_unknown_servers(search_term)
    return messages


def search_messages_unknown_servers(search_term):
    """ 
        Searches through the messages folder for all messages sent from unknown servers containing search_term  
    """
    if not search_term:
        print("No search term entered")
        return []
    messages = []

    for channel_dir in os.listdir('package/messages'):
        channel_path = os.path.join('package/messages', channel_dir)

        if os.path.isdir(channel_path):
            for file_name in os.listdir(channel_path):
                file_path = os.path.join(channel_path, file_name)

                if file_name.endswith('.json'):  # Check for JSON files
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        for message in data:
                            if 'Contents' in message:
                                server_name = ""
                                date_time = message['Timestamp']
                                content = message['Contents']
                                if os.path.exists(os.path.join(channel_path, 'channel.json')):
                                    with open(os.path.join(channel_path, 'channel.json'), 'r', encoding='utf-8') as guild_file:
                                        data = json.load(guild_file)
                                        if data.get('guild'):
                                            server_name = (f"{data['guild']['name']} in {data['name']}")
                                        else:
                                            with open('package/messages/index.json', 'r', encoding='utf-8') as index_file:
                                                index_data = json.load(index_file)
                                                temp = channel_dir[1:]
                                                if temp in index_data:
                                                    server_name = index_data[temp]
                                if not server_name and search_term.lower() in content.lower():
                                    messages.append(f"{date_time} - {content}")

    messages.sort()
    return messages


def display_all_unknown_messages():
    print("\n")
    os.system('cls' if os.name == 'nt' else 'clear')

    messages = []

    print(f"Sorting through {total_messages()} messages...")
    print("This may take a minute\n")

    for channel_dir in os.listdir('package/messages'):
        channel_path = os.path.join('package/messages', channel_dir)

        if os.path.isdir(channel_path):
            for file_name in os.listdir(channel_path):
                file_path = os.path.join(channel_path, file_name)

                if file_name.endswith('.json'):  # Check for JSON files
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        for message in data:
                            if 'Contents' in message:
                                server_name = ""
                                date_time = message['Timestamp']
                                content = message['Contents']
                                if os.path.exists(os.path.join(channel_path, 'channel.json')):
                                    with open(os.path.join(channel_path, 'channel.json'), 'r', encoding='utf-8') as guild_file:
                                        data = json.load(guild_file)
                                        if data.get('guild'):
                                            server_name = (f"{data['guild']['name']} in {data['name']}")
                                        else:
                                            with open('package/messages/index.json', 'r', encoding='utf-8') as index_file:
                                                index_data = json.load(index_file)
                                                temp = channel_dir[1:]
                                                if temp in index_data:
                                                    server_name = index_data[temp]
                                if not server_name:
                                    messages.append(f"{date_time} - {content}")

    messages.sort()
    
    num_per_page = None
    while not num_per_page:
        try:
            num_per_page = int(input("Enter the number of messages to display per page: "))
        except ValueError:
            print("Invalid input")
        if num_per_page < 1:
            print("Invalid input")
            num_per_page = None
        if num_per_page > 1000:
            if num_per_page > len(messages) and len(messages) < 1000:
                print(f"Max messages per page is {len(messages)}")
            else:
                print("Max messages per page is 1000")
            num_per_page = None
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\nFound {len(messages)} messages sent by you in unknown servers\n")
    for i in range(0, len(messages), num_per_page):
        print("\n\n".join(messages[i:i+num_per_page]))
        print(f"\nDisplaying messages {i+1} to {min(i+num_per_page, len(messages))} of {len(messages)}\n")
        choice = input("Type 'e' to exit. Enter to continue: ") 
        if choice == 'e':
            break
        os.system('cls' if os.name == 'nt' else 'clear')



if __name__ == '__main__':
    __main__()