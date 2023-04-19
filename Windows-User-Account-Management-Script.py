import ctypes, sys
import subprocess
from getpass import getpass
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(filename='account-management.log', level=logging.INFO)

# log account creation
now = datetime.now()

# Checks if the user running the script has administrator privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to create a standard user account
def create_account():

    username = input("Enter username: ")
    
    password = getpass("Enter password for account: ")
    check_password = getpass("Enter password again: ")

    # Verify that the password was entered correctly
    while password != check_password:
        print("Passwords do not match")
        password = getpass("Enter password for account: ")
        check_password = getpass("Enter password again: ")


    # Define the command to create the user
    create_account = f"net user {username} {password} /add"

    # Run the command to create the user
    try:
        result = subprocess.run(create_account, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if the command was successful and print an appropriate message
        if result.returncode == 0:
            print(f"User {username} created successfully.")
            logging.info(f"Account {username} created successfully {now}")
        else:
            print(f"Error creating user {username}.")
            print(result.stderr.decode())
            logging.critical(f"Failed to create user {username} {now}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error creating user {username}.")
        print(e.stderr.decode())

# Function to create an admin user account
def create_admin():
    account_name = input("What account do you want to make an admin: ")
    make_admin = f"net localgroup administrators {account_name} /add"

    try:
        create_admin_account = subprocess.run(make_admin, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if create_admin_account.returncode == 0:
            print(f"{account_name} is now apart of administrator group")
        else:
            print(f"Error making {account_name} admin")
            logging.critical(f"Failed to make {account_name} administrator {now}")

    except subprocess.CalledProcessError as e:
        print(f"Error making {account_name} admin.")
        print(e.stderr.decode())

# Function to assign a user account to a group
def assign_account_to_group():
    # Command to list all local group
    get_groups = "net localgroup"
    try:
        get_all_groups = subprocess.run(get_groups, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Print the list of all the local groups on the system
        if get_all_groups.returncode == 0:
            print("All groups are listed")
            for group in get_all_groups.stdout.decode().splitlines():
                if group:
                    print(group)
        else:
            print(f"Error getting groups")
    except subprocess.CalledProcessError as e:
        print(f"Error getting all group.")
        print(e.stderr.decode())
        logging.error(f"Failed to get all local groups {now}")

    # Get the account name and the group name from the user
    account_name = input("Account name: ")
    group = input(f"What group should {account_name} be added to: ")

    # Command to add user to local group
    make_admin = f"net localgroup {group} {account_name} /add"
    
    try:
        create_admin_account = subprocess.run(make_admin, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if create_admin_account.returncode == 0:
            print(f"{account_name} is now apart of {group} group")
        else:
            print(f"Error adding {account_name} to {group}")
    except subprocess.CalledProcessError as e:
        print(f"Error making {account_name} admin.")
        print(e.stderr.decode())

def delete_account():
    list_accounts = "net user"
    try:
        all_accounts = subprocess.run(list_accounts, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if all_accounts.returncode == 0:
            print("All Local Accounts are listed")
            for accounts in all_accounts.stdout.decode().splitlines():
                if accounts:
                    print(accounts)
        else:
            print(f"Error getting acounts")
    except subprocess.CalledProcessError as e:
        print(f"Error getting all accounts.")
        print(e.stderr.decode())

    username = input("Account to delete: ")
    delete_account_command = f"net user {username} /DELETE"

    try:
        delete_account = subprocess.run(delete_account_command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if delete_account.returncode == 0:
            print(f"{username} was successfully deleted")
        else:
            print("Failed to delete account")
    except subprocess.CalledProcessError as e:
        print("An error has happened in delete account")
        print(e.stderr.decode())

def enable_disable_account():
    ask_to_enable_disable = input("Would you like to enable or disable: ")
    username = input("Enter the username: ")
    enable_account_command = f"net user {username} /ACTIVE:yes"
    disable_account_command = f"net user {username} /ACTIVE:no"

    if ask_to_enable_disable == "enable":
        try:
            enable_account = subprocess.run(enable_account_command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if enable_account.returncode == 0:
                print(f"{username} was successfully enabled")
            else:
                print("Failed to enable account")
                logging.info(f"Failed to enable account: {username} {now}")
        except subprocess.CalledProcessError as e:
            print("An error has happened when enabling account")
            print(e.stderr.decode())

    if ask_to_enable_disable == "disable":
        try:
            disable_account = subprocess.run(disable_account_command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if disable_account.returncode == 0:
                print(f"{username} was successfully disabled")
            else:
                print("Failed to disabled account")
                logging.info(f"Failed to disable account {username} {now}")
        except subprocess.CalledProcessError as e:
            print("An error has happened when disabling account")
            print(e.stderr.decode())



if is_admin():
    # Code of your program here
    try:
        print("ctrl-c to quit")

        while True:
            print("1. To Create account \t   2. Make account admin")
            print("3. Manually add to group   4. Delete account")
            print("5. Enable/Disable Accounts 6. Quit program")
            print("-"*50)

            # Valildates the user entered a number
            try:
                choice = int(input("Your choice: "))
            except ValueError:
                print("Please enter a number")

            options = {
                1: create_account,
                2: create_admin,
                3: assign_account_to_group,
                4: delete_account,
                5: enable_disable_account,
                6: quit,
            }

            # Runs the funciton based of user input
            if choice in options:
                options[choice]()
            else:
                print("Please enter a valid choice (1-4)")

            # Askes if the user want to change their choice
            switch_choice = input("Do you want to switch choice? (y/n) ")
            if switch_choice.lower() == "y":
                if choice == 1 or choice == 2 or choice == 3:
                    continue
            elif switch_choice.lower() == "n":
                while True:
                    options[choice]()
            else:
                break

    except KeyboardInterrupt:
        quit()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

input("Press enter to exit")