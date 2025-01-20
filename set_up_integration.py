import getpass
from config import *
from ncc_rest_call import *
from ncc_survey import *
from ncc_workflow import *
from ncc_disposition import *
from ncc_campaign import *


def set_up_integration(ncc_location: str, ncc_token: str):
    """
    This function sets up an integration with a supported third-party system.
    """

    # Select system
    print()
    print("Please select a system with which to integrate.")
    choice = ""
    while choice == "":
        print()
        print("1. HubSpot")
        print("2. Zendesk")
        print()
        choice = input("Command: ")
        print()
        if choice == "1":
            hubspot_access_token = input("Access token: ")
            print()
            search_contacts_name = "Test HubSpot - Search Contacts"
            log_workitem_name = "Test HubSpot - Create Activity"
            system_name = "Test HubSpot"
            survey_body = hubspot_survey_body
        elif choice == "2":
            zendesk_username = input("Zendesk username: ")
            zendesk_password = getpass.getpass(prompt="Zendesk password: ", stream=None)
            print()
            search_contacts_name = "Test Zendesk - Search Contacts"
            log_workitem_name = "Test Zendesk - Create Ticket"
            system_name = "Test Zendesk"
            survey_body = zendesk_survey_body
        else:
            choice = ""
            print("Invalid choice. Please try again.")

    # Create "search contacts" REST API call object
    print(f'Searching for "{search_contacts_name}" REST API object...', end="")
    if system_name == "Test HubSpot":
        search_contacts_rest_call = search_rest_calls(
            ncc_location, ncc_token, search_contacts_name
        )
        if search_contacts_rest_call == {}:
            print("not found.")
            print(f'Creating "{search_contacts_name}" REST API object...', end="")
            search_contacts_rest_call = hubspot_create_search_contacts_rest_call(
                ncc_location, ncc_token, hubspot_access_token, search_contacts_name
            )
            if search_contacts_rest_call != {}:
                print("success!")
            else:
                print("failed.")
        else:
            print("found.")
    elif system_name == "Test Zendesk":
        search_contacts_rest_call = search_rest_calls(
            ncc_location, ncc_token, search_contacts_name
        )
        if search_contacts_rest_call == {}:
            print("not found.")
            print(f'Creating "{search_contacts_name}" REST API object...', end="")
            search_contacts_rest_call = zendesk_create_search_contacts_rest_call(
                ncc_location,
                ncc_token,
                zendesk_username,
                zendesk_password,
                search_contacts_name,
            )
            if search_contacts_rest_call != {}:
                print("success!")
            else:
                print("failed.")
        else:
            print("found.")

    # Create "log activity" REST API call object
    print(f'Searching for "{log_workitem_name}" REST API object...', end="")
    if system_name == "Test HubSpot":
        log_workitem_rest_call = search_rest_calls(
            ncc_location, ncc_token, log_workitem_name
        )
        if log_workitem_rest_call == {}:
            print("not found.")
            print(f'Creating "{log_workitem_name}" REST API object...', end="")
            log_workitem_rest_call = hubspot_create_activity_rest_call(
                ncc_location, ncc_token, hubspot_access_token, log_workitem_name
            )
            if log_workitem_rest_call != {}:
                print("success!")
            else:
                print("failed.")
        else:
            print("found.")
    elif system_name == "Test Zendesk":
        log_workitem_rest_call = search_rest_calls(
            ncc_location, ncc_token, log_workitem_name
        )
        if log_workitem_rest_call == {}:
            print("not found.")
            print(f'Creating "{log_workitem_name}" REST API object...', end="")
            log_workitem_rest_call = zendesk_create_ticket_rest_call(
                ncc_location,
                ncc_token,
                zendesk_username,
                zendesk_password,
                log_workitem_name,
            )
            if log_workitem_rest_call != {}:
                print("success!")
            else:
                print("failed.")
        else:
            print("found.")

    # Assign "search contacts" REST API call object to "Test Workflow"
    print('Searching for "Test Workflow"...', end="")
    workflow = search_workflows(ncc_location, ncc_token, "Test Workflow")
    if workflow != {}:
        print("found.")
        print(
            f'Assigning "{search_contacts_name}" to "Test Workflow" workflow...', end=""
        )
        success = assign_rest_call_to_workflow(
            ncc_location,
            ncc_token,
            search_contacts_rest_call["_id"],
            workflow["_id"],
            search_contacts_name,
        )
        if success:
            print("success!")
        else:
            print("failed.")
    else:
        print("not found.")

    # Assign "log activity" REST API call object to all dispositions
    print('Searching for dispositions with "Test " prefix...', end="")
    dispositions = get_dispositions(ncc_location, ncc_token)
    if len(dispositions) > 0:
        print(f"found {len(dispositions)} disposition(s).")
        for disposition in dispositions:
            print(
                f'Assigning "{log_workitem_name}" REST API call object to "{disposition["name"]}" disposition...',
                end="",
            )
            success = assign_rest_call_to_dispositon(
                ncc_location,
                ncc_token,
                log_workitem_rest_call["_id"],
                disposition["_id"],
            )
            if success:
                print("success!")
            else:
                print("failed.")
    else:
        print("none found.")

    # Create survey
    print(f'Searching for "{system_name}" survey...', end="")
    survey_id = search_surveys(ncc_location, ncc_token, system_name)
    if survey_id == "":
        print("not found.")
        print(f'Creating "{system_name}" survey...', end="")
        survey_id = create_survey(ncc_location, ncc_token, system_name, survey_body)
        if survey_id != "":
            print("success!")
        else:
            print("failed.")
    else:
        print("found.")

    # Assign survey to campaign
    if survey_id != "":
        print('Searching for "Test Campaign" campaign...', end="")
        campaign_id = search_campaigns(ncc_location, ncc_token, "Test Campaign")
        if campaign_id != "":
            print("found.")
            print(
                f'Assigning "{system_name}" survey to "Test Campaign" campaign...',
                end="",
            )
            success = assign_survey_to_campaign(
                ncc_location, ncc_token, survey_id, campaign_id
            )
            if success:
                print("success!")
            else:
                print("failed.")
        else:
            print("not found.")
