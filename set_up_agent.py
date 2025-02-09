import datetime
import logging
from ncc_user import *


def set_up_agent(ncc_location: str, ncc_token: str):
    """
    This function creates an agent in Nextiva Contact Center (NCC) and assigns them to queues.
    """
    # Enter first name
    first_name = ""
    while first_name == "":
        print()
        first_name = input("First name: ")
        if first_name == "":
            print()
            print("Invalid first name.")
        else:
            first_name = f"Test {first_name}"

    # Enter last name
    last_name = ""
    while last_name == "":
        print()
        last_name = input("Last name: ")
        if last_name == "":
            print()
            print("Invalid last name.")

    # Enter email
    email = ""
    while email == "":
        print()
        email = input("Email: ")
        if email == "":
            print()
            print("Invalid email.")
        else:
            print()

    start_time = datetime.datetime.now()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting...")
    # Create agent
    agent = search_users(ncc_location, ncc_token, first_name, last_name)
    if agent == {}:
        agent = create_user(ncc_location, ncc_token, first_name, last_name, email)
        if agent != {}:
            logging.info(f'"{first_name} {last_name}" user created.')
        else:
            logging.warning(f'"{first_name} {last_name}" user not created.')
    else:
        logging.info(f'"{first_name} {last_name}" user already exists.')

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
