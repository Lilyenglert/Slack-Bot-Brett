# adapted from: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html


import os
import time
import re
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None

# DEFINE NEW MEMBERS FOR THE CHAT:  
#### To find these ID's uncomment the section with the header "ID UPDATE FOR NEW PARTICIPANTS"
# Participant user id:
participant_user_id = "UH2MEGTU5"
# Participant - bot channel id: 
part_bot_channel_id = "DH5F2SWLD"
# Group channel id: 
group_channel_id = "CH289F6SX"
# Researcher - bot channel id:
researcher_bot_channel_id = "UH5CJN1D3"

# "UH2MEGTU5" = Devki user id 
# "DH5F2SWLD" for Devki-bot Channel
# "DH51YLLJX" for Lily Channel
# group channel ID = "CH289F6SX"


target_channel = "DH5F2SWLD"
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_event(target_channel, slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            # ID UPDATE FOR NEW PARTICIPANTS: Uncomment the lines one at a time and send the message 
            # participant ID , 
            ############
            print()
            ############

            if event["user"] == "UH5CJN1D3":
                # check whether the message text says GROUP or PARTICIPANT 
                text = event["text"]
                if text == 'GROUP':
                    # group channel ID = "CH289F6SX"
                    target_channel = "CH289F6SX"  #group_target_channel
                    print("You have switched to the GROUP channel. If you would like to change back please write PARTICIPANT")
                elif text == 'PARTICIPANT':
                    target_channel = "DH5F2SWLD" #participant_target_channel
                    print("You have switched to the PARTICIPANT channel. If you would like to change back please write GROUP") 
                elif text == 'ERASE ALL MESSAGES':
                    #### ADD function to clear channel
                    print("messages have been erased")                
                print("target channel is", target_channel)
                if text != None and text != 'GROUP' and text != 'PARTICIPANT':
                    send_message(target_channel, text, timestamp)

                time.sleep(RTM_READ_DELAY)
                return text, target_channel, event["ts"]

            # if the participant sends a personal message, then print that message in the researchers
            # chat with the prefix: participant says: 
            elif event["user"] == "UH2MEGTU5" and event["channel"] == "DH5F2SWLD":
                text = event["text"]
                if text != None:
                    text = "The Participant: " + event["text"]
                    target_channel = "DH51YLLJX"
                    send_message(target_channel, text, timestamp)
                time.sleep(RTM_READ_DELAY)
                return text, target_channel, event["ts"]

            return event["text"], target_channel, event["ts"]
    return None, target_channel, None
    

#  Helper for sending 
def send_message(target_channel, text, timestamp):
    slack_client.api_call(
        "chat.postMessage",
        channel=target_channel,
        text=text
        )
    slack_client.api_call(
        "chat.update",
        channel=target_channel,
        ts=timestamp,
        text="dontknow"
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


