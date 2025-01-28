import getpass
from authentication import *
from set_up_inbound_campaign import *
from set_up_feature import *
from set_up_integration import *
from tear_down_tenant import *


def display_main_menu():
    print()
    print("Main Menu")
    print("---------")
    print("1. Set up inbound campaign")
    print("2. Set up outbound campaign")
    print("3. Set up feature")
    print("4. Set up integration")
    print("5. Set up agent")
    print("6. Set up supervisor")
    print("7. Tear down tenant")
    print("8. Exit")
    print()


def main():
    authenticated = False
    print("*****************************************************")
    print("This system is the property of Nextiva, Inc.")
    print("It is for authorized use only. By using this system,")
    print("all users acknowledge notice of, and agree to comply")
    print("with, Nextiva, Inc.'s Acceptable Use Policy (“AUP”).")
    print()
    print("See www.nextiva.com for details.")
    print("*****************************************************")
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
            while choice != "8":
                display_main_menu()
                choice = input("Command: ")
                if choice == "1":
                    set_up_inbound_campaign(ncc_location, ncc_token)
                elif choice == "2":
                    pass
                elif choice == "3":
                    set_up_feature(ncc_location, ncc_token)
                elif choice == "4":
                    set_up_integration(ncc_location, ncc_token)
                elif choice == "5":
                    pass
                elif choice == "6":
                    pass
                elif choice == "7":
                    tear_down_tenant(ncc_location, ncc_token)
                elif choice == "8":
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
