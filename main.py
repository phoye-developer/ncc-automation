import getpass
from authentication import *
from set_up_tenant import *
from tear_down_tenant import *


def display_main_menu():
    print()
    print("1. Set up tenant")
    print("2. Tear down tenant")
    print("3. Exit")
    print()


def main():
    authenticated = False
    print(
        "This computer system is the property of Nextiva, Inc. It is for authorized use only. By using this system, all users acknowledge notice of, and agree to comply with, Nextiva, Inc.'s Acceptable Use Policy (“AUP”). See https://www.nextiva.com/legal.html?doc=09 for details."
    )
    print()
    print("Please log in.")
    print()
    while not authenticated:
        username = input("Username: ")
        password = getpass.getpass(prompt="Password: ", stream=None)
        auth_info = get_ncc_token(username, password)
        if auth_info:
            authenticated = True
            ncc_location = auth_info["location"].replace("https://", "")
            ncc_token = auth_info["token"]
            choice = ""
            while choice != "3":
                display_main_menu()
                choice = input("Command: ")
                if choice == "1":
                    set_up_tenant(ncc_location, ncc_token)
                elif choice == "2":
                    tear_down_tenant(ncc_location, ncc_token)
                elif choice == "3":
                    pass
                else:
                    print("You did not make a valid choice.")
        else:
            print()
            print("Authentication failed. Please try again.")
            print()
    print()


if __name__ == "__main__":
    main()
