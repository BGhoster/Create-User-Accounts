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
    # Prompt the user for username and password
    username = ""
    password = ""


    while not username:
        username = input("Enter username: ")
    while not password:
        password = getpass("Enter password for account: ")
    

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

if is_admin():
    # Code of your program here
    try:
        print("ctrl-c to quit")


        while True:
            print("1. To Create account \t 2. Make account admin")
            print("1. To Create account \t 2. Make account admin")
            print("-"*50)

            choice = input("Your choice: ")

            if choice == "1":
                create_account()
            elif choice == "2":
                create_admin()
            else:
                print("Please enter a valid choice (1 or 2)")

            switch_choice = input("Do you want to switch account types? (y/n) ")

            if switch_choice.lower() == "y":
                if choice == "1":
                    print("Switching to create admin account")
                    choice = "2"
                elif choice == "2":
                    print("Switching to create account")
                    choice = "1"
            else:
                break

    except KeyboardInterrupt:
        quit()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

input("Press enter to exit")