import logging
from authentication_info import *
from datadog import *
from ncc_campaign import *
from set_up_csat_survey import *


def set_up_feature(ncc_location: str, ncc_token: str, username: str):
    """
    This function performs the setup of a specific feature in Nextiva Contact Center (NCC).
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
                "Feature Setup Cancelled",
                f'User "{username}" cancelled feature setup.',
                ["featuresetup"],
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

        # Enter business name
        business_name = ""
        while business_name == "":
            print()
            business_name = input("Business name: ")
            if business_name.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Feature Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" feature setup.',
                    ["featuresetup"],
                )
                print()
                print("Operation cancelled.")
                cancelled = True
            elif business_name == "":
                print()
                print("Invalid business name.")

    if cancelled == False:

        # Select feature
        print()
        choice = ""
        while choice == "":
            print("Please select a feature.")
            print("------------------------")
            print("1. CSAT Survey via SMS Text")
            print("2. SMS Text on Abandoned Call")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Feature Setup Cancelled",
                    f'User "{username}" cancelled feature setup for "{campaign_name}" campaign.',
                    ["featuresetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    set_up_csat_survey(
                        ncc_location,
                        ncc_token,
                        username,
                        campaign_name,
                        business_name,
                    )
                elif choice == "2":
                    pass
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()
