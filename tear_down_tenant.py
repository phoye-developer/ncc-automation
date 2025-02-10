from config import *
from authentication_info import *
from ncc_disposition import *
from ncc_user_profile import *
from ncc_user_profile_disposition import *
from ncc_queue import *
from ncc_workflow import *
from ncc_function import *
from ncc_campaign import *
from ncc_survey import *
from ncc_survey_theme import *
from ncc_rest_call import *
from ncc_classification import *
from ncc_scorecard import *
from ncc_template import *
from ncc_topic import *
from ncc_report import *
from ncc_user import *


def tear_down_tenant(ncc_location: str, ncc_token: str) -> str:
    """
    This function deletes many of the entities created for the given NCC tenant.
    """
    print()

    # Delete campaign
    print('Searching for campaigns with "Test " prefix...', end="")
    campaigns = get_campaigns(ncc_location, ncc_token)
    if len(campaigns) > 0:
        print(f"found {len(campaigns)} campaign(s).")
        for campaign in campaigns:
            print(f'Deleting "{campaign["name"]}" campaign...', end="")
            success = delete_campaign(ncc_location, ncc_token, campaign["_id"])
            if success:
                print("success!")
            else:
                print("failed.")
    else:
        print("none found.")

    # Delete workflow
    print('Searching for workflows with "Test " prefix...', end="")
    workflows = get_workflows(ncc_location, ncc_token)
    if len(workflows) > 0:
        print(f"found {len(workflows)} workflow(s).")
        for workflow in workflows:
            print(f'Deleting "{workflow["name"]}" workflow...', end="")
            success = delete_workflow(ncc_location, ncc_token, workflow["_id"])
            if success:
                print("success!")
            else:
                print("failed.")
    else:
        print("none found.")

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

    # Delete topics
    print('Searching for topics with "Test " prefix...', end="")
    topics = get_topics(ncc_location, ncc_token)
    if len(topics) > 0:
        print(f"found {len(topics)} topic(s).")
    else:
        print("none found.")
    for topic in topics:
        print(f'Deleting "{topic["name"]}" topic...', end="")
        success = delete_topic(ncc_location, ncc_token, topic["_id"])
        if success:
            print("success!")
        else:
            print("failed.")

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

    # Delete survey themes
    print('Searching for survey themes with "Test " prefix...', end="")
    survey_themes = get_survey_themes(ncc_location, ncc_token)
    if len(survey_themes) > 0:
        print(f"found {len(survey_themes)} survey theme(s).")
    else:
        print("none found.")
    for survey_theme in survey_themes:
        print(f'Deleting "{survey_theme["name"]}" survey theme...', end="")
        success = delete_survey_theme(ncc_location, ncc_token, survey_theme["_id"])
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

    # Delete classifications
    print('Searching for classifications with "Test " prefix...', end="")
    classifications = get_classifications(ncc_location, ncc_token)
    if len(classifications) > 0:
        print(f"found {len(classifications)} classification(s).")
    else:
        print("none found.")
    for classification in classifications:
        print(f'Deleting "{classification["name"]}" classification...', end="")
        success = delete_classification(ncc_location, ncc_token, classification["_id"])
        if success:
            print("success!")
        else:
            print("failed.")

    # Delete scorecards
    print('Searching for scorecards with "Test " prefix...', end="")
    scorecards = get_scorecards(ncc_location, ncc_token)
    if len(scorecards) > 0:
        print(f"found {len(scorecards)} scorecard(s).")
    else:
        print("none found.")
    for scorecard in scorecards:
        print(f'Deleting "{scorecard["name"]}" scorecard...', end="")
        success = delete_scorecard(ncc_location, ncc_token, scorecard["_id"])
        if success:
            print("success!")
        else:
            print("failed.")

    # Delete templates
    print('Searching for templates with "Test " prefix...', end="")
    templates = get_templates(ncc_location, ncc_token)
    if len(templates) > 0:
        print(f"found {len(templates)} template(s).")
    else:
        print("none found.")
    for template in templates:
        print(f'Deleting "{template["name"]}" template...', end="")
        success = delete_template(ncc_location, ncc_token, template["_id"])
        if success:
            print("success!")
        else:
            print("failed.")

    # Delete reports
    print('Searching for reports with "Test " prefix...', end="")
    reports = get_reports(ncc_location, ncc_token)
    if len(reports) > 0:
        print(f"found {len(reports)} report(s).")
    else:
        print("none found.")
    for report in reports:
        print(f'Deleting "{report["name"]}" report...', end="")
        success = delete_report(ncc_location, ncc_token, report["_id"])
        if success:
            print("success!")
        else:
            print("failed.")

    # Delete users
    print('Searching for users with "Test " prefix...', end="")
    users = get_users(ncc_location, ncc_token)
    if len(users) > 0:
        print(f"found {len(users)} user(s).")
    else:
        print("none found.")
    for user in users:
        print(f'Deleting "{user["name"]}" user...', end="")
        success = delete_user(ncc_location, ncc_token, user["_id"])
        if success:
            print("success!")
        else:
            print("failed.")