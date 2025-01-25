from config import *
from deepgram import *
from ncc_disposition import *
from ncc_user_profile import *
from ncc_user_profile_disposition import *
from ncc_queue import *
from ncc_survey import *
from ncc_workflow import *
from ncc_service import *
from ncc_campaign import *
from ncc_campaign_disposition import *
from dialogflow import *


def set_up_tenant(ncc_location: str, ncc_token: str):
    """
    This function performs the basic setup of a new Nextiva Contact Center (NCC) tenant.
    """

    # Select vertical
    print()
    print("Please select a vertical.")
    choice = ""
    while choice == "":
        print()
        print("1. General")
        print("2. Healthcare")
        print("3. FinServ")
        print()
        choice = input("Command: ")
        print()
        if choice == "1":
            dispositions = general_dispositions
            queues = general_queues
            intents = general_intents
        elif choice == "2":
            dispositions = general_dispositions + hc_dispositions
            queues = general_queues + hc_queues
            intents = general_intents + hc_intents
        elif choice == "3":
            dispositions = general_dispositions + finserv_dispositions
            queues = general_queues + finserv_queues
            intents = general_intents + finserv_intents
        else:
            choice = ""
            print("Invalid choice. Please try again.")

    # Create dispositions
    for disposition in dispositions:
        print(f'Searching for "{disposition}" disposition...', end="")
        result = search_dispositions(ncc_location, ncc_token, disposition)
        if result == {}:
            print("none found.")
            print(f'Creating "{disposition}" disposition...', end="")
            disposition = create_disposition(ncc_location, ncc_token, disposition)
            if disposition != {}:
                print("success!")
            else:
                print("failed.")
        else:
            print("found.")

    # Assign user profiles to dispositions
    for user_profile in user_profiles:
        print(f'Searching for "{user_profile}" user profile...', end="")
        result = search_user_profiles(ncc_location, ncc_token, user_profile)
        if result != {}:
            print("found.")
            dispositions = get_dispositions(ncc_location, ncc_token)
            for disposition in dispositions:
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

    # Create survey
    print('Searching for "Test Main - User" survey...', end="")
    survey = search_surveys(ncc_location, ncc_token, "Test Main - User")
    if survey == {}:
        print("not found.")
        print('Creating "Test Main - User" survey...', end="")
        survey = create_survey(
            ncc_location, ncc_token, "Test Main - User", main_user_survey_body
        )
        if survey != {}:
            print("success!")
        else:
            print("failed.")
    else:
        print("found.")

    # Create workflow
    print('Searching for "Test Workflow" workflow...', end="")
    workflow = search_workflows(ncc_location, ncc_token, "Test Workflow")
    if workflow == {}:
        print("not found.")
        print('Creating "Test Workflow" workflow...', end="")
        workflow = create_workflow(
            ncc_location, ncc_token, main_workflow, "Test Workflow"
        )
        if workflow != {}:
            print("success!")
        else:
            print("failed.")
    else:
        workflow = workflow["_id"]
        print("found.")

    # Create Deepgram API key
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
    print(
        'Searching for "Test Deepgram Real-Time Transcription" service...',
        end="",
    )
    service = search_services(
        ncc_location,
        ncc_token,
        "Test Deepgram Real-Time Transcription",
        "REALTIME_ANALYSIS",
    )
    if service == {}:
        print("none found.")
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
    else:
        print("found.")

    # Create campaign
    print('Searching for "Test Campaign" campaign...', end="")
    campaign = search_campaigns(ncc_location, ncc_token, "Test Campaign")
    if campaign == {}:
        print("none found.")
        print('Creating "Test Campaign" campaign...', end="")
        campaign = create_campaign(
            ncc_location,
            ncc_token,
            "Test Campaign",
            survey["_id"],
            workflow["_id"],
            service["_id"],
        )
        if campaign != {}:
            print("success!")
        else:
            print("failed.")
    else:
        print("found.")

    # Assign dispositions to campaign
    if campaign != {}:
        dispositions = get_dispositions(ncc_location, ncc_token)
        for disposition in dispositions:
            print(
                f'Checking if "{disposition["name"]}" disposition is assigned to "Test Campaign" campaign...',
                end="",
            )
            success = search_campaign_dispositions(
                ncc_location, ncc_token, campaign["_id"], disposition["_id"]
            )
            if not success:
                print("not found.")
                print(
                    f'Assigning "{disposition["name"]}" disposition to "Test Campaign" campaign...',
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

    # Create Dialogflow intent
    for intent in intents:
        print(f'Searching for "{intent["intent"]}" intent...', end="")
        success = search_intents(intent["intent"])
        if success:
            print("found.")
        else:
            print("not found.")
            print(f'Creating "{intent["intent"]}" intent...', end="")
            success = create_intent(
                intent["intent"],
                intent["training_phrases"],
                intent["action"],
                intent["messages"],
                intent["webhook_state"],
                intent["end_interaction"],
            )
            if success:
                print("success!")
            else:
                print("failed.")
