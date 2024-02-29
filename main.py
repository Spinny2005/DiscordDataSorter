import os, json, re
from datetime import datetime

def __main__():
    user_info = get_user_info()
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
    print()
    print("\033[1mMain Menu\033[0m")
    print(f"User: {user_info[0]}")
    print(f"Email: {user_info[1]}")
    print(f"ID: {user_info[2]}")
    print(f"IP: {user_info[3]}")
    print(f"Phone: {user_info[4]}")
    print("")
    
    servers = get_servers()
    invites = get_server_invites()

    while True:
        print("1. Get servers")
        print("2. Get invites")
        print("3. Search messages")
        print("4. Get total messages")
        print("5. Exit")
        choice = input("Enter a choice: ")
        if choice == '1':
            print("\nIn order of creation: ")
            print("\n".join(servers))
            print(f"\nFound {len(servers)} servers you are in")
            print("")
        elif choice == '2':
            print("\nAll server invites you have sent: ")

            for i in range(0, len(invites), 10):
                # use max to avoid slicing out of range
                print(f"\nDisplaying invites {i+1} to {min(i+10, len(invites))} of {len(invites)}:")
                print("\n".join(invites[i:i+10]))


            print(f"\nFound {len(invites)} invites sent by you")
            print("")
        elif choice == '3':
            print()
            messages = search_messages_menu()
            print("\n\n".join(messages))
            print(f"\nFound {len(messages)} messages sent by you")
            print("")
        elif choice == '4':
            print(f"\nTotal messages sent by you in this data package: {total_messages()}")
            print("")
        elif choice == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            print("Invalid choice")
        input("Press enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')


def get_user_info():
    with open('package/account/user.json', 'r') as file:
        data = json.load(file)
        return data['global_name'], data['email'], data['id'], data['ip'], data['phone']


def get_servers():
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
    match = re.search(r'https?://(?:www\.)?(?:discord\.gg/[^\s,]+|discord\.com/invite/[^\s,]+)', line)
    if match:
        return match.group(0).rstrip(',').rstrip('"')
    return None

def is_valid_invite(invite_link):
    return invite_link is not None




def search_messages_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Notes: \n - Searching for numbers also returns dates and times. \n - Searching for non alphanumeric characters may return unexpected results. \n - Results with over 1000 messages may be truncated.\n\t(If you use VScode the max lines is 1000, cmd is 9999) \n - Some messages may be missing due to impropper csv formatting.\n\t(Blame discord, not me. I ain't trying to work around that shit) \n")
    search_term = input('Enter a search term: ')
    messages = search_messages(search_term)
    return messages


def search_messages(search_term):
    if not search_term:
        print("No search term entered")
        return []
    messages = []
    for channel_dir in os.listdir('package/messages'):
        channel_path = os.path.join('package/messages', channel_dir)
        if os.path.isdir(channel_path):
            for file_name in os.listdir(channel_path):
                file_path = os.path.join(channel_path, file_name)
                if file_name == 'messages.csv':
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            if search_term.lower() in line.lower():
                                parts = line.strip().split(',', 2)
                                if len(parts) >= 3 and len(parts[1].split()) >= 2:
                                    date_time = f"\033[1;30m{parts[1].split()[0]} - {parts[1].split()[1][:8]}\033[0m"
                                    message = parts[2].strip().rstrip(',')
                                    messages.append((parts[1], f"{date_time} - {message}"))

    messages.sort(key=lambda x: x[0])
    sorted_messages = [msg[1] for msg in messages]
    return sorted_messages


def total_messages():
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