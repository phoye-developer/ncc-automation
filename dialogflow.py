from google.cloud import dialogflow_v2
from config import *
from authentication_info import *


def search_intents(intent_name: str) -> bool:
    """
    This function searches for an intent with the specified display name.
    """
    success = False
    client = dialogflow_v2.IntentsClient()
    client.from_service_account_info(google_service_account_info)

    request = dialogflow_v2.ListIntentsRequest(parent=google_dialogflow_parent)

    page_result = client.list_intents(request=request)

    for response in page_result:
        if response.display_name == intent_name:
            success = True
            break

    return success


def get_intents() -> list:
    """
    This function fetches a list of intents for the Dialogflow agent and returns a list of those with the "Test_" prefix.
    """
    intent_list = []
    client = dialogflow_v2.IntentsClient()
    client.from_service_account_info(google_service_account_info)

    request = dialogflow_v2.ListIntentsRequest(parent=google_dialogflow_parent)

    page_result = client.list_intents(request=request)

    for response in page_result:
        if response.display_name[0:5] == "Test_":
            intent_list.append(response)

    return intent_list


def create_intent(
    intent_name: str,
    intent_training_phrases: list,
    intent_action: str,
    intent_messages: dict,
    intent_webhook_state: str,
    intent_end_interaction: bool,
) -> bool:
    """
    This function creates a new intent for the Dialogflow agent.
    """
    success = False
    client = dialogflow_v2.IntentsClient()
    client.from_service_account_info(google_service_account_info)

    intent = dialogflow_v2.Intent()
    intent.display_name = intent_name
    intent.training_phrases = intent_training_phrases
    intent.action = intent_action
    intent.messages = intent_messages
    intent.webhook_state = intent_webhook_state
    intent.end_interaction = intent_end_interaction

    request = dialogflow_v2.CreateIntentRequest(
        parent=google_dialogflow_parent, intent=intent
    )

    response = client.create_intent(request=request)
    try:
        response.name
        success = True
    except:
        success = False
    return success


def delete_intent(intent_name: str) -> bool:
    """
    This function deletes a Dialogflow agent's intent.
    """
    success = False
    client = dialogflow_v2.IntentsClient()
    client.from_service_account_info(google_service_account_info)

    request = dialogflow_v2.DeleteIntentRequest(name=intent_name)

    try:
        client.delete_intent(request=request)
        success = True
    except:
        success = False
    return success
