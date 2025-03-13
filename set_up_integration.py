import logging
from authentication_info import *
from datadog import *
from ncc_campaign import *
from set_up_freshdesk_integration import *


def set_up_integration(ncc_location: str, ncc_token: str, username: str):
    """
    This function performs the setup of an integration in Nextiva Contact Center (NCC).
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    cancelled = False

    print()
    print('Enter "cancel" at any prompt to cancel.')

    # Enter campaign name
    campaign_name = ""
    while campaign_name == "":
        print()
        campaign_name = input("Campaign name: ")
        if campaign_name.lower() == "cancel":
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Integration Setup Cancelled",
                f'User "{username}" cancelled integration setup.',
                ["integrationsetup"],
            )
            print()
            print("Operation cancelled.")
            cancelled = True
        elif campaign_name == "":
            print()
            print("Invalid campaign name.")
        else:
            campaign = search_campaigns_by_name(ncc_location, ncc_token, campaign_name)
            if campaign == {}:
                print()
                print(f'Campaign "{campaign_name}" not found. Please try again.')
                campaign_name = ""

    if cancelled == False:

        # Select system
        print()
        choice = ""
        while choice == "":
            print("Please select a system.")
            print("----------------------")
            print("1. Freshdesk")
            print()
            choice = input("Command: ")
            if choice.lower() == "cancel":
                print()
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Integration Setup Cancelled",
                    f'User "{username}" cancelled integration setup for "{campaign_name}" campaign.',
                    ["integrationsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    set_up_freshdesk_integration(
                        ncc_location, ncc_token, username, campaign_name, campaign
                    )
                else:
                    print()
                    choice = ""
                    print("Invalid choice.")
                    print()
