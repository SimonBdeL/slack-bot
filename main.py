import os
from dotenv import load_dotenv
import slack
# from slack_bolt.adapter.socket_mode import SocketModeHandler
import ssl
from flask import Flask
from slackeventsapi import SlackEventAdapter
from functions import get_user_name
from messages import welcome_message, create_new_event_message, report_issue_message, hi_message, unclear_question_message, greetings, goodbyes, bye_message, help_message
ssl._create_default_https_context = ssl._create_unverified_context

# Load environment variables from .env file
env_path = ".env"
load_dotenv(env_path)

# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

# Initialize Slack WebClient with bot token
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# Define a dictionary to keep track of users the bot has welcomed
users_welcomed = {}

@slack_event_adapter.on('message')
def message(payload):
    global users_welcomed

    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    #skip responses from the bot itself
    if user_id != os.environ['BOT_ID']:
        # Check if the user has already been welcomed
        if user_id not in users_welcomed or not users_welcomed[user_id]:
            client.chat_postMessage(
                channel=channel_id,
                text='Hi ' + get_user_name(client, user_id) + "! \n" + welcome_message
                )
            users_welcomed[user_id] = True
        elif text:
            # Check for the specific question and respond accordingly
            if 'help' in text.lower():
                client.chat_postMessage(
                    channel=channel_id,
                    text=help_message
                )
            elif 'create a new event' in text.lower():
                client.chat_postMessage(
                    channel=channel_id,
                    text=create_new_event_message
                )
            elif 'report an issue' in text.lower():
                client.chat_postMessage(
                    channel=channel_id,
                    text=report_issue_message
                )
            elif any(greet in text.lower() for greet in greetings):
                client.chat_postMessage(
                    channel = channel_id,
                    text = 'Hi ' + get_user_name(client, user_id) + '!' + hi_message
                )
            elif any(goodbye in text.lower() for goodbye in goodbyes):
                client.chat_postMessage(
                    channel=channel_id,
                    text=bye_message
                )
            elif 'bug'in text.lower():
                client.chat_postMessage(
                    channel=channel_id,
                    text='miam!'
                )
            else:
                client.chat_postMessage(
                    channel=channel_id,
                    text=unclear_question_message
                )


if __name__ == "__main__":
    app.run(debug=True, port=9000)
