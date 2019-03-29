# Code adapted from: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html


import os
import time
import re
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_event(target_channel, slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            
            #  Check the channel of incoming message. If it is the researcher, check if they are
            #  trying to switch the channel to either GROUP or PARTICIPANT.
            #  Forward to the target chanel target channel.

            # REMINDER: THE RESEARCHER SHOULD NEVER MESSAGE IN THE GROUP CHAT - it will forward it back to a channel

            #  Lily is acting as the researcher here
            if event["user"] == "UH5CJN1D3":
                # "DH5F2SWLD" for Devki
                # group channel ID = "CH289F6SX"
                # check whether the message text says GROUP or PARTICIPANT 
                text = event["text"]
                if text == 'GROUP':
                    target_channel = "CH289F6SX"
                    print("You have switched to the GROUP channel. If you would like to change back please write PARTICIPANT")
                elif text == 'PARTICIPANT':
                    #  using lily as place holder
                    target_channel = "DH51YLLJX"
                    print("You have switched to the PARTICIPANT channel. If you would like to change back please write GROUP") 
                
                print("target channel is", target_channel)
                if text != None and text != 'GROUP' and text != 'PARTICIPANT':
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
                time.sleep(RTM_READ_DELAY)
                return text, target_channel, event["ts"]
            return event["text"], target_channel, event["ts"]
    return None, None, None

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        target_channel = "DH51YLLJX"
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            text, target_channel, timestamp = parse_event(target_channel, slack_client.rtm_read())
    else:
        print("Connection failed. Exception traceback printed above.")
