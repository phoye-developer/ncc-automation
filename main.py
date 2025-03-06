import getpass
from authentication import *
from datadog import *
from set_up_inbound_campaign import *
from set_up_agent import *
from set_up_supervisor import *
from set_up_feature import *
from tear_down_campaign import *


def display_main_menu():
    print()
    print("Main Menu")
    print("---------")
    print("1. Set up inbound campaign")
    print("2. Set up agent")
    print("3. Set up supervisor")
    print("4. Set up feature")
    print("5. Tear down campaign")
    print("6. Logout")
    print("7. Exit")
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
    print("NCC Automation v1.1.0")
    print()
    print("Please log in. Your password will not display on the screen.")
    print()
    while not authenticated:
        username = input("Username: ")
        password = getpass.getpass(prompt="Password: ", stream=None)
        auth_info = get_ncc_token(username, password)
        if auth_info:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "success",
                "normal",
                "Login Successful",
                f'User "{username}" logged in.',
                ["login"],
            )
            authenticated = True
            ncc_location = auth_info["location"].replace("https://", "")
            ncc_token = auth_info["token"]
            choice = ""
            while choice != "7":
                display_main_menu()
                choice = input("Command: ")
                if choice == "1":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "info",
                        "normal",
                        "Inbound Campaign Setup Started",
                        f'User "{username}" started inbound campaign setup.',
                        ["inboundcampaignsetup"],
                    )
                    set_up_inbound_campaign(ncc_location, ncc_token, username)
                elif choice == "2":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "info",
                        "normal",
                        "Agent Setup Started",
                        f'User "{username}" started agent setup.',
                        ["agentsetup"],
                    )
                    set_up_agent(ncc_location, ncc_token, username)
                elif choice == "3":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "info",
                        "normal",
                        "Supervisor Setup Started",
                        f'User "{username}" started supervisor setup.',
                        ["supervisorsetup"],
                    )
                    set_up_supervisor(ncc_location, ncc_token, username)
                elif choice == "4":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "info",
                        "normal",
                        "Feature Setup Started",
                        f'User "{username}" started feature setup.',
                        ["featuresetup"],
                    )
                    set_up_feature(ncc_location, ncc_token, username)
                elif choice == "5":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "info",
                        "normal",
                        "Campaign Teardown Started",
                        f'User "{username}" started campaign teardown.',
                        ["campaignteardown"],
                    )
                    tear_down_campaign(ncc_location, ncc_token, username)
                elif choice == "6":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "info",
                        "normal",
                        "Logout",
                        f'User "{username}" logged out.',
                        ["logout"],
                    )
                    auth_info = ""
                    authenticated = False
                    print()
                    break
                elif choice == "7":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "info",
                        "normal",
                        "Exit Application",
                        f'User "{username}" exited the application.',
                        ["exitapplication"],
                    )
                    pass
                else:
                    print()
                    print("Invalid choice.")
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Login Failed",
                f'User "{username}" tried unsuccessfully to log in.',
                ["login"],
            )
            print()
            print("Authentication failed. Please try again.")
            print()
    print()


if __name__ == "__main__":
    main()
