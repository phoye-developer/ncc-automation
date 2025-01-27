import getpass
from authentication import *
from set_up_campaign import *
from set_up_feature import *
from set_up_integration import *
from tear_down_tenant import *


def display_main_menu():
    print()
    print("Main Menu")
    print("---------")
    print("1. Set up campaign")
    print("2. Set up feature")
    print("3. Set up integration")
    print("4. Tear down tenant")
    print("5. Exit")
    print()


def main():
    authenticated = False
    print(
        "This computer system is the property of Nextiva, Inc. It is for authorized use only. By using this system, all users acknowledge notice of, and agree to comply with, Nextiva, Inc.'s Acceptable Use Policy (“AUP”). See www.nextiva.com for details."
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
            while choice != "5":
                display_main_menu()
                choice = input("Command: ")
                if choice == "1":
                    set_up_campaign(ncc_location, ncc_token)
                elif choice == "2":
                    set_up_feature(ncc_location, ncc_token)
                elif choice == "3":
                    set_up_integration(ncc_location, ncc_token)
                elif choice == "4":
                    tear_down_tenant(ncc_location, ncc_token)
                elif choice == "5":
                    pass
                else:
                    print()
                    print("Invalid choice.")
        else:
            print()
            print("Authentication failed. Please try again.")
            print()
    print()


if __name__ == "__main__":
    main()
