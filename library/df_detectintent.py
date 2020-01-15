"""Install the following requirements:
    dialogflow        0.5.1
    google-api-core   1.4.1
"""
import dialogflow
import os
from google.api_core.exceptions import InvalidArgument

import db_query
from db_query import select_response_for_charlie

DIALOGFLOW_LANGUAGE_CODE = 'en-US'
SESSION_ID = 'current-user-id'

dirname = os.path.dirname(__file__)
alpha_filename = os.path.join(dirname, 'modelb-37edc-8bcbf482cbdf.json')
beta_filename = os.path.join(dirname, 'report-purpose-meceyp-e52d50746452.json')
charlie_filename = os.path.join(dirname, 'nlumodule-charlie-nrayfl-e494247ef306.json')

def detectintent_alpha(userinput):
    # os.environ[
    #     "GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Joey\PycharmProjects\SimpleUI\data\a\modelb-37edc-8bcbf482cbdf.json"
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = alpha_filename
    DIALOGFLOW_PROJECT_ID = 'modelb-37edc'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=userinput, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    print("Query text:", response.query_result.query_text)
    print("Detected intent of Alpha:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Response:", response.query_result.fulfillment_text)

    output = {
        'intent': response.query_result.intent.display_name,
        'response': response.query_result.fulfillment_text
    }

    return output

def detectintent_beta(userinput):
    # os.environ[
    #     "GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Joey\PycharmProjects\SimpleUI\data\report-purpose-meceyp-e52d50746452.json"
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = beta_filename
    DIALOGFLOW_PROJECT_ID = 'report-purpose-meceyp'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=userinput, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    print("Query text:", response.query_result.query_text)
    print("Detected intent of Beta:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Response:", response.query_result.fulfillment_text)
    print("Entities:", response.query_result.parameters.fields)
    res = response.query_result.fulfillment_text
    extraction_values = []

#ambiguity
    if response.query_result.intent.display_name == "ambiguous-intent":
        if response.query_result.parameters.fields["ambiguous-type"].string_value != "":
            question_suggestion = [i[0] for i in db_query.select_suggestions_by_keyword(response.query_result.parameters.fields["ambiguous-type"].string_value)]
            question_list = []
            j = 1
            question_list.append("I did not understand your question.<br/>Here are some questions related to '" + response.query_result.query_text + "'.<br/>")
            for i in question_suggestion:
                i = '<span><button onclick="myFunction(this)" id="question_suggestion" class="btn" style="width: 100%; background-color: white; opacity: 0.5; text-align: left; ">' + i + '</button></span>'
                # i = '<span><button id="question_suggestion' + str(
                #     j) + '" class="btn" style="width: 100%; background-color: white; opacity: 0.5; text-align: left;" onClick="copyPasteFunction(this.id)">' + i + '</button></span>'
                question_list.append(i)
                j = j + 1
            res = question_list
#1
    if response.query_result.intent.display_name == "what-is-intent":
        extraction_values.append("What is ")
        if response.query_result.parameters.fields["what-is-type"].string_value != "":
            extraction_values.append(response.query_result.parameters.fields["what-is-type"].string_value)
            res = [i[0] for i in db_query.select_response_for_beta("what-is", extraction_values)]
#2
    if response.query_result.intent.display_name == "what-are-intent":
        extraction_values.append("What are ")
        if response.query_result.parameters.fields["what-are-type"].string_value != "":
            extraction_values.append(response.query_result.parameters.fields["what-are-type"].string_value)
            res = [i[0] for i in db_query.select_response_for_beta("what-are", extraction_values)]
#3
    if response.query_result.intent.display_name == "how-do-i-intent":
        extraction_values.append("How do I ")
        if response.query_result.parameters.fields["how-do-i-type"].string_value != "":
            extraction_values.append(response.query_result.parameters.fields["how-do-i-type"].string_value)
            res = [i[0] for i in db_query.select_response_for_beta("how-do-i", extraction_values)]
#4
    if response.query_result.intent.display_name == "how-can-i-change-intent":
        extraction_values.append("How can I change ")
        if response.query_result.parameters.fields["how-can-i-change-type"].string_value != "":
            print(response.query_result.parameters.fields["how-can-i-change-type"])
            extraction_values.append(response.query_result.parameters.fields["how-can-i-change-type"].string_value)
            res = [i[0] for i in db_query.select_response_for_beta("how-can-i-change", extraction_values)]
#5
    if response.query_result.intent.display_name == "how-can-i-update-intent":
        extraction_values.append("How can I update ")
        if response.query_result.parameters.fields["how-can-i-update-type"].string_value != "":
            extraction_values.append(response.query_result.parameters.fields["how-can-i-update-type"].string_value)
            res = [i[0] for i in db_query.select_response_for_beta("how-can-i-update", extraction_values)]
#6
    if response.query_result.intent.display_name == "how-can-i-open-intent":
        extraction_values.append("How can I open ")
        if response.query_result.parameters.fields["how-can-i-open-type"].string_value != "":
            extraction_values.append(response.query_result.parameters.fields["how-can-i-open-type"].string_value)
            res = [i[0] for i in db_query.select_response_for_beta("how-can-i-open", extraction_values)]
#7
    if response.query_result.intent.display_name == "how-can-i-indicate-interest-intent":
        extraction_values.append("How can I indicate interest ")
        if response.query_result.parameters.fields["how-can-i-indicate-interest"].string_value != "":
            extraction_values.append(response.query_result.parameters.fields["how-can-i-indicate-interest"].string_value)
            res = [i[0] for i in db_query.select_response_for_beta("how-can-i-indicate-interest", extraction_values)]
#8
    if response.query_result.intent.display_name == "why-am-i-intent":
        extraction_values.append("Why am I ")
        if response.query_result.parameters.fields["why-am-i-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["why-am-i-type"].string_value)
            res = [i[0] for i in
                   db_query.select_response_for_beta("why-am-i", extraction_values)]
#9
    if response.query_result.intent.display_name == "why-is-intent":
        extraction_values.append("Why is ")
        if response.query_result.parameters.fields["why-is-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["why-is-type"].string_value)
            res = [i[0] for i in
                   db_query.select_response_for_beta("why-is", extraction_values)]
#10
    if response.query_result.intent.display_name == "i-have-intent":
        extraction_values.append("I have ")
        if response.query_result.parameters.fields["i-have-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["i-have-type"].string_value)
            res = [i[0] for i in
                   db_query.select_response_for_beta("i-have", extraction_values)]
#11
    if response.query_result.intent.display_name == "when-do-intent":
        extraction_values.append("When do ")
        if response.query_result.parameters.fields["when-do-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["when-do-type"].string_value)
            res = [i[0] for i in
                   db_query.select_response_for_beta("when-do", extraction_values)]
#12
    if response.query_result.intent.display_name == "when-will-intent":
        extraction_values.append("When will ")
        if response.query_result.parameters.fields["when-will-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["when-will-type"].string_value)
            res = [i[0] for i in
                   db_query.select_response_for_beta("when-will", extraction_values)]
#13
    if response.query_result.intent.display_name == "what-will-intent":
        extraction_values.append("What will ")
        if response.query_result.parameters.fields["what-will-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["what-will-type"].string_value)
            res = [i[0] for i in
                   db_query.select_response_for_beta("what-will", extraction_values)]
#14
    if response.query_result.intent.display_name == "how-can-i-check-intent":
        extraction_values.append("How can I check ")
        if response.query_result.parameters.fields["how-can-i-check-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["how-can-i-check-type"].string_value)
            res = [i[0] for i in
                   db_query.select_response_for_beta("how-can-i-check", extraction_values)]
    output = {
        'intent': response.query_result.intent.display_name,
        'response': res
    }

    return output

def detectintent_charlie(userinput):
    # os.environ[
    #     "GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Joey\PycharmProjects\SimpleUI\data\nlumodule-charlie-nrayfl-e494247ef306.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = charlie_filename
    DIALOGFLOW_PROJECT_ID = 'nlumodule-charlie-nrayfl'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=userinput, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    print("Query text:", response.query_result.query_text)
    print("Detected intent of Charlie:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Response:", response.query_result.fulfillment_text)
    extraction_values = []

    intentname = response.query_result.intent.display_name
    if intentname == "DeadlineDetails":
        if response.query_result.parameters.fields["deadline-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["deadline-type"].string_value)
    if intentname == "GetAddress":
        if response.query_result.parameters.fields["address-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["address-type"].string_value)
    if intentname == "GetContactDetails":
        if response.query_result.parameters.fields["contacts-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["contacts-type"].string_value)
    if intentname == "GetKeytermDetails":
        if response.query_result.parameters.fields["keyterm-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["keyterm-type"].string_value)
    if intentname == "UpdateRequest":
        if response.query_result.parameters.fields["update-type"].string_value != "":
            extraction_values.append(
                response.query_result.parameters.fields["update-type"].string_value)

    res = [i[0] for i in select_response_for_charlie(intentname, extraction_values)]
    output = {
        'intent': response.query_result.intent.display_name,
        'response': res
    }

    return output
