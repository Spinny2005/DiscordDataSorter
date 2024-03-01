import os, json, re, requests, time

def __main__():
    # Load user data
    user_info = get_user_info()

    # Title display
    print("\n")
    os.system('cls' if os.name == 'nt' else 'clear')
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
    print("By Spencer Boggs\n")

    # Main menu
    print("\033[1mMain Menu\033[0m")
    print(f"User: {user_info[0]}")
    print(f"Email: {user_info[1]}")
    print(f"ID: {user_info[2]}")
    print(f"IP: {user_info[3]}")
    print(f"Phone: {user_info[4]}")
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
        print("4. Search messages")
        print("5. Get total messages")
        print("6. Exit")
        choice = input("Enter a choice: ")

        # Get all servers
        if choice == '1':
            print("\nIn order of creation: ")
            print("\n".join(servers))
            print(f"\nFound {len(servers)} servers you are in")
            print("")

        # Get all invites
        elif choice == '2':
            print("\nAll server invites you have sent: ")
            for i in range(0, len(invites), 10):
                print(f"\nDisplaying invites {i+1} to {min(i+10, len(invites))} of {len(invites)}:")
                print("\n".join(invites[i:i+10]))
            print(f"\nFound {len(invites)} invites sent by you")
            print("")

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

        # Search messages
        elif choice == '4':
            print()
            messages = search_messages_menu()
            print("\n\n".join(messages))
            print(f"\nFound {len(messages)} messages sent by you")
            print("")

        # Get total messages
        elif choice == '5':
            print(f"\nTotal messages sent by you in this data package: {total_messages()}")
            print("")

        # Exit
        elif choice == '6':
            print("\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        elif choice == '7':
            print("\n".join(search_messages("https://discord.gg/")))

        # Invalid choice
        else:
            print("Invalid choice")

        # Await user input to continue
        input("Press enter to continue...")
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
                if file_name == 'messages.csv':
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            invite_link = extract_invite_link(line)
                            if is_valid_invite(invite_link):
                                invites.add(invite_link)
    invites_list = list(invites)
    invites_list.sort()
    return invites_list


def extract_invite_link(line):
    """ 
        Extracts an invite link from a line of text
    """
    match = re.search(r'https?://(?:www\.)?(?:discord\.gg/[^\s,]+|discord\.com/invite/[^\s,]+)', line)
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
    print("Notes: \n - Searching for numbers also returns dates and times as well as message IDs. \n - Searching for non alphanumeric characters may return unexpected results. \n - Results with over 1000 messages may be truncated.\n\t(If you use VScode the max lines is 1000, cmd is 9999) \n - Some messages may be missing due to impropper csv formatting.\n\t(Blame discord, not me. I ain't trying to work around that shit) \n")
    search_term = input('Enter a search term: ')
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
                # parts[1], f"\033[1;34m{server_name}\033[0m\n{date_time} - {message}"

                if file_name == 'messages.csv':
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            # Set up variables
                            server_name = ""
                            parts = ""
                            date_time = ""
                            message = ""

                            # If the search term is in the line
                            if search_term.lower() in line.lower():
                                parts = line.strip().split(',', 2)
                                if len(parts) >= 3 and len(parts[1].split()) >= 2:
                                    date_time = f"\033[1;30m{parts[1].split()[0]} - {parts[1].split()[1][:8]}\033[0m"
                                    message = parts[2].strip().rstrip(',')

                                # Get the server name
                                if os.path.exists(os.path.join(channel_path, 'channel.json')):
                                    with open(os.path.join(channel_path, 'channel.json'), 'r', encoding='utf-8') as guild_file:
                                        data = json.load(guild_file)
                                        if data.get('guild'):
                                            server_name = data['guild']['name']
                                        else:
                                            with open('package/messages/index.json', 'r', encoding='utf-8') as index_file:
                                                index_data = json.load(index_file)
                                                temp = channel_dir[1:]
                                                if temp in index_data:
                                                    server_name = index_data[temp]

                                # Append the message along with the server_name
                                if date_time != "" and message != "":
                                    if server_name:
                                        # messages.append((parts[1], f"\033[1;34m{server_name}\033[0m\n{date_time} - {message}"))
                                        messages.append(("", f"\033[1;34mMessage sent in {server_name}\033[0m\n{date_time} - {message}"))
                                    else:
                                        # messages.append((parts[1], f"\033[1;34mMessage sent in Unknown server\033[0m\n{date_time} - {message}"))
                                        messages.append(("", f"\033[1;34mMessage sent in Unknown server\033[0m\n{date_time} - {message}"))


    messages.sort(key=lambda x: x[0])
    sorted_messages = [msg[1] for msg in messages]
    return sorted_messages


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
                if file_name == 'messages.csv':
                    with open(file_path, 'r', encoding='utf-8') as file:
                        total += sum(1 for line in file)
    return total


if __name__ == '__main__':
    __main__()