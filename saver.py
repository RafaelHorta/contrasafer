import argparse
from colorama import init, Fore
from classes.crypt import Crypt
from classes.manager_files import ManagerFiles

__version__ = 1.0
__author__ = 'RafaelHorta'
__github__ = 'https://github.com/RafaelHorta?tab=repositories'
__doc__ = 'Password Saver'

init() # Initialize colorama

# - - - - - - - - - - - - - - - - - -
# Function to list records
def list_records():
    print(f"\n{Fore.MAGENTA}Record list:{Fore.RESET}")

    records = objManagerFile.list_sitenames

    if not records:
        print(f"{Fore.RED}List empty!{Fore.RESET}")
        return False

    for data in records:
        print(f"{Fore.BLUE}* {data}{Fore.RESET}")

    return True

# - - - - - - - - - - - - - - - - - -
# Main function
def main():
    global file_name
    global file_extension

    # Print message to select options

    print(f"{Fore.WHITE}Select option number:{Fore.BLUE}")
    print(f"1. To save data")
    print(f"2. To list records")
    print(f"3. To view data for a record")
    print(f"4. To delete a record")
    print(f"5. Leave{Fore.RESET}")

    while True:
        try:
            option = int(input(f"\n{Fore.WHITE}Enter option number:{Fore.RESET} "))

        except Exception as ex:
            print(f"{Fore.RED}{ex}{Fore.RESET}")
            continue

        # Option to save data
        if option == 1:
            print(f"{Fore.MAGENTA}- - - - - - - - - - - - - - - - - - - - - - -:{Fore.RESET}")

            while True:
                site = input("Enter website or app name: ").lower()

                if objManagerFile.exist_data_file(site):
                    print(f"{Fore.RED}This website or app already exist!{Fore.RESET}")
                else:
                    break

            username = input("Enter username or any data to log in: ")
            password = input("Enter password: ")

            objCrypt = Crypt()

            objManagerFile.add_data_file({
                'site': site,
                'username': username,
                'password': objCrypt.encrypt_text(password),
                'key': objCrypt.get_key
            })

            print(f"{Fore.GREEN}Data saved successfully!{Fore.RESET}")

        # Option to list records
        elif option == 2:
            list_records()

        # Option to view data
        elif option == 3:
            if not list_records():
                continue

            site = input("\nEnter website or app name: ").lower()
            session_data = objManagerFile.search_data_file(site)

            if session_data is None:
                print(f"{Fore.RED}Not exist \"{site}\"!{Fore.RESET}")
                continue

            objCrypt = Crypt(session_data['key'])
            get_password = objCrypt.decrypt_text(session_data['password'])

            print(f"\nUsername:\t{Fore.YELLOW}\"{session_data['username']}\"{Fore.RESET}")
            print(f"Password:\t{Fore.YELLOW}\"{get_password}\"{Fore.RESET}")

        # Option to remove records
        elif option == 4:
            if not list_records():
                continue

            site = input("\nEnter website or app name to remove: ").lower()

            if objManagerFile.delete_data_file(site):
                print(f"{Fore.GREEN}Removed \"{site}\" website or app{Fore.RESET}")
            else:
                print(f"{Fore.RED}\"{site}\" cannot be deleted. Please check it on the list{Fore.RESET}")

        # Option to leave
        elif option == 5:
            print(f"{Fore.YELLOW}See you later!{Fore.RESET}\n")
            break

        else:
            print(f"{Fore.RED}This option doesn't exist!{Fore.RESET}\n")


if __name__ == '__main__':
    try:
        # Get and parser arguments
        parser = argparse.ArgumentParser(description = "Name and extension file")
        parser.add_argument('--name', type = str, default = "passwords")
        parser.add_argument('--type', type = str, default = "txt")
        args = parser.parse_args()

        objManagerFile = ManagerFiles(args.name, args.type) # Init Manager Files class

        main()

    except Exception as ex:
        print(f"{Fore.RED}{ex}{Fore.RESET}")