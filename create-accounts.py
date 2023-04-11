import ctypes, sys
import subprocess
from getpass import getpass

# Checks for admin privs
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_account():
    # Prompt the user for username and password
    username = ""
    password = ""


    while not username:
        username = input("Enter username: ")
    while not password:
        password = getpass("Enter password for account: ")
    

    # Define the command to create the user
    command = f"net user {username} {password} /add"

    # Run the command to create the user
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"User {username} created successfully.")
        else:
            print(f"Error creating user {username}.")
            print(result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error creating user {username}.")
        print(e.stderr.decode())


if is_admin():
    # Code of your program here
    try:
        print("ctrl-c to quit")
        
        # Runs the create account function until user presses ctrl-c
        while True:
            create_account()

    except KeyboardInterrupt:
        quit()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

input("Press enter to exit")