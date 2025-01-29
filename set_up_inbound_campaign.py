from config import *
from authentication_info import *
from deepgram import *
from ncc_pstn_number import *
from ncc_disposition import *
from ncc_user_profile import *
from ncc_user_profile_disposition import *
from ncc_queue import *
from ncc_survey_theme import *
from ncc_survey import *
from ncc_workflow import *
from ncc_service import *
from ncc_campaign import *
from ncc_campaign_disposition import *


def set_up_inbound_campaign(ncc_location: str, ncc_token: str):
    """
    This function performs the basic setup of a new Nextiva Contact Center (NCC) tenant.
    """

    # Enter campaign name
    campaign_name = ""
    while campaign_name == "":
        print()
        campaign_name = input("Campaign name: ")
        if campaign_name == "":
            print()
            print("Invalid campaign name.")

    # Enter business name
    business_name = ""
    while business_name == "":
        print()
        business_name = input("Business name: ")
        if business_name == "":
            print()
            print("Invalid business name.")

    # Select vertical
    print()
    choice = ""
    while choice == "":
        print("Please select a vertical.")
        print("-------------------------")
        print("1. General")
        print("2. Healthcare")
        print("3. FinServ")
        print()
        choice = input("Command: ")
        print()
        if choice == "1":
            dispositions = general_dispositions
            queues = general_queues
        elif choice == "2":
            dispositions = general_dispositions + hc_dispositions
            queues = general_queues + hc_queues
        elif choice == "3":
            dispositions = general_dispositions + finserv_dispositions
            queues = general_queues + finserv_queues
        else:
            choice = ""
            print("Invalid choice.")
            print()

    # Select PSTN number
    campaign_address = ""
    print("Searching for available PSTN numbers...")
    print()
    pstn_numbers = get_pstn_numbers(ncc_location, ncc_token)
    if len(pstn_numbers) > 0:
        campaign_addresses_available = []
        for index, pstn_number in enumerate(pstn_numbers):
            success = search_campaigns_by_address(
                ncc_location, ncc_token, pstn_number["name"]
            )
            if success:
                pass
            else:
                campaign_addresses_available.append(pstn_number)
    if len(campaign_addresses_available) > 0:
        while campaign_address == "":
            print("Please select a PSTN number:")
            print("----------------------------")
            for index, campaign_address_available in enumerate(
                campaign_addresses_available
            ):
                print(f"{index + 1}. {campaign_address_available["name"]}")
            print()
            choice = input("Command: ")
            choice = int(choice) - 1
            try:
                campaign_address = campaign_addresses_available[choice]["name"]
                print()
            except:
                print()
                print("Invalid choice.")
                print()
    else:
        print("No phone numbers available.")

    # Create dispositions
    dispositions_to_assign = []
    for disposition in dispositions:
        print(f'Searching for "{disposition}" disposition...', end="")
        result = search_dispositions(ncc_location, ncc_token, disposition)
        if result == {}:
            print("not found.")
            print(f'Creating "{disposition}" disposition...', end="")
            disposition = create_disposition(ncc_location, ncc_token, disposition)
            if disposition != {}:
                print("success!")
                dispositions_to_assign.append(disposition)
            else:
                print("failed.")
        else:
            print("found.")
            dispositions_to_assign.append(result)

    # Assign user profiles to dispositions
    for user_profile in user_profiles:
        print(f'Searching for "{user_profile}" user profile...', end="")
        result = search_user_profiles(ncc_location, ncc_token, user_profile)
        if result != {}:
            print("found.")
            for disposition in dispositions_to_assign:
                print(
                    f'Checking if "{disposition["name"]}" disposition is assigned to "{user_profile}" user profile...',
                    end="",
                )
                success = search_user_profile_dispositions(
                    ncc_location, ncc_token, disposition["_id"], result["_id"]
                )
                if success:
                    print("assigned.")
                else:
                    print("not assigned.")
                    print(
                        f'Assigning "{disposition["name"]}" disposition to "{user_profile}" user profile...',
                        end="",
                    )
                    user_profile_disposition = create_user_profile_disposition(
                        ncc_location, ncc_token, result["_id"], disposition["_id"]
                    )
                    if user_profile_disposition != {}:
                        print("success!")
                    else:
                        print("failed.")
        else:
            print(f'"{user_profile}" user profile not found.')

    # Create queues
    for queue in queues:
        print(f'Searching for "{queue}" queue...', end="")
        result = search_queues(ncc_location, ncc_token, queue)
        if result == {}:
            print("none found.")
            print(f'Creating "{queue}" queue...', end="")
            result = create_queue(ncc_location, ncc_token, queue)
            if result != {}:
                print("success!")
            else:
                print("failed.")
        else:
            print("found.")

    # Create survey theme
    print(f'Searching for "Test {business_name}" survey theme...', end="")
    survey_theme = search_survey_themes(
        ncc_location, ncc_token, f"Test {business_name}"
    )
    if survey_theme == {}:
        print("not found.")
        print(f'Creating "Test {business_name}" survey theme...', end="")
        survey_theme = create_survey_theme(
            ncc_location, ncc_token, f"Test {business_name}"
        )
        if survey_theme != {}:
            print("success!")
        else:
            print("failed.")
    else:
        print("found.")

    # Create user survey
    print(f'Searching for "{campaign_name} - User" survey...', end="")
    user_survey = search_surveys(ncc_location, ncc_token, f"{campaign_name} - User")
    if user_survey == {}:
        print("not found.")
        print(f'Creating "{campaign_name} - User" survey...', end="")
        user_survey = create_survey(
            ncc_location,
            ncc_token,
            f"{campaign_name} - User",
            main_user_survey_body,
            survey_theme,
        )
        if user_survey != {}:
            print("success!")
        else:
            print("failed.")
    else:
        print("found.")

    # Create chat survey
    print(f'Searching for "{campaign_name} - Chat" survey...', end="")
    chat_survey = search_surveys(ncc_location, ncc_token, f"{campaign_name} - Chat")
    if chat_survey == {}:
        print("not found.")
        print(f'Creating "{campaign_name} - Chat" survey...', end="")
        chat_survey = create_survey(
            ncc_location,
            ncc_token,
            f"{campaign_name} - Chat",
            main_chat_survey_body,
            survey_theme,
        )
        if chat_survey != {}:
            print("success!")
        else:
            print("failed.")
    else:
        print("found.")

    # Create QM survey
    print(f'Searching for "{campaign_name} - QM" survey...', end="")
    qm_survey = search_surveys(ncc_location, ncc_token, f"{campaign_name} - QM")
    if qm_survey == {}:
        print("not found.")
        print(f'Creating "{campaign_name} - QM" survey...', end="")
        qm_survey = create_survey(
            ncc_location,
            ncc_token,
            f"{campaign_name} - QM",
            main_qm_survey_body,
            survey_theme,
        )
        if qm_survey != {}:
            print("success!")
        else:
            print("failed.")
    else:
        print("found.")

    # Create workflow
    print(f'Searching for "{campaign_name}" workflow...', end="")
    workflow = search_workflows(ncc_location, ncc_token, campaign_name)
    if workflow == {}:
        print("not found.")
        print(f'Creating "{campaign_name}" workflow...', end="")
        workflow = create_workflow(
            ncc_location, ncc_token, main_workflow, campaign_name
        )
        if workflow != {}:
            print("success!")
        else:
            print("failed.")
    else:
        workflow = workflow["_id"]
        print("found.")

    # Search for REALTIME_ANALYSIS service
    print('Searching for "REALTIME_ANALYSIS" service...', end="")
    service = search_services(ncc_location, ncc_token, "REALTIME_ANALYSIS")
    if service != {}:
        print("found.")
    else:
        print("not found.")

    # Create Deepgram API key
    if service == {}:
        print('Searching for "Test Key" Deepgram API key...', end="")
        deepgram_api_key_id = search_deepgram_api_keys(
            deepgram_project_id, deepgram_main_api_key, "Test Key"
        )
        if deepgram_api_key_id == "":
            print("none found.")
            print("Creating new Deepgram API key...", end="")
            deepgram_api_key = create_deepgram_api_key(
                deepgram_project_id, deepgram_main_api_key
            )
            if deepgram_api_key != "":
                print("success!")
            else:
                print("failed.")
        else:
            print("found.")

    # Create real-time transcription service
    if service == {} and deepgram_api_key != "":
        print(
            'Creating "Test Deepgram Real-Time Transcription" service...',
            end="",
        )
        service = create_real_time_transcription_service(
            ncc_location,
            ncc_token,
            "Test Deepgram Real-Time Transcription",
            deepgram_api_key,
        )
        if service != {}:
            print("success!")
        else:
            print("failed.")

    # Create campaign
    print(f'Searching for "{campaign_name}" campaign...', end="")
    campaign = search_campaigns_by_name(ncc_location, ncc_token, campaign_name)
    if campaign == {}:
        print("none found.")
        print(f'Creating "{campaign_name}" campaign...', end="")
        campaign = create_campaign(
            ncc_location,
            ncc_token,
            campaign_name,
            user_survey["_id"],
            chat_survey["_id"],
            qm_survey["_id"],
            campaign_address,
            workflow["_id"],
            service["_id"],
        )
        if campaign != {}:
            print("success!")
        else:
            print("failed.")
    else:
        print("found.")

    # Update chat survey campaign ID
    if campaign != {} and chat_survey != {}:
        print(
            f'Updating "{chat_survey["name"]}" survey with "{campaign_name}" campaign...',
            end="",
        )
        success = update_chat_survey_campaign_id(
            ncc_location, ncc_token, chat_survey["_id"], campaign["_id"]
        )
        if success:
            print("success!")
        else:
            print("failed.")

    # Assign dispositions to campaign
    if campaign != {}:
        for disposition in dispositions_to_assign:
            print(
                f'Checking if "{disposition["name"]}" disposition is assigned to "{campaign_name}" campaign...',
                end="",
            )
            success = search_campaign_dispositions(
                ncc_location, ncc_token, campaign["_id"], disposition["_id"]
            )
            if not success:
                print("not found.")
                print(
                    f'Assigning "{disposition["name"]}" disposition to "{campaign_name}" campaign...',
                    end="",
                )
                success = create_campaign_disposition(
                    ncc_location, ncc_token, campaign["_id"], disposition["_id"]
                )
                if success:
                    print("success!")
                else:
                    print("failed.")
            else:
                print("assigned.")
