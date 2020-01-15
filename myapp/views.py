from django.shortcuts import render
# import HttpResponse to view result
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from library.df_response_lib import *
from db_query import *
from library.call_askjamie import calljamie
import json
from library import df_detectintent


def home(request):
    return HttpResponse('Hello World!')

def chatbot_view(request):
    if request.is_ajax():
        user_input = request.POST.get('user_input')
        # call charlie
        output = df_detectintent.detectintent_charlie(user_input)
        if ((output["intent"] == "Default Fallback Intent")):
            # call beta
            output = df_detectintent.detectintent_beta(user_input)
            if((output["intent"] == "Default Fallback Intent") or len(output["response"]) == 0) and output["intent"] != "ambiguous-intent":
                # call alpha
                output = df_detectintent.detectintent_alpha(user_input)

        #call jamie
        msfresponse = calljamie(user_input)
        return HttpResponse(json.dumps({"response": output["response"], "msfresponse": msfresponse}), content_type="application/json")
        # return HttpResponse(output["response"])
    else:
        return render(request, 'chatbot.html')


# not in use
@csrf_exempt
def webhook(request):
    req = json.loads(request.body)
    action = req.get('queryResult').get('action')
    print(action)
    text = req.get('queryResult').get('queryText')
    print(text)

    #text preprocessing
    # if text == "how can i open a child development account" or "how can i open a CDA":
    #     text = "How can I open a Child Development Account (CDA)?"
    # if text == "I have applied for the Baby Bonus Scheme. How can I open Child Development Account for my child?" or "I have applied for the Baby Bonus Scheme. How can I open CDA for my child?":
    #     text = "I have applied for the Baby Bonus Scheme. How can I open the Child Development Account (CDA) for my child?"

    if action == 'get_suggestion_chips':
        fulfillmentText = 'I did not understand your question. Here is some question suggestion related to "' + text + '."'
        question_suggestion = [i[0] for i in select_suggestions_by_keyword(text)]
        dr_sr = {'fulfillmentText': str(fulfillmentText) + '\n' + ''.join(question_suggestion)}

        # # GOOGLE
        # aog = actions_on_google_response()
        # aog_sr = aog.simple_response([
        #     [fulfillmentText, fulfillmentText, False]
        # ])
        # # create suggestion chips
        # # aog_sc = aog.suggestion_chips(["suggestion1", "suggestion2"])
        # # print(question_suggestion)
        count = 1
        question_list = []
        for i in question_suggestion:
            question_list.append([i])
            count = count + 1
            if count > 3:
                break

        print(question_list)
        # aog_sc = aog.suggestion_chips(question_suggestion)

        # FACEBOOK - CHANGE TO LIST TEMPLATE
        fb = facebook_response()
        fb_sr = fb.card_response(fulfillmentText, question_list)
        # print(fb.quick_replies(fulfillmentText, question_suggestion))
        # print(fb.button_response(fulfillmentText, question_suggestion))

        ff_response = fulfillment_response()
        question_list = []
        j = 1
        for i in question_suggestion:
            i = '<span><button id="question_suggestion' + str(j) + '" class="btn" style="width: 100%; background-color: white; opacity: 0.5; text-align: left;" onClick="myFunction(this)">' + i + '</button></span>'
            question_list.append(i)
            j = j + 1

        ff_text = ff_response.fulfillment_text(fulfillmentText + '<br>' + '<br>'.join(question_list))
        # ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
        ff_messages = ff_response.fulfillment_messages([dr_sr, fb_sr])
        reply = ff_response.main_response(ff_text, ff_messages)

    # return generated response
    return JsonResponse(reply, safe=False)

    # # build a request object
    # req = json.loads(request.body)
    # # get action from json
    # action = req.get('queryResult').get('action')
    # # return a fulfillment message
    # fulfillmentText = {'fulfillmentText': 'This is Django test response from webhook.'}
    # # return response
    # return JsonResponse(fulfillmentText, safe=False)
