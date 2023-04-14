import ctypes, sys
import subprocess
from getpass import getpass

# Checks for admin privs
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Creates standard accounts
def create_account():

    username = input("Enter username: ")
    
    password = getpass("Enter password for account: ")
    check_password = getpass("Enter password again: ")

    while password != check_password:
        # Keeps reprompting until password matches
        print("Passwords do not match")
        password = getpass("Enter password for account: ")
        check_password = getpass("Enter password again: ")


    # Define the command to create the user
    create_account = f"net user {username} {password} /add"

    # Run the command to create the user
    try:
        result = subprocess.run(create_account, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print(f"User {username} created successfully.")
        else:
            print(f"Error creating user {username}.")
            print(result.stderr.decode())
    
    except subprocess.CalledProcessError as e:
        print(f"Error creating user {username}.")
        print(e.stderr.decode())

# Creates admin accounts
def create_admin():
    account_name = input("What account do you want to make an admin: ")
    make_admin = f"net localgroup administrators {account_name} /add"

    try:
        create_admin_account = subprocess.run(make_admin, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if create_admin_account.returncode == 0:
            print(f"{account_name} is now apart of administrator group")
        else:
            print(f"Error making {account_name} admin")
    except subprocess.CalledProcessError as e:
        print(f"Error making {account_name} admin.")
        print(e.stderr.decode())

# Assign accounts to groups
def assign_account_to_group():
    get_groups = "net localgroup"
    try:
        get_all_groups = subprocess.run(get_groups, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

    account_name = input("Account name: ")
    group = input(f"What group should {account_name} be added to: ")
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
    username = input("Account to delete")
    delete_account_command = f"net user {username} /DELETE"

    try:
        delete_account = subprocess.run(delete_account_command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if delete_account.returncode == 0:
            print(f"{username} was successfully deleted")
        else:
            print("Failed to delete account")
    except subprocess.CalledProcessError as e:
        print("An error hsa happened in delete account")
        print(e.stderr.decode())


if is_admin():
    # Code of your program here
    try:
        print("ctrl-c to quit")

        while True:
            print("1. To Create account \t 2. Make account admin")
            print("3. Manually add to group")
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