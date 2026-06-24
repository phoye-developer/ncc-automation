import getpass
from authentication import *
from set_up_inbound_campaign import *
from set_up_agent import *
from set_up_supervisor import *
from set_up_feature import *
from set_up_integration import *
from set_up_chat_survey_link import *
from tear_down_campaign import *


def display_main_menu():
    print()
    print("Main Menu")
    print("---------")
    print("1. Set up inbound campaign")
    print("2. Set up agent")
    print("3. Set up supervisor")
    print("4. Set up feature")
    print("5. Set up integration")
    print("6. Set up chat survey link")
    print("7. Tear down campaign")
    print("8. Logout")
    print("9. Exit")
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
    print("NCC Automation v2.2.3")
    print()
    print("Please log in. Your password will not display on the screen.")
    print()
    while not authenticated:
        default_login_site = "login.thrio.io"
        login_site = input(f"Login site (default: {default_login_site}): ")
        if not login_site:
            login_site = default_login_site
        username = input("Username: ")
        password = getpass.getpass(prompt="Password: ", stream=None)
        auth_info = get_ncc_token(login_site, username, password)
        if auth_info:
            authenticated = True
            ncc_location = auth_info["location"].replace("https://", "")
            ncc_token = auth_info["token"]
            choice = ""
            while choice != "9":
                display_main_menu()
                choice = input("Command: ")
                if choice == "1":
                    set_up_inbound_campaign(ncc_location, ncc_token, username)
                elif choice == "2":
                    set_up_agent(ncc_location, ncc_token, username)
                elif choice == "3":
                    set_up_supervisor(ncc_location, ncc_token, username)
                elif choice == "4":
                    set_up_feature(ncc_location, ncc_token, username)
                elif choice == "5":
                    set_up_integration(ncc_location, ncc_token, username)
                elif choice == "6":
                    set_up_chat_survey_link(
                        login_site, ncc_location, ncc_token, username
                    )
                elif choice == "7":
                    tear_down_campaign(ncc_location, ncc_token, username)
                elif choice == "8":
                    auth_info = ""
                    authenticated = False
                    print()
                    break
                elif choice == "9":
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
