from config import *
from deepgram import *
from ncc_disposition import *
from ncc_user_profile import *
from ncc_user_profile_disposition import *
from ncc_queue import *
from ncc_workflow import *
from ncc_function import *
from ncc_service import *
from ncc_campaign import *
from ncc_survey import *
from ncc_rest_call import *
from dialogflow import *


def tear_down_tenant(ncc_location: str, ncc_token: str) -> str:
    """
    This function deletes many of the entities created for the given NCC tenant.
    """
    print()

    # Delete campaign
    print('Searching for "Test Campaign" campaign...', end="")
    campaign = search_campaigns(ncc_location, ncc_token, "Test Campaign")
    if campaign != {}:
        print("found.")
        print('Deleting "Test Campaign" campaign...', end="")
        success = delete_campaign(ncc_location, ncc_token, campaign["_id"])
        if success:
            print("success!")
        else:
            print("failed.")
    else:
        print("not found.")

    # Delete real-time transcription service
    print('Searching for "Test Deepgram Real-Time Transcription" service...', end="")
    real_time_transcription_service_id = search_services(
        ncc_location,
        ncc_token,
        "Test Deepgram Real-Time Transcription",
        "REALTIME_ANALYSIS",
    )
    if real_time_transcription_service_id != "":
        print("found.")
        print('Deleting "Test Deepgram Real-Time Transcription" service...', end="")
        success = delete_service(
            ncc_location, ncc_token, real_time_transcription_service_id
        )
        if success:
            print("success!")
        else:
            print("failed.")
    else:
        print("not found.")

    # Delete Deepgram API key
    print('Searching for "Test Key" Deepgram API key...', end="")
    deepgram_api_key_id = search_deepgram_api_keys(
        deepgram_project_id, deepgram_main_api_key, "Test Key"
    )
    if deepgram_api_key_id != "":
        print("found.")
        print(f'Deleting "Test Key" Deepgram API key...', end="")
        success = delete_deepgram_api_key(
            deepgram_project_id, deepgram_main_api_key, deepgram_api_key_id
        )
        if success:
            print("success!")
        else:
            print("failed.")
    else:
        print("not found.")

    # Delete workflow
    print('Searching for "Test Workflow" workflow...', end="")
    workflow = search_workflows(ncc_location, ncc_token, "Test Workflow")
    if workflow != {}:
        workflow_id = workflow["_id"]
        print("found.")
        print('Deleting "Test Workflow" workflow...', end="")
        success = delete_workflow(ncc_location, ncc_token, workflow_id)
        if success:
            print("success!")
        else:
            print("failed.")
    else:
        print("not found.")

    # Delete functions
    print('Searching for functions with "Test " prefix...', end="")
    test_functions = get_functions(ncc_location, ncc_token)
    if len(test_functions) > 0:
        print(f"found {len(test_functions)} function(s).")
    else:
        print("none found.")
    for test_function in test_functions:
        test_function_name = test_function["name"]
        test_function_id = test_function["_id"]
        print(f'Deleting "{test_function_name}" function...', end="")
        success = delete_function(ncc_location, ncc_token, test_function_id)
        if success:
            print("success!")
        else:
            print("failed")

    # Delete queues
    print('Searching for queues with "Test " prefix...', end="")
    queues = get_queues(ncc_location, ncc_token)
    if len(queues) > 0:
        print(f"found {len(queues)} queue(s).")
    else:
        print("none found.")
    for queue in queues:
        print(f'Deleting "{queue["name"]}" queue...', end="")
        success = delete_queue(ncc_location, ncc_token, queue["_id"])
        if success:
            print("success!")
        else:
            print("failed")

    # Delete dispositions
    print('Searching for dispositions with "Test " prefix...', end="")
    dispositions = get_dispositions(ncc_location, ncc_token)
    if len(dispositions) > 0:
        print(f"found {len(dispositions)} dispositions.")
    else:
        print("none found.")
    for disposition in dispositions:
        print(f'Deleting "{disposition["name"]}" disposition...', end="")
        success = delete_disposition(ncc_location, ncc_token, disposition["_id"])
        if success:
            print("success!")
        else:
            print("failed")

    # Delete surveys
    print('Searching for surveys with "Test " prefix...', end="")
    surveys = get_surveys(ncc_location, ncc_token)
    if len(surveys) > 0:
        print(f"found {len(surveys)} survey(s).")
    else:
        print("none found.")
    for survey in surveys:
        print(f'Deleting "{survey["name"]}" survey...', end="")
        success = delete_survey(ncc_location, ncc_token, survey["_id"])
        if success:
            print("success!")
        else:
            print("failed.")

    # Delete REST API objects
    print('Searching for REST API call objects with "Test " prefix...', end="")
    rest_calls = get_rest_calls(ncc_location, ncc_token)
    if len(rest_calls) > 0:
        print(f"found {len(rest_calls)} REST API call object(s).")
    else:
        print("none found.")
    for rest_call in rest_calls:
        print(f'Deleting "{rest_call["name"]}" REST API call object...', end="")
        success = delete_rest_call(ncc_location, ncc_token, rest_call["_id"])
        if success:
            print("success!")
        else:
            print("failed.")

    # Delete Dialogflow intents
    print('Searching for Dialogflow intents with "Test_" prefix...', end="")
    intent_list = get_intents()
    if len(intent_list) > 0:
        print(f"found {len(intent_list)} intent(s).")
        for intent in intent_list:
            print(f'Deleting "{intent.display_name}" intent...', end="")
            success = delete_intent(intent.name)
            if success:
                print("success!")
            else:
                print("failed.")
    else:
        print("no intents found.")
