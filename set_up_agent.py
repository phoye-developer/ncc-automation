import datetime
import logging
from authentication_info import *
from datadog import *
from ncc_user_profile import *
from ncc_user import *
from ncc_queue import *
from ncc_user_queue import *
from ncc_supervisor_user import *
from ncc_topic import *


def set_up_agent(ncc_location: str, ncc_token: str, username: str):
    """
    This function creates an agent in Nextiva Contact Center (NCC) and assigns them to queues.
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
                "Agent Setup Cancelled",
                f'User "{username}" cancelled agent setup.',
                ["agentsetup"],
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
                    "Agent Setup Cancelled",
                    f'User "{username}" cancelled agent setup.',
                    ["agentsetup"],
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
                    "Agent Setup Cancelled",
                    f'User "{username}" cancelled agent setup.',
                    ["agentsetup"],
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

        # Select whether to assign agents to queues
        choice = ""
        while choice == "":
            print("Assign agent to all queues?")
            print("---------------------------")
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
                    "Agent Setup Cancelled",
                    f'User "{username}" cancelled agent setup.',
                    ["agentsetup"],
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

        # Select whether to assign agents to supervisors
        choice = ""
        while choice == "":
            print("Assign agent to all supervisors?")
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
                    "Agent Setup Cancelled",
                    f'User "{username}" cancelled agent setup.',
                    ["agentsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            elif choice == "1":
                assign_to_supervisors = True
            elif choice == "2":
                assign_to_supervisors = False
            else:
                choice = ""
                print("Invalid choice.")
                print()

    if cancelled == False:

        # Select whether to assign agent to topics
        choice = ""
        while choice == "":
            print("Assign agent to all topics?")
            print("---------------------------")
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
                    "Agent Setup Cancelled",
                    f'User "{username}" cancelled agent setup.',
                    ["agentsetup"],
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
        # Create agent
        agent = search_users(ncc_location, ncc_token, first_name, last_name)
        if agent == {}:
            agent_user_profile = search_user_profiles(ncc_location, ncc_token, "Agent")
            if agent_user_profile != {}:
                agent = create_user(
                    ncc_location,
                    ncc_token,
                    first_name,
                    last_name,
                    email,
                    agent_user_profile["_id"],
                )
                if agent != {}:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "success",
                        "normal",
                        "Agent Setup Successful",
                        f'Agent "{first_name} {last_name}" created.',
                        ["agentsetup"],
                    )
                    logging.info(f'Agent "{first_name} {last_name}" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Agent Setup Failed",
                        f'Agent "{first_name} {last_name}" not created.',
                        ["agentsetup"],
                    )
                    logging.error(f'Agent "{first_name} {last_name}" not created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Agent" not found.',
                    ["agentsetup"],
                )
                logging.warning('User profile "Agent" not found.')
        else:
            logging.info(f'Agent "{first_name} {last_name}" already exists.')

        # Assign agent to queues
        if agent != {} and assign_to_queues:
            queues = get_queues(ncc_location, ncc_token)
            if len(queues) > 0:
                for queue in queues:
                    success = search_user_queues(
                        ncc_location, ncc_token, agent["_id"], queue["_id"]
                    )
                    if success:
                        logging.info(
                            f'Agent "{agent["name"]}" already assigned to queue "{queue["name"]}".'
                        )
                    else:
                        success = create_user_queue(
                            ncc_location, ncc_token, agent["_id"], queue["_id"]
                        )
                        if success:
                            logging.info(
                                f'Agent "{agent["name"]}" assigned to queue "{queue["name"]}".'
                            )
                        else:
                            post_datadog_event(
                                dd_api_key,
                                dd_application_key,
                                username,
                                "error",
                                "normal",
                                "Agent Assignment to Queue Failed",
                                f'Agent "{agent["name"]}" not assigned to queue "{queue["name"]}".',
                                ["agentsetup"],
                            )
                            logging.error(
                                f'Agent "{agent["name"]}" not assigned to queue "{queue["name"]}".'
                            )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "No Queues Found",
                    "No queues found for agent assignment.",
                    ["agentsetup"],
                )
                logging.warning("No queues found for agent assignment.")

        # Assign agent to supervisors
        if agent != {} and assign_to_supervisors:
            supervisor_user_profile = search_user_profiles(
                ncc_location, ncc_token, "Supervisor"
            )
            if supervisor_user_profile != {}:
                supervisors = get_users(
                    ncc_location, ncc_token, supervisor_user_profile["_id"]
                )
                if len(supervisors) > 0:
                    for supervisor in supervisors:
                        success = search_supervisor_users(
                            ncc_location, ncc_token, supervisor["_id"], agent["_id"]
                        )
                        if success:
                            logging.info(
                                f'Agent "{first_name} {last_name}" already assigned to "{supervisor["firstName"]} {supervisor["lastName"]}".'
                            )
                        else:
                            success = create_supervisor_user(
                                ncc_location, ncc_token, supervisor["_id"], agent["_id"]
                            )
                            if success:
                                logging.info(
                                    f'Agent "{first_name} {last_name}" assigned to "{supervisor["firstName"]} {supervisor["lastName"]}".'
                                )
                            else:
                                post_datadog_event(
                                    dd_api_key,
                                    dd_application_key,
                                    username,
                                    "error",
                                    "normal",
                                    "Agent Assignment to Supervisor Failed",
                                    f'Agent "{first_name} {last_name}" not assigned to "{supervisor["firstName"]} {supervisor["lastName"]}".',
                                    ["agentsetup"],
                                )
                                logging.error(
                                    f'Agent "{first_name} {last_name}" not assigned to "{supervisor["firstName"]} {supervisor["lastName"]}".'
                                )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "No Supervisors Found",
                        "No supervisors found for agent assignment.",
                        ["agentsetup"],
                    )
                    logging.warning("No supervisors found for agent assignment.")
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Supervisor" not found.',
                    ["agentsetup"],
                )
                logging.warning('User profile "Supervisor" not found.')

        # Assign agent to topics
        if agent != {} and assign_to_topics:
            topics = get_topics(ncc_location, ncc_token)
            if len(topics) > 0:
                for topic in topics:
                    if "users" in topic:
                        users = topic["users"]
                    else:
                        users = []
                    if agent["_id"] in users:
                        logging.info(
                            f'Agent "{first_name} {last_name}" already assigned to topic "{topic["name"]}".'
                        )
                    else:
                        users.append(agent["_id"])
                        success = update_topic_users(
                            ncc_location, ncc_token, topic["_id"], users
                        )
                        if success:
                            logging.info(
                                f'Agent "{first_name} {last_name}" assigned to topic "{topic["name"]}".'
                            )
                        else:
                            post_datadog_event(
                                dd_api_key,
                                dd_application_key,
                                username,
                                "error",
                                "normal",
                                "Agent Assignment to Topic Failed",
                                f'Agent "{first_name} {last_name}" not assigned to topic "{topic["name"]}".',
                                ["agentsetup"],
                            )
                            logging.error(
                                f'Agent "{first_name} {last_name}" not assigned to topic "{topic["name"]}".'
                            )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "No Topics Found",
                    "No topics found for agent assignment",
                    ["agentsetup"],
                )
                logging.warning("No topics found for agent assignment.")

        duration = datetime.datetime.now() - start_time
        logging.info(f"Duration: {str(duration)}")
