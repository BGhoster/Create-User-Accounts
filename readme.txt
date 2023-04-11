Windows User Management
This Python program allows Windows users with administrator privileges to create new accounts and grant admin rights to existing accounts.

How to Use
Run the program in your command prompt or terminal.
Select an option from the menu:
1 to create a new user account.
2 to grant admin rights to an existing account.
Follow the prompts to enter the required information.
To quit the program, press Ctrl-C.
Requirements
This program requires a Windows operating system.
The user running the program must have administrator privileges.
Functions
is_admin()
This function checks if the user running the program has admin privileges. It returns True if the user is an admin, False otherwise.

create_account()
This function prompts the user to enter a new username and password for the new account. It then uses the subprocess module to execute a command to create the new user account. If the command is successful, it prints a success message to the console.

create_admin()
This function prompts the user to enter the name of an existing account to which they want to grant admin rights. It then uses the subprocess module to execute a command to add the specified account to the administrators group. If the command is successful, it prints a success message to the console.

Disclaimer
This program is provided as-is, without warranty of any kind, express or implied. Use at your own risk. The author assumes no liability for any damages arising from the use of this program.