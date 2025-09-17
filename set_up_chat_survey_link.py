import logging
from authentication_info import *
from datadog import *
from ncc_campaign import *


def set_up_chat_survey_link(
    host: str, ncc_location: str, ncc_token: str, username: str
):
    """
    This function creates a URL link to a website that hosts a Nextiva Contact Center (NCC) chat survey.
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
                "Chat Survey Link Setup Cancelled",
                f'User "{username}" cancelled chat survey link setup for "{campaign_name}" campaign.',
                ["chatsurveylinksetup"],
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

        # Select vertical
        print()
        choice = ""
        while choice == "":
            print("Please select a vertical.")
            print("-------------------------")
            print("1. General")
            print("2. Healthcare")
            print("3. FinServ")
            print("4. Insurance")
            print("5. Retail")
            print("6. PubSec")
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
                    "Chat Survey Link Setup Cancelled",
                    f'User "{username}" cancelled chat survey link setup for "{campaign_name}" campaign.',
                    ["chatsurveylinksetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice in ["1", "2", "3", "4", "5", "6"]:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "success",
                        "normal",
                        "Chat Survey Link Setup Successful",
                        f'User "{username}" set up chat survey link for "{campaign_name}" campaign.',
                        ["chatsurveylinksetup"],
                    )
                    print(
                        f'Link: https://enterprise-demos.com/{choice}?host={host}&tenantId={campaign["tenantId"]}&campaignId={campaign["_id"]}'
                    )
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()
