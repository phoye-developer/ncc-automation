import datetime
import logging
from datadog import *
from authentication_info import *
from ncc_user_profile import *
from ncc_user import *
from ncc_queue import *
from ncc_user_queue import *
from ncc_supervisor_user import *
from ncc_supervisor_queue import *
from ncc_campaign import *
from ncc_supervisor_campaign import *
from ncc_topic import *


def set_up_supervisor(ncc_location: str, ncc_token: str, username: str):
    """
    This function creates a supervisor in Nextiva Contact Center (NCC), assigns them to queues, and assigns agents for them to supervise.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    cancelled = False

    print()
    print('Enter "cancel" at any prompt to cancel.')

    # Enter first name
    first_name = ""
    while first_name == "":
        print()
        first_name = input("First name: ")
        if first_name.lower() == "cancel":
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Supervisor Setup Cancelled",
                f'User "{username}" cancelled supervisor setup.',
                ["supervisorsetup"],
            )
            print()
            print("Operation cancelled.")
            cancelled = True
        elif first_name == "":
            print()
            print("Invalid first name.")

    if cancelled == False:

        # Enter last name
        last_name = ""
        while last_name == "":
            print()
            last_name = input("Last name: ")
            if last_name.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Supervisor Setup Cancelled",
                    f'User "{username}" cancelled supervisor setup.',
                    ["supervisorsetup"],
                )
                print()
                print("Operation cancelled.")
                cancelled = True
            elif last_name == "":
                print()
                print("Invalid last name.")

    if cancelled == False:

        # Enter email
        email = ""
        while email == "":
            print()
            email = input("Email: ")
            if email.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Supervisor Setup Cancelled",
                    f'User "{username}" cancelled supervisor setup.',
                    ["supervisorsetup"],
                )
                print()
                print("Operation cancelled.")
                cancelled = True
            elif email == "":
                print()
                print("Invalid email.")
            else:
                print()

    if cancelled == False:

        # Select whether to assign supervisors to queues
        choice = ""
        while choice == "":
            print("Assign supervisor to all queues?")
            print("--------------------------------")
            print("1. Yes")
            print("2. No")
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
                    "Supervisor Setup Cancelled",
                    f'User "{username}" cancelled supervisor setup.',
                    ["supervisorsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            elif choice == "1":
                assign_to_queues = True
            elif choice == "2":
                assign_to_queues = False
            else:
                choice = ""
                print("Invalid choice.")
                print()

    if cancelled == False:

        # Select whether to assign all agents to the supervisor
        choice = ""
        while choice == "":
            print("Assign all agents to supervisor?")
            print("--------------------------------")
            print("1. Yes")
            print("2. No")
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
                    "Supervisor Setup Cancelled",
                    f'User "{username}" cancelled supervisor setup.',
                    ["supervisorsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            elif choice == "1":
                assign_agents = True
            elif choice == "2":
                assign_agents = False
            else:
                choice = ""
                print("Invalid choice.")
                print()

    if cancelled == False:

        # Select whether to assign all campaigns to the supervisor
        choice = ""
        while choice == "":
            print("Assign supervisor to all campaigns?")
            print("-----------------------------------")
            print("1. Yes")
            print("2. No")
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
                    "Supervisor Setup Cancelled",
                    f'User "{username}" cancelled supervisor setup.',
                    ["supervisorsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            elif choice == "1":
                assign_to_campaigns = True
            elif choice == "2":
                assign_to_campaigns = False
            else:
                choice = ""
                print("Invalid choice.")
                print()

    if cancelled == False:

        # Select whether to assign supervisor to topics
        choice = ""
        while choice == "":
            print("Assign supervisor to all topics?")
            print("--------------------------------")
            print("1. Yes")
            print("2. No")
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
                    "Supervisor Setup Cancelled",
                    f'User "{username}" cancelled supervisor setup.',
                    ["supervisorsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            elif choice == "1":
                assign_to_topics = True
            elif choice == "2":
                assign_to_topics = False
            else:
                choice = ""
                print("Invalid choice.")
                print()

    if cancelled == False:

        start_time = datetime.datetime.now()

        logging.info("Starting...")
        # Create supervisor
        supervisor = search_users(ncc_location, ncc_token, first_name, last_name)
        if supervisor == {}:
            supervisor_user_profile = search_user_profiles(
                ncc_location, ncc_token, "Supervisor"
            )
            if supervisor_user_profile != {}:
                supervisor = create_user(
                    ncc_location,
                    ncc_token,
                    first_name,
                    last_name,
                    email,
                    supervisor_user_profile["_id"],
                )
                if supervisor != {}:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "success",
                        "normal",
                        "Supervisor Setup Successful",
                        f'Supervisor "{first_name} {last_name}" created.',
                        ["supervisorsetup"],
                    )
                    logging.info(f'Supervisor "{first_name} {last_name}" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Supervisor Setup Failed",
                        f'Supervisor "{first_name} {last_name}" not created.',
                        ["supervisorsetup"],
                    )
                    logging.error(f'Supervisor "{first_name} {last_name}" not created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Supervisor" not found.',
                    ["supervisorsetup"],
                )
                logging.warning('User profile "Supervisor" not found.')
        else:
            logging.info(f'Supervisor "{first_name} {last_name}" already exists.')

        # Assign supervisor to queues
        if supervisor != {} and assign_to_queues:
            queues = get_queues(ncc_location, ncc_token)
            if len(queues) > 0:
                for queue in queues:
                    success = search_supervisor_queues(
                        ncc_location, ncc_token, supervisor["_id"], queue["_id"]
                    )
                    if success:
                        logging.info(
                            f'Supervisor "{supervisor["name"]}" already assigned to queue "{queue["name"]}".'
                        )
                    else:
                        success = create_supervisor_queue(
                            ncc_location, ncc_token, supervisor["_id"], queue["_id"]
                        )
                        if success:
                            logging.info(
                                f'Supervisor "{supervisor["name"]}" assigned to queue "{queue["name"]}".'
                            )
                        else:
                            post_datadog_event(
                                dd_api_key,
                                dd_application_key,
                                username,
                                "error",
                                "normal",
                                "Supervisor Assignment to Queue Failed",
                                f'Supervisor "{supervisor["name"]}" not assigned to queue "{queue["name"]}".',
                                ["supervisorsetup"],
                            )
                            logging.error(
                                f'Supervisor "{supervisor["name"]}" not assigned to queue "{queue["name"]}".'
                            )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "No Queues Found",
                    "No queues found for supervisor assignment.",
                    ["supervisorsetup"],
                )
                logging.warning("No queues found for supervisor assignment.")

        # Assign agents to supervisor
        if supervisor != {} and assign_agents:
            agent_user_profile = search_user_profiles(ncc_location, ncc_token, "Agent")
            if agent_user_profile != {}:
                agents = get_users(ncc_location, ncc_token, agent_user_profile["_id"])
                if len(agents) > 0:
                    for agent in agents:
                        success = search_supervisor_users(
                            ncc_location, ncc_token, supervisor["_id"], agent["_id"]
                        )
                        if success:
                            logging.info(
                                f'Agent "{agent["firstName"]} {agent["lastName"]}" already assigned to "{first_name} {last_name}".'
                            )
                        else:
                            success = create_supervisor_user(
                                ncc_location, ncc_token, supervisor["_id"], agent["_id"]
                            )
                            if success:
                                logging.info(
                                    f'Agent "{agent["firstName"]} {agent["lastName"]}" assigned to "{first_name} {last_name}".'
                                )
                            else:
                                post_datadog_event(
                                    dd_api_key,
                                    dd_application_key,
                                    username,
                                    "error",
                                    "normal",
                                    "Agent Assignment to Supervisor Failed",
                                    f'Agent "{agent["firstName"]} {agent["lastName"]}" not assigned to "{first_name} {last_name}".',
                                    ["supervisorsetup"],
                                )
                                logging.error(
                                    f'Agent "{agent["firstName"]} {agent["lastName"]}" not assigned to "{first_name} {last_name}".'
                                )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "No Agents Found",
                        "No agents found for supervisor assignment.",
                        ["supervisorsetup"],
                    )
                    logging.warning("No agents found for supervisor assignment.")
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Agent" not found for supervisor assignment.',
                    ["supervisorsetup"],
                )
                logging.warning(
                    'User profile "Agent" not found for supervisor assignment.'
                )

        # Assign supervisor to campaigns
        if supervisor != {} and assign_to_campaigns:
            campaigns = get_campaigns(ncc_location, ncc_token)
            if len(campaigns) > 0:
                for campaign in campaigns:
                    success = search_supervisor_campaigns(
                        ncc_location, ncc_token, supervisor["_id"], campaign["_id"]
                    )
                    if success:
                        logging.info(
                            f'Supervisor "{first_name} {last_name}" already assigned to campaign "{campaign["name"]}".'
                        )
                    else:
                        success = create_supervisor_campaign(
                            ncc_location, ncc_token, supervisor["_id"], campaign["_id"]
                        )
                        if success:
                            logging.info(
                                f'Supervisor "{first_name} {last_name}" assigned to campaign "{campaign["name"]}".'
                            )
                        else:
                            post_datadog_event(
                                dd_api_key,
                                dd_application_key,
                                username,
                                "error",
                                "normal",
                                "Supervisor Assignment to Campaign Failed",
                                f'Supervisor "{first_name} {last_name}" not assigned to campaign "{campaign["name"]}".',
                                ["supervisorsetup"],
                            )
                            logging.error(
                                f'Supervisor "{first_name} {last_name}" not assigned to campaign "{campaign["name"]}".'
                            )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "No Campaigns Found",
                    "No campaigns found for supervisor assignment.",
                    ["supervisorsetup"],
                )
                logging.warning("No campaigns found for supervisor assignment.")

        # Assign supervisor to topics
        if supervisor != {} and assign_to_topics:
            topics = get_topics(ncc_location, ncc_token)
            if len(topics) > 0:
                for topic in topics:
                    if "users" in topic:
                        users = topic["users"]
                    else:
                        users = []
                    if supervisor["_id"] in users:
                        logging.info(
                            f'Supervisor "{first_name} {last_name}" already assigned to topic "{topic["name"]}".'
                        )
                    else:
                        users.append(supervisor["_id"])
                        success = update_topic_users(
                            ncc_location, ncc_token, topic["_id"], users
                        )
                        if success:
                            logging.info(
                                f'Supervisor "{first_name} {last_name}" assigned to topic "{topic["name"]}".'
                            )
                        else:
                            post_datadog_event(
                                dd_api_key,
                                dd_application_key,
                                username,
                                "error",
                                "normal",
                                "Supervisor Assignment to Topic Failed",
                                f'Supervisor "{first_name} {last_name}" not assigned to topic "{topic["name"]}".',
                                ["supervisorsetup"],
                            )
                            logging.error(
                                f'Supervisor "{first_name} {last_name}" not assigned to topic "{topic["name"]}".'
                            )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "No Topics Found",
                    "No Topics found for supervisor assignment.",
                    ["supervisorsetup"],
                )
                logging.warning("No topics found for assignment.")

        duration = datetime.datetime.now() - start_time
        logging.info(f"Duration: {str(duration)}")
