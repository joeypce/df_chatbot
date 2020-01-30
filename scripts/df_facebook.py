import apiai
from flask import Flask, request
import json
import requests

# https://medium.com/ymedialabs-innovation/messenger-bot-using-flask-and-api-ai-f34f6e2eb6e6 #

CLIENT_ACCESS_TOKEN = 'c674cabec63a4eb4ab4258dc42ebdf8c'
PAGE_ACCESS_TOKEN = 'EAAlZAJWnHZB4ABAIHG34IhRpQFYvAWGh4zE1byc7xZAONB6VxXpwp9MW5VvxJOVXxw8fHnqYB1lWgB9xW9tEkgo6bYH4erzkvbCeSsjzih8GrZAIYiBI8j68A44F3L5yPAKmyGShZArZBBlVMmBaTeS5LUBjosgcfqpxq5J2SZAaBE6wgQ9h1w7A3m5sSvNUXIZD'
VERIFY_TOKEN = 'fypbabybonus'

# initialize the flask app
app = Flask(__name__)

# AI
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

# WEBHOOKS
# ===========================================
# GET
@app.route('/', methods=['GET'])
def handle_verification():
    '''
    Verifies facebook webhook subscription
    Successful when verify_token is same as token sent by facebook
    app
    '''
    if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):
        print("Verified")
        return request.args.get('hub.challenge', '')
    else:
        print("Wrong token")
        return "Error, wrong validation token"

# POST
@app.route('/', methods=['POST'])
def handle_message():
    '''
    Handle messages sent by facebook messenger to the applicaiton
    '''
    data = request.get_json()
    # continue processing

# PARSE MESSAGE
# ===========================================
def parse_user_text(user_text):
    '''
    Send the message to API AI which invokes an intent
    and sends the response accordingly
    '''
    request = ai.text_request()
    request.query = user_text
    response = json.loads(request.getresponse().read().decode('utf-8'))
    return response

def parse_natural_event(self, event, session_id, contexts):
    e = apiai.events.Event(event)
    request = ai.event_request(e)
    request.session_id = session_id  # unique for each user
    request.contexts = contexts    # a list
    response = json.loads(request.getresponse().read().decode("utf-8"))
    return response

# SENDING BACK MESSAGE TO FACEBOOK USER
# ===========================================
def send_response(sender_id, message_text):
    url = "https://graph.facebook.com/v2.6/me/messages"
    params = {'access_token': PAGE_ACCESS_TOKEN}
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': message_text}
    }
    response = requests.post(url, params=params, headers=headers,
                             json=data)
    return response

if __name__ == '__main__':\
    app.run(debug=True, port=8000)