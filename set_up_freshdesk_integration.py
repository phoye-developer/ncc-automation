import logging
import datetime
from authentication_info import *
from config import *
from ncc_rest_call import *
from ncc_function import *
from ncc_survey import *
from ncc_survey_theme import *
from ncc_service import *
from ncc_workflow import *
from ncc_campaign import *
from ncc_script import *
from ncc_disposition import *


def set_up_freshdesk_integration(
    ncc_location: str,
    ncc_token: str,
    username: str,
    campaign_name: str,
    campaign: dict,
):
    """
    This function sets up an integration with Freshdesk.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    cancelled = False

    # Enter subdomain
    freshdesk_subdomain = ""
    while freshdesk_subdomain == "":
        print()
        freshdesk_subdomain = input("Freshdesk Subdomain: ")
        if freshdesk_subdomain.lower() == "cancel":
            print()
            print("Operation cancelled.")
            cancelled = True
        elif freshdesk_subdomain == "":
            print()
            print("Invalid Freshdesk subdomain.")

    if cancelled == False:

        # Enter API key
        freshdesk_api_key = ""
        while freshdesk_api_key == "":
            print()
            freshdesk_api_key = input("Freshdesk API Key: ")
            if freshdesk_api_key.lower() == "cancel":
                print()
                print("Operation cancelled.")
                cancelled = True
            elif freshdesk_api_key == "":
                print()
                print("Invalid Freshdesk API key.")

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
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    categories = general_categories
                elif choice == "2":
                    categories = general_categories + hc_categories
                elif choice == "3":
                    categories = general_categories + finserv_categories
                elif choice == "4":
                    categories = general_categories + insurance_categories
                elif choice == "5":
                    categories = general_categories + retail_categories
                elif choice == "6":
                    categories = general_categories + pubsec_categories
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        # Select logging option
        add_logging = False
        choice = ""
        while choice == "":
            print("Add logging to all dispositions?")
            print("--------------------------------")
            print("1. Yes")
            print("2. No")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    add_logging = True
                elif choice == "2":
                    pass
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        start_time = datetime.datetime.now()

        logging.info("Starting...")

        # Create REST API object
        rest_call = search_rest_calls(
            ncc_location, ncc_token, f"{campaign_name} - Search Freshdesk Contacts"
        )
        if rest_call == {}:
            rest_call = freshdesk_create_search_contacts_rest_call(
                ncc_location,
                ncc_token,
                freshdesk_subdomain,
                freshdesk_api_key,
                f"{campaign_name} - Search Freshdesk Contacts",
            )
            if rest_call != {}:
                logging.info(
                    f'REST API object "{campaign_name} - Search Freshdesk Contacts" created.'
                )
            else:
                logging.error(
                    f'REST API object "{campaign_name} - Search Freshdesk Contacts" not created.'
                )
        else:
            logging.info(
                f'REST API object "{campaign_name} - Search Freshdesk Contacts" already exists'
            )

        # Create Search Freshdesk Contacts function
        function = search_functions(
            ncc_location, ncc_token, f"{campaign_name} - Search Freshdesk Contacts"
        )
        if function == {}:
            if rest_call != {}:
                function = freshdesk_create_search_contacts_function(
                    ncc_location,
                    ncc_token,
                    f"{campaign_name} - Search Freshdesk Contacts",
                    rest_call,
                )
                if function != {}:
                    tenant_id = function["tenantId"]
                    logging.info(
                        f'Function "{campaign_name} - Search Freshdesk Contacts" created.'
                    )
                else:
                    logging.error(
                        f'Function "{campaign_name} - Search Freshdesk Contacts" not created.'
                    )
            else:
                logging.warning(
                    f'Insufficient data to create Function "{campaign_name} - Search Freshdesk Contacts".'
                )
        else:
            tenant_id = function["tenantId"]
            logging.info(
                f'Function "{campaign_name} - Search Freshdesk Contacts" already exists.'
            )

        # Create Freshdesk user survey
        survey = search_surveys(
            ncc_location, ncc_token, f"{campaign_name} - User - Freshdesk"
        )
        if survey == {}:
            user_survey = search_surveys(
                ncc_location, ncc_token, f"{campaign_name} - User"
            )
            if user_survey != {}:
                if "surveythemeId" in user_survey:
                    survey_theme = get_survey_theme(
                        ncc_location, ncc_token, user_survey["surveythemeId"]
                    )
                    if survey_theme != {}:
                        survey = freshdesk_create_user_survey(
                            ncc_location,
                            ncc_token,
                            f"{campaign_name} - User - Freshdesk",
                            categories,
                            survey_theme,
                            freshdesk_subdomain,
                        )
                        if survey != {}:
                            logging.info(
                                f'Survey "{campaign_name} - User - Freshdesk" created.'
                            )
                        else:
                            logging.error(
                                f'Survey "{campaign_name} - User - Freshdesk" not created.'
                            )
                    else:
                        logging.warning(
                            f'Insufficient data to create Survey "{campaign_name} - User - Freshdesk". Survey theme not found.'
                        )
                else:
                    logging.warning(
                        f'Insufficient data to create survey "{campaign_name} - User - Freshdesk". No survey theme ID in survey "{campaign_name} - User".'
                    )
            else:
                logging.warning(
                    f'Insufficient data to create survey "{campaign_name} - User - Freshdesk". Existing survey "{campaign_name} - User" not found.'
                )
        else:
            logging.info(
                f'User survey "{campaign_name} - User - Freshdesk" already exists.'
            )

        # Create GenAI service
        service = search_services_by_name(
            ncc_location, ncc_token, "Generative AI - Plain Text"
        )
        if service == {}:
            if tenant_id != "":
                service = create_plain_text_gen_ai_service(
                    ncc_location,
                    ncc_token,
                    "Generative AI - Plain Text",
                    f"thrio-prod-{tenant_id}",
                )
                if service != {}:
                    logging.info('Service "Generative AI - Plain Text" created.')
                else:
                    logging.error('Service "Generative AI - Plain Text" not created.')
            else:
                logging.warning(
                    'Insufficient data to create service "Generative AI - Plain Text". Tenant ID not available.'
                )
        else:
            logging.info('Service "Generative AI - Plain Text" already exists.')

        # Update workflow
        workflow = search_workflows(ncc_location, ncc_token, campaign_name)
        if workflow != {}:
            if function != {}:
                found = False
                states = workflow["states"]
                for key, value in enumerate(states):
                    if workflow["states"][value]["name"] == "Search Contacts":
                        actions = workflow["states"][value]["actions"]
                        for action in actions:
                            if action["properties"]["description"] == "Search Contacts":
                                found = True
                                action["properties"]["functionId"] = function["_id"]
                                if "functionId" in action["properties"]["expansions"]:
                                    action["properties"]["expansions"]["functionId"][
                                        "name"
                                    ] = f"{campaign_name} - Search Freshdesk Contacts"
                                else:
                                    logging.warning(
                                        f'Expansion not updated for workflow "{campaign_name}".'
                                    )
                                success = update_workflow(
                                    ncc_location, ncc_token, workflow["_id"], workflow
                                )
                                if success:
                                    logging.info(f'Workflow "{campaign_name}" updated.')
                                else:
                                    logging.error(
                                        f'Workflow "{campaign_name}" not updated.'
                                    )
                                break
                if not found:
                    logging.warning(
                        f'Workflow "{campaign_name}" not updated due to malformed workflow.'
                    )
            else:
                logging.warning(
                    f'Insufficient data to update workflow "{campaign_name}". No function available for update.'
                )
        else:
            logging.warning(f'Workflow "{campaign_name}" not found.')

        # Update campaign
        if survey != {}:
            if "surveyId" in campaign:
                campaign["surveyId"] = survey["_id"]
            else:
                logging.warning(f'No "surveyId" field in campaign "{campaign_name}".')
            if "generativeAIServiceId" in campaign:
                campaign["generativeAIServiceId"] = service["_id"]
            else:
                logging.warning(
                    f'No "generativeAIServiceId" field in campaign "{campaign_name}".'
                )
            success = update_campaign(
                ncc_location, ncc_token, campaign["_id"], campaign
            )
            if success:
                logging.info(f'Campaign "{campaign_name}" updated.')
            else:
                logging.error(f'Campaign "{campaign_name}" not updated.')
        else:
            logging.warning(
                f'Insufficient data to update campaign "{campaign_name}". No survey available for update.'
            )

        # Create "parse transcription" script
        parse_transcription_script = search_scripts(
            ncc_location, ncc_token, "Parse transcriptionMessages"
        )
        if parse_transcription_script == {}:
            parse_transcription_script = create_parse_transcription_script(
                ncc_location, ncc_token, "Parse transcriptionMessages"
            )
            if parse_transcription_script != {}:
                logging.info('Script "Parse transcriptionMessages" created.')
            else:
                logging.error(f'Script "Parse transcriptionMessages" not created.')
        else:
            logging.info('Script "Parse transcriptionMessages" already exists.')

        # Create "parse summary" script
        parse_summary_script = search_scripts(ncc_location, ncc_token, "Parse summary")
        if parse_summary_script == {}:
            parse_summary_script = create_parse_summary_script(
                ncc_location, ncc_token, "Parse summary"
            )
            if parse_summary_script != {}:
                logging.info('Script "Parse summary" created.')
            else:
                logging.error(f'Script "Parse summary" not created.')
        else:
            logging.info('Script "Parse summary" already exists.')

        # Create "chat ticket" REST API object
        chat_rest_call = search_rest_calls(
            ncc_location, ncc_token, f"{campaign_name} - Create Freshdesk Chat Ticket"
        )
        if chat_rest_call == {}:
            chat_rest_call = freshdesk_create_chat_ticket_rest_call(
                ncc_location,
                ncc_token,
                freshdesk_subdomain,
                freshdesk_api_key,
                f"{campaign_name} - Create Freshdesk Chat Ticket",
            )
            if chat_rest_call != {}:
                logging.info(
                    f'REST API object "{campaign_name} - Create Freshdesk Chat Ticket" created.'
                )
            else:
                logging.error(
                    f'REST API object "{campaign_name} - Create Freshdesk Chat Ticket" not created.'
                )
        else:
            logging.info(
                f'REST API object "{campaign_name} - Create Freshdesk Chat Ticket" already exists.'
            )

        # Create "call ticket" REST API object
        call_rest_call = search_rest_calls(
            ncc_location, ncc_token, f"{campaign_name} - Create Freshdesk Call Ticket"
        )
        if call_rest_call == {}:
            call_rest_call = freshdesk_create_call_ticket_rest_call(
                ncc_location,
                ncc_token,
                freshdesk_subdomain,
                freshdesk_api_key,
                f"{campaign_name} - Create Freshdesk Call Ticket",
            )
            if call_rest_call != {}:
                logging.info(
                    f'REST API object "{campaign_name} - Create Freshdesk Call Ticket" created.'
                )
            else:
                logging.error(
                    f'REST API object "{campaign_name} - Create Freshdesk Call Ticket" not created.'
                )
        else:
            logging.info(
                f'REST API object "{campaign_name} - Create Freshdesk Call Ticket" already exists.'
            )

        # Create Freshdesk ticket function
        function = search_functions(
            ncc_location, ncc_token, f"{campaign_name} - Create Freshdesk Ticket"
        )
        if function == {}:
            if chat_rest_call != {} and call_rest_call != {}:
                function = freshdesk_create_ticket_function(
                    ncc_location,
                    ncc_token,
                    f"{campaign_name} - Create Freshdesk Ticket",
                    parse_summary_script,
                    chat_rest_call,
                    call_rest_call,
                )
                if function != {}:
                    logging.info(
                        f'Function "{campaign_name} - Create Freshdesk Ticket" created.'
                    )
                else:
                    logging.error(
                        f'Function "{campaign_name} - Create Freshdesk Ticket" not created.'
                    )
            else:
                logging.warning(
                    f'Insufficient data to create function "{campaign_name} - Create Freshdesk Ticket".'
                )
        else:
            logging.info(
                f'Function "{campaign_name} - Create Freshdesk Ticket" already exists.'
            )

        # Add logging to dispositions
        if add_logging == True:
            if function != {}:
                dispositions = get_dispositions(ncc_location, ncc_token)
                if len(dispositions) > 0:
                    for disposition in dispositions:
                        success = assign_function_to_dispositon(
                            ncc_location, ncc_token, function["_id"], disposition["_id"]
                        )
                        if success:
                            logging.info(
                                f'Disposition "{disposition["name"]}" updated.'
                            )
                        else:
                            logging.error(
                                f'Disposition "{disposition["name"]}" not updated.'
                            )
                else:
                    logging.warning(f"No dispositions found.")
            else:
                logging.warning(f"Insufficient data to update dispositions.")

        duration = datetime.datetime.now() - start_time
        logging.info(f"Duration: {str(duration)}")
