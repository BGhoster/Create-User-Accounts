import ctypes, sys
import subprocess
from getpass import getpass

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_account():
    # define constants
    username = ""
    password = ""
    command = f"net user {username} {password} /add"

    while not username:
        username = input("Enter username: ")
    # wait for the user to enter a non-empty password
    while not password:
        password = getpass("Enter password for account: ")
    # run the command to create the user
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
    create_account()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)