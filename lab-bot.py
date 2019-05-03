# adapted from: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

# WORKSPACE TOKEN NEEDS TO BE EXPORTED IN TERMINAL as described in documentation

import os
import time
import re
from slackclient import SlackClient
import json

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None

# DEFINE NEW MEMBERS FOR THE CHAT:  
#### To find these ID's use Slack interface as described in documentation
participant_user_id = "UHZ8UF4CR"
researcher_user_id = "UHZ8Y7WSV"
group_channel_id = "CHU6S0QP4"
part_bot_channel_id = "DJ7NJAYLV"
researcher_bot_channel_id = "DJ77S2F6G"

target_channel = group_channel_id
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_event(target_channel, slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            if event["user"] == researcher_user_id:
                text = event["text"]
    
                # Check whether the message text says GROUP or PARTICIPANT 
                if text == 'GROUP':
                    target_channel = group_channel_id 
                    print("You have switched to the GROUP channel. If you would like to change back please write PARTICIPANT")
                elif text == 'PARTICIPANT':
                    target_channel = part_bot_channel_id #participant_target_channel
                    print("You have switched to the PARTICIPANT channel. If you would like to change back please write GROUP")
                if text != None and text != 'GROUP' and text != 'PARTICIPANT':
                    send_message(target_channel, text, timestamp)
                time.sleep(RTM_READ_DELAY)
                return text, target_channel, event["ts"]

            # if the participant sends a personal message, then print that message in the researchers message
            elif event["user"] == participant_user_id and event["channel"] == part_bot_channel_id:
                text = event["text"]
                if text != None:
                    text = "The Participant: " + event["text"]
                    target_channel = researcher_bot_channel_id
                    send_message(target_channel, text, timestamp)
                    target_channel = part_bot_channel_id 
                time.sleep(RTM_READ_DELAY)
                return text, target_channel, event["ts"]
            return event["text"], target_channel, event["ts"]
    return None, target_channel, None
    

#  Helper for sending 
def send_message(target_channel, text, timestamp):
    slack_client.api_call(
        "chat.postMessage",
        channel=target_channel,
        text=text,
        )
    slack_client.api_call(
        "chat.update",
        channel=target_channel,
        ts=timestamp,
        text="dontknow",
        )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            text, target_channel, timestamp = parse_event(target_channel, slack_client.rtm_read())
    else:
        print("Connection failed. Exception traceback printed above.")


